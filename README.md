# Inventory Manager

A minimalist Python application for tracking daily inventory, calculating sales averages, and generating AI-driven business insights. It features both a fast terminal dashboard and a modern web interface for managing your reports.

## Features
* **Terminal Dashboard:** Quick, text-based menus for recording daily inventory and viewing specific days.
* **Web API & Frontend:** A FastAPI-powered web interface to view and batch-download reports as ZIP files.
* **AI Consultant:** Uses the new `google-genai` library (gemini-2.5-flash) to analyze your sales data and provide actionable business advice.
* **Data Visualization:** Automated text-based sell-through charts in the terminal.

## Project Structure
* `launcher.py` - The main gate. Run this to choose between the Terminal Menu or the Web Server.
* `get.py` - The core terminal menu logic.
* `api.py` - The FastAPI web server and API routes.
* `data/` - Contains the logic modules (`getdata`, `report`, `average`, `insight`, `visualizer`) and the `entries/` folder for your JSON records.
* `webpage/` - Contains the minimalist `index.html` frontend.
* `install.bat` / `requirements.txt` - Quick setup scripts to install dependencies.
* `.env` - Secure storage for your API keys.

## Setup Instructions
1. Run `install.bat` (or manually run `pip install -r requirements.txt`) to install FastAPI, Uvicorn, Dotenv, and the Gemini SDK.
2. Create a `.env` file in the main folder and add your Gemini key:
   `GEMINI_API_KEY=your_actual_key_here`
3. Run `python launcher.py` to start the application.

## Usage
* **Option 1 (Terminal):** Use this to log your daily sales, crunch weekly averages, or ask the AI to analyze your performance.
* **Option 2 (Web Server):** Use this to open a clean web dashboard where you can easily view or mass-download your inventory records.
