import os
from google import genai


def generate_workout_gemini(goal: str, intensity: str) -> str:

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Create a detailed 7-day personalized workout plan for someone with the following profile:
    - Fitness Goal: {goal}
    - Workout Intensity: {intensity}

    Format each day exactly like this:
    Day X
    Warm-up: ...
    Main Workout: ... (include exercises, sets, and reps)
    Cooldown: ...

    Make intensity appropriate:
    - Low: beginner-friendly, lighter weights, shorter sessions
    - Medium: intermediate level, moderate weights
    - High: advanced, challenging, heavier weights and more volume

    Be specific with exercises, sets, reps, and rest times.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text
