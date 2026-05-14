import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# This is the magic line that actually reads your .env file!
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY", "")

DATA_DIR = "data/entries"
AVERAGE_REPORT = os.path.join(DATA_DIR, "average_report.json")
INSIGHT_REPORT = os.path.join(DATA_DIR, "insight_report.json")

PROMPT_TEMPLATE = """
You are an expert business consultant. Analyse the average daily sales data below.
Focus on sell-through rates and waste.

Data:
{data}

Return ONLY a valid JSON object in this exact format (no extra text or markdown):
{{
    "summary": "A 2-sentence overall evaluation of the business's performance.",
    "alerts": [
        {{"product": "Item Name", "message": "Why production should be reduced for this item."}}
    ],
    "good_performers": [
        {{"product": "Item Name", "message": "Why this item is doing well and what to do next."}}
    ]
}}

Rules:
- Only add an item to "alerts" if it has notably high waste (low sell-through).
- Only add an item to "good_performers" if it sells out almost completely.
- If no items fit a category, leave the list empty [].
"""

def load_average_data():
    if not os.path.exists(AVERAGE_REPORT):
        print("No average data found. Run the Average tool first.")
        return None
    with open(AVERAGE_REPORT, "r") as f:
        return json.load(f)["averages"]

def generate_insights():
    print("\n" + "═" * 45)
    print("Generating AI Insights...")
    print("═" * 45)

    if not API_KEY:
        print("GEMINI_API_KEY environment variable is not set.")
        print("Make sure your .env file is in the same folder as your main script.")
        return

    averages = load_average_data()
    if averages is None:
        return

    # Initialize the new genai client
    client = genai.Client(api_key=API_KEY)

    prompt = PROMPT_TEMPLATE.format(data=json.dumps(averages, indent=2))

    try:
        # The new syntax for calling the model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        ai_insights = json.loads(response.text)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(INSIGHT_REPORT, "w") as f:
            json.dump(ai_insights, f, indent=4)

        print(f"\nAI analysis complete!")
        print(f"Insights saved to: {INSIGHT_REPORT}")
        
        # Print a quick preview
        print("\n─── AI SUMMARY ───")
        print(ai_insights.get("summary", "No summary provided."))

    except Exception as e:
        print(f"\n❌ Error contacting AI: {e}")

if __name__ == "__main__":
    generate_insights()