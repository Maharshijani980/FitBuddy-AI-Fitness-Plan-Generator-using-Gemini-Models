from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# SQLite database file
DATABASE_URL = "sqlite:///./fitbuddy.db"

# Create engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()


# -------------------------
# User Table
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Integer)
    goal = Column(String)
    intensity = Column(String)

    workout_plans = relationship("WorkoutPlan", back_populates="user")


# -------------------------
# Workout Plan Table
# -------------------------

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    original_plan = Column(Text)

    updated_plan = Column(Text, nullable=True)

    user = relationship("User", back_populates="workout_plans")


# -------------------------
# Create Tables
# -------------------------

def create_tables():
    Base.metadata.create_all(bind=engine)


# -------------------------
# Database Utility Functions
# -------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Save User
# -------------------------

def save_user(db, name, age, weight, goal, intensity):
    user = User(
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# -------------------------
# Save Workout Plan
# -------------------------

def save_plan(db, user_id, original_plan):

    plan = WorkoutPlan(
        user_id=user_id,
        original_plan=original_plan
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


# -------------------------
# Update Workout Plan
# -------------------------

def update_plan(db, user_id, updated_plan):

    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id
    ).first()

    if plan:
        plan.updated_plan = updated_plan
        db.commit()
        db.refresh(plan)

    return plan


# -------------------------
# Get Original Plan
# -------------------------

def get_original_plan(db, user_id):

    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id
    ).first()

    if plan:
        return plan.original_plan

    return None


# -------------------------
# Get User
# -------------------------

def get_user(db, user_id):

    return db.query(User).filter(User.id == user_id).first()


# -------------------------
# Get All Users
# -------------------------

def get_all_users(db):

    users = db.query(User).all()

    return users
