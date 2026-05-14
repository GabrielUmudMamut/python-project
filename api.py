from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
import os
import zipfile
import io

app = FastAPI()

@app.get("/")
def serve_webpage():
    return FileResponse("webpage/index.html")

#ai generated code start
@app.get("/api/download-zip/")
def download_zip(files: list[str] = Query(None)):
    if not files:
        return {"error": "No files selected"}

    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file in files:
            file_path = f"data/entries/{file}"
            # Double check the file actually exists before zipping
            if os.path.exists(file_path):
                zip_file.write(file_path, arcname=file)
    
    # Rewind the memory buffer to the beginning
    zip_buffer.seek(0)
    
    # Send it to the browser with a pre-assigned name
    return StreamingResponse(
        zip_buffer, 
        media_type="application/zip", 
        headers={"Content-Disposition": "attachment; filename=inventory_reports.zip"}
    )

@app.get("/api/files/")
def list_available_files():
    folder_path = "data/entries"
    if not os.path.exists(folder_path):
        return {"files": []}
    all_files = os.listdir(folder_path)
    json_files = [f for f in all_files if f.endswith('.json')]
    return {"files": json_files}
# ai generated code end

@app.get("/{what}/{filename}/")
def init(filename: str, what: str):
    file_path = f"data/entries/{filename}"
    if what == "down":
        return FileResponse(path=file_path, filename=filename)
    elif what == "view":
        return FileResponse(path=file_path)
    else:
        return {"status": "error", "text": "What you doing? You can only view or download the file."}

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start_server()