from app.gemini_generator import generate_workout_gemini

plan = generate_workout_gemini("muscle gain", "high")

print(plan)