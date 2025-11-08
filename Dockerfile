# Start from the official Python 3.12 image for a modern Python environment.
# the specific Python version of our project: 3.12.3
FROM python:3.12.3

# Make Python output show immediately in Docker logs (no delays)
# helps in real-time logging and debugging by disabling output buffering
# it is recommended when using Python inside a Docker container
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app for all subsequent commands meaning
# all commands will run in the /app folder inside the container
WORKDIR /app/

# Install 'uv' by copying its binaries from the official Astral image.
# This is a fast and version-consistent approach, recommended for Docker builds.
# uv version: 0.9.5 (can update tag as needed)
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

# Alternative approach (commented for reference): install uv using pip.
# RUN pip install uv

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
# Make sure our installed tools are found first when running commands
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
# Compile Python files to bytecode for faster runtime startup as recommended in uv integration guides.
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
# Use 'copy' linking mode for dependency caching during installation.
# Optimize how dependencies are installed for Docker
ENV UV_LINK_MODE=copy

# Install dependencies using uv and advanced Docker build mounts.
# This step uses Docker's cache-mount to speed up builds and bind-mounts to use lockfiles for reproducible installs.
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Tell Python where to find our application code
ENV PYTHONPATH=/app

# Copy our actual application code into the container
COPY ./app /app/app

# Optionally copy supporting files (license, readme, etc.)
COPY LICENSE README.md Makefile ./


# Expose port 8000, the default for FastAPI ("fastapi run ...").
EXPOSE 8000

# Start FastAPI via uv's Python runner, setting worker count to 4 for better multi-core support.
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
