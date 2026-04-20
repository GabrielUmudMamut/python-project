from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware #ai told me to do this
import os, time, pyautogui, requests, subprocess, shutil, io

app = FastAPI()
app.add_middleware( #ai 
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (good for local testing)
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
) #ai

@app.get("/")
def init():
    return RedirectResponse(url="/page/index.html")

@app.get("/page/index.html")
def init():
    return FileResponse(os.path.join("page", "index.html"))

@app.get("/page/style.css")
def get_style():
    return FileResponse(os.path.join("page", "style.css"))

@app.get("/page/script.js")
def get_script():
    return FileResponse(os.path.join("page", "script.js"))

@app.get("/assets/favicon.ico")
def get_favicon():
    return FileResponse(os.path.join("assets", "favicon.ico"))

@app.get("/installsteam")
def installsteam():
    try:
        subprocess.run(["winget", "install", "--id", "Valve.Steam", "--silent", "--accept-package-agreements"], check=True)
        return {"status": "success", "message": "Steam installation initiated successfully."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

@app.get("/opensteam")
def steamopen():
    try:
        os.system(f"start steam://")
        return {"status": "success", "message": "Steam launched."}
    except:
        return {"status": "error", "message": "For some reason steam did not launch."}

@app.get("/closesteam")
def steamclose():
    try:
        os.system("taskkill /f /im steam.exe")
        return {"status": "success", "message": "Steam closed."}
    except:
        return {"status": "error", "message": "For some reason steam did not close."}

@app.get("/storage")
def getremainingstorage():
    try:
        total, used, free = shutil.disk_usage("/")
        gb_divider = 1024 ** 3
        total_gb = round(total / gb_divider, 1)
        used_gb = round(used / gb_divider, 1)
        free_gb = round(free / gb_divider, 1)
        
        return {"status": "success", "total_GB": total_gb, "used_GB": used_gb, "free_GB": free_gb}
    except:
        return {"status": "error", "message": "Could not retrieve storage information."}

@app.get("/si/{game_id}")
def steaminstall(game_id: int):
    os.system(f"start steam://install/{game_id}")
    time.sleep(3)
    try:
        response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game_id}")
        steam_data = response.json()
        if steam_data[str(game_id)]['success']:
            game_name = steam_data[str(game_id)]['data']['name']
        else:
            game_name = "Unknown Game"
    except Exception:
        game_name = "Unknown Game"
    try:
        x, y = pyautogui.locateCenterOnScreen('assets/install_button.png', confidence=0.8)
        pyautogui.click(x, y)
        
        # 3. FastAPI automatically converts Python dictionaries to data your JS can easily read
        return {"status": "success", "game_name": game_name, "steam_id": game_id, "message": f"Game called {game_name} with the id {game_id} has tried to start installing."}
        
    except pyautogui.ImageNotFoundException:
        return {"status": "error", "game_name": game_name, "steam_id": game_id, "message": f"Game called {game_name} with the id {game_id} has tried to start installing but the install button was not found."}

@app.get("/uninstall/{game_id}")
def steamuninstall(game_id: int):
    os.system(f"start steam://uninstall/{game_id}")
    time.sleep(3)
    try:
        response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game_id}")
        steam_data = response.json()
        if steam_data[str(game_id)]['success']:
            game_name = steam_data[str(game_id)]['data']['name']
        else:
            game_name = "Unknown Game"
    except Exception:
        game_name = "Unknown Game"
    try:
        x, y = pyautogui.locateCenterOnScreen('assets/uninstall_button.png', confidence=0.8)
        pyautogui.click(x, y)
        
        # 3. FastAPI automatically converts Python dictionaries to data your JS can easily read
        return {"status": "success", "game_name": game_name, "steam_id": game_id, "message": f"Game called {game_name} with the id {game_id} has tried to start uninstalling."}
        
    except pyautogui.ImageNotFoundException:
        return {"status": "error", "game_name": game_name, "steam_id": game_id, "message": f"Game called {game_name} with the id {game_id} has tried to start uninstalling but the uninstall button was not found."}

@app.get("/screenshot")
def capture_screen():
    try:
        img = pyautogui.screenshot()
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        return StreamingResponse(img_buffer, media_type="image/png")
        
    except Exception:
        return {"status": "error", "message": f"Failed to take screenshot: {str(Exception)}"}