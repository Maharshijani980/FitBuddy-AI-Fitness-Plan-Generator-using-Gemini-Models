import os
from google import genai


def generate_updated_plan(original_plan: str, feedback: str) -> str:

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Here is an existing 7-day workout plan:

    {original_plan}

    The user has provided the following feedback to improve the plan:
    "{feedback}"

    Please revise the workout plan based on this feedback.
    Keep the same day-by-day format with Warm-up, Main Workout, and Cooldown sections.
    Incorporate the user's requested changes while maintaining the overall structure and fitness goal.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text
