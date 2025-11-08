# Start from the official Python 3.12 image for a modern Python environment.
# Meaning to start with a clean Linux environment that already has Python 3.12.3 installed.
# This is our foundation (a.k.a Base Image)
FROM python:3.12.3

# it is recommended when using Python inside a Docker container
# Make Python output print immediately instead of waiting - crucial for seeing logs in real-time in Docker
ENV PYTHONUNBUFFERED=1

# Docker best practices
# Ref: https://docs.docker.com/build/building/best-practices/#workdir
# For clarity and reliability, you should always use absolute paths for your WORKDIR.
# Also, you should use WORKDIR instead of proliferating instructions like RUN cd … && do-something,
# which are hard to read, troubleshoot, and maintain.
# Set the working directory to /app for all subsequent commands meaning
WORKDIR /app/

# Copy the uv and uvx binaries from UV's official image into our /bin directory.
# This is faster than installing via pip (RUN pip install uv) and is recommended for Docker builds.
# uv version: 0.9.5 (can update tag as needed)
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

# Make sure when we run Python commands, they use the virtual environment
# we'll create in /app/.venv instead of the system Python.
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode  / UV Optimization Settings (1)
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
# Compile Python files to bytecode for faster runtime startup as recommended in uv integration guides.
ENV UV_COMPILE_BYTECODE=1

# uv Cache / UV Optimization Settings (2)
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
# Use 'copy' linking mode for dependency caching during installation.
# Optimize how dependencies are installed for Docker
ENV UV_LINK_MODE=copy

# Install dependencies using uv and advanced Docker build mounts.
# This step uses Docker's cache-mount to speed up builds and bind-mounts to use lockfiles for reproducible installs.
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# --mount=type=cache: "Keep UV's cache between builds so subsequent builds are faster
# --mount=type=bind: "Temporarily make uv.lock and pyproject.toml available during this step
# uv sync --frozen --no-install-project: "Install all dependencies from pyproject.toml and uv.lock
# but don't install our actual application code yet"
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Tell Python to look for modules in the /app directory.
ENV PYTHONPATH=/app

# NOW copy our actual FastAPI application code and other necessary files into the container.
COPY ./app /app/app

# Optionally copy supporting files (license, readme, etc.)
COPY LICENSE README.md Makefile ./


# Document that this container will listen on port 8000. This is mostly for documentation.
# Actual port mapping happens with -p in docker run
EXPOSE 8000

# Start FastAPI via uv's Python runner, setting worker count to 4 for better multi-core support.
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]

# Why This Structure is Smart:
#    Dependencies first, code last - If you change your code but not dependencies, Docker can reuse the cached dependency layer
#    UV cache mounting - Makes rebuilds much faster
#    Separate dependency install from code copy - Optimizes Docker's build cache
