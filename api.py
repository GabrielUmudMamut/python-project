from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

@app.get("/")
def serve_webpage():
    return FileResponse("webpage/index.html")

#ai generated code start
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