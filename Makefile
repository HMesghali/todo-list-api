.PHONY: clean

clean:
	@echo "🧹 Clearing Python cache and build files..."

	# Remove Python cache directories
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

	# Remove Python compiled files
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name "*.pyc.*" -delete

	# Remove build and distribution directories
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .eggs/

	@echo "✅ Python cache and build files cleared!"
