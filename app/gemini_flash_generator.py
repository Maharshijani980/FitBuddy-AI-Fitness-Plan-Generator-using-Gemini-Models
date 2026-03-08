import os
from google import genai


def generate_nutrition_tip_with_flash(goal: str) -> str:

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Give a short, practical nutrition tip (2-3 sentences) for someone whose fitness goal is: {goal}.
    Make it specific, actionable, and science-backed.
    Avoid generic advice — tailor it directly to the goal.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text
