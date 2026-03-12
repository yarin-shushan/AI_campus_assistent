from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session, select
import passlib.context
import os

from database import engine
import app.models as models 
from app.models import User, Student, Lecturer, Building, Classroom, Course, Exam, TechnicalFAQ
from datetime import date, time

# הגדרות הצפנת סיסמה
pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_data():
    with Session(engine) as session:
        try:
            # בדיקה אם המשתמש כבר קיים כדי לא ליצור כפילויות
            statement = select(User).where(User.email == "admin@afeka.ac.il")
            existing_user = session.exec(statement).first()
            
            if existing_user:
                print("--- DATABASE CHECK: Admin user already exists. Skipping seed. ---")
                return

            print("--- SEEDING PROCESS: Starting to seed initial Afeka data... ---")
            
            # 1. Students
            s1 = Student(full_name="Yarin Shushan", identity_number="123456789", department="Software Engineering")
            session.add(s1)
            session.commit()
            session.refresh(s1)

            # 2. Admin & Student Users
            admin_user = User(
                email="admin@afeka.ac.il", 
                hashed_password=get_password_hash("AdminPass123!"), 
                role="admin"
            )
            student_user = User(
                email="yarin@afeka.ac.il", 
                hashed_password=get_password_hash("StudentPass123!"), 
                role="student",
                student_id=s1.id
            )
            
            # 3. FAQs / Events
            faq1 = TechnicalFAQ(
                issue="Student Union Marathon for Calculus", 
                solution="Join us on Thursday at 18:00 in Mitchell 201 for a complete review of Calculus 1!"
            )
            
            session.add_all([admin_user, student_user, faq1])
            session.commit()
            print("--- SEEDING PROCESS: Completed successfully! ---")
            
        except Exception as e:
            print(f"--- SEEDING ERROR: Failed to seed data. Error: {e} ---")
            session.rollback()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- STARTUP: Connecting to RDS and creating tables... ---")
    try:
        # יצירת הטבלאות ב-Public Schema שאיפסנו
        SQLModel.metadata.create_all(engine)
        print("--- STARTUP: Tables created/verified. ---")
        seed_data()
    except Exception as e:
        print(f"--- STARTUP ERROR: Database connection failed: {e} ---")
    
    yield
    print("--- SHUTDOWN: Cleaning up resources... ---")

app = FastAPI(title="Smart Campus Assistant", lifespan=lifespan)

# הגדרות CORS מתוקנות - מפורשות עבור