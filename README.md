# Website Screenshot Tool Backend

This is the backend for the Website Screenshot Tool, built with FastAPI and Playwright. It provides API endpoints to capture screenshots of a website and its internal pages, and to download all screenshots as a ZIP file.

## Features
- `/screenshot` endpoint: Accepts a URL, crawls internal links, and captures screenshots
- `/screenshots` static route: Serves screenshot images
- `/download_zip/{folder}` endpoint: Download all screenshots as a ZIP
- CORS enabled for frontend integration

## Requirements
- Python 3.8+
- Playwright
- FastAPI
- Uvicorn

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install --with-deps
```

### 2. Run locally
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. CORS Configuration
- By default, CORS is enabled for all origins. For production, set `allow_origins` in `main.py` to your frontend domain for security.

### 4. Deploying to Render
- Add a `render.yaml` with the following content:
```yaml
services:
  - type: web
    name: fastapi-backend
    env: python
    buildCommand: |
      pip install -r requirements.txt
      playwright install --with-deps
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
    plan: free
```
- Push your code to GitHub and connect the repo to Render.
- Set the root directory to `backend/` if prompted.

## Notes
- Screenshots are saved in the `screenshots/` directory and served as static files.
- The backend must be accessible from the frontend for API calls and image loading. 