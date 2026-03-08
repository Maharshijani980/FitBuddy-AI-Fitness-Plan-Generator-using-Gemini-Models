from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db, save_user, save_plan, update_plan, get_original_plan, get_user
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import generate_updated_plan

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Home Page
# -----------------------------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -----------------------------
# Generate Workout Plan
# -----------------------------

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
        request: Request,
        username: str = Form(...),
        age: int = Form(...),
        weight: int = Form(...),
        goal: str = Form(...),
        intensity: str = Form(...),
        db: Session = Depends(get_db)
):

    # save user
    user = save_user(db, username, age, weight, goal, intensity)

    # generate plan using Gemini Pro
    plan = generate_workout_gemini(goal, intensity)

    # generate nutrition tip using Gemini Flash
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # store plan in DB
    save_plan(db, user.id, plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": username,
            "user_id": user.id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip,
            "updated_plan": None
        }
    )


# -----------------------------
# Submit Feedback & Update Plan
# -----------------------------

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
        request: Request,
        user_id: int = Form(...),
        feedback: str = Form(...),
        db: Session = Depends(get_db)
):

    # get original plan from DB
    original_plan = get_original_plan(db, user_id)

    # generate updated plan using Gemini Flash
    new_plan = generate_updated_plan(original_plan, feedback)

    # save updated plan to DB
    update_plan(db, user_id, new_plan)

    # get user details for rendering
    user = get_user(db, user_id)

    # get fresh nutrition tip
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": user.name,
            "user_id": user.id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": original_plan,
            "nutrition_tip": nutrition_tip,
            "updated_plan": new_plan
        }
    )


# -----------------------------
# Admin Dashboard
# -----------------------------

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):

    from app.database import get_all_users

    users = get_all_users(db)

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users
        }
    )
