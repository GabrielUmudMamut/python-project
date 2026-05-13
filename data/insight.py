import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# Load your API key from an environment variable.
# Set it with: export GEMINI_API_KEY="your_key_here"
# Or create a .env file and use the `python-dotenv` package.
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
- If no items qualify for a category, return an empty list for it.
"""


def load_average_data() -> list | None:
    """Loads the average report. Returns None if it doesn't exist."""
    if not os.path.exists(AVERAGE_REPORT):
        print("❌ No average data found. Run the Average tool first.")
        return None
    with open(AVERAGE_REPORT, "r") as f:
        return json.load(f)["averages"]


def generate_insights():
    print("\n" + "═" * 45)
    print("      🤖  CALLING AI CONSULTANT...")
    print("═" * 45)

    if not API_KEY:
        print("❌ GEMINI_API_KEY environment variable is not set.")
        print("   Set it with: export GEMINI_API_KEY='your_key_here'")
        return

    averages = load_average_data()
    if averages is None:
        return

    genai.configure(api_key=API_KEY)

    prompt = PROMPT_TEMPLATE.format(data=json.dumps(averages, indent=2))

    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config={"response_mime_type": "application/json"},
        )
        response = model.generate_content(prompt)
        ai_insights = json.loads(response.text)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(INSIGHT_REPORT, "w") as f:
            json.dump(ai_insights, f, indent=4)

        print(f"\n✅ AI analysis complete!")
        print(f"   Summary: {ai_insights.get('summary', 'N/A')}")
        print(f"   Saved to {INSIGHT_REPORT}. Refresh your web dashboard!")

    except json.JSONDecodeError:
        print("❌ The AI returned an unexpected format. Please try again.")
    except Exception as e:
        print(f"❌ Something went wrong: {e}")


if __name__ == "__main__":
    generate_insights()
