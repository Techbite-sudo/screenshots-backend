from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
import shutil
from screenshot_service import take_screenshots_of_all_links_api

app = FastAPI()

# CORS setup: allow all origins for now (customize in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the screenshots directory exists
SCREENSHOTS_ROOT = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOTS_ROOT, exist_ok=True)

# Mount the static files route
app.mount("/screenshots", StaticFiles(directory=SCREENSHOTS_ROOT), name="screenshots")

@app.get("/screenshot")
async def screenshot(url: str = Query(..., description="URL to screenshot")):
    # Generate a unique folder for this request
    folder = f"screenshots_{uuid.uuid4().hex}"
    output_folder = os.path.join(SCREENSHOTS_ROOT, folder)
    os.makedirs(output_folder, exist_ok=True)
    # Call the screenshot function (refactored to accept url and output folder)
    screenshots = await take_screenshots_of_all_links_api(url, output_folder)
    # Return a list of screenshot URLs
    screenshot_urls = [f"/screenshots/{folder}/{os.path.basename(path)}" for path in screenshots]
    return JSONResponse({"screenshots": screenshot_urls, "folder": folder})

@app.get("/download_zip/{folder}")
def download_zip(folder: str):
    folder_path = os.path.join(SCREENSHOTS_ROOT, folder)
    if not os.path.isdir(folder_path):
        return JSONResponse({"error": "Folder not found"}, status_code=404)
    zip_path = os.path.join(SCREENSHOTS_ROOT, f"{folder}.zip")
    shutil.make_archive(base_name=zip_path[:-4], format='zip', root_dir=folder_path)
    return FileResponse(zip_path, filename=f"{folder}.zip", media_type='application/zip') 