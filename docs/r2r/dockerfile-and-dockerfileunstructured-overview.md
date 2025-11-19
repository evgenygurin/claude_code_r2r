## **Dockerfile and Dockerfile.unstructured Overview**

### **Dockerfile**

The `Dockerfile` is used to build the R2R application image.

- **Base Image**: `python:3.12-slim`
- **System Dependencies**: GCC, G++, Musl-dev, Curl, Libffi-dev, Gfortran, Libopenblas-dev, Poppler-utils, Rust (via Rustup)
- **Python Dependencies**: Installed via Poetry with extras `core ingestion-bundle`
- **Final Image**: Copies site-packages and binaries from the builder stage, sets environment variables, exposes the configured port, and runs the application using Uvicorn.

### **Dockerfile.unstructured**

The `Dockerfile.unstructured` builds the Unstructured service image.

- **Base Image**: `python:3.12-slim`
- **System Dependencies**: GCC, G++, Musl-dev, Curl, Libffi-dev, Gfortran, Libopenblas-dev, Tesseract-OCR, Libleptonica-dev, Poppler-utils, Libmagic1, Pandoc, LibreOffice, OpenCV dependencies
- **Python Dependencies**: Installed Unstructured with `unstructured[all-docs]`, Gunicorn, Uvicorn, FastAPI, HTTPX
- **Final Steps**: Copies `main.py`, exposes port `7275`, and runs the application using Uvicorn with 8 workers.

---