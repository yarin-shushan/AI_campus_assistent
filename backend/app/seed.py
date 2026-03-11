import os
from datetime import date, time
from sqlmodel import Session, create_engine
import passlib.context
from app.models import Student, User, Lecturer, Building, Classroom, Course, Exam, TechnicalFAQ

# Context for hashing passwords
pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/smart_campus")
engine = create_engine(DATABASE_URL)

def seed():
    with Session(engine) as session:
        # Check if users already exist to avoid duplicates on multiple runs
        existing_user = session.query(User).filter(User.email == "admin@afeka.ac.il").first()
        if existing_user:
            print("Database already seeded.")
            return

        # 1. Students
        s1 = Student(full_name="Yarin Shushan", identity_number="123456789", department="Software Engineering")
        s2 = Student(full_name="Noa Cohen", identity_number="987654321", department="Electrical Engineering")
        session.add_all([s1, s2])
        session.commit()
        session.refresh(s1)
        session.refresh(s2)

        # 2. Users (Admin and regular student)
        # Admin User (Not tied to a student profile, acts as Student Union Chairman)
        admin_user = User(
            email="admin@afeka.ac.il", 
            hashed_password=get_password_hash("AdminPass123!"), 
            role="admin"
        )
        
        # Regular Student User
        student_user = User(
            email="yarin@afeka.ac.il", 
            hashed_password=get_password_hash("StudentPass123!"), 
            role="student",
            student_id=s1.id
        )
        session.add_all([admin_user, student_user])

        # 3. Lecturers
        l1 = Lecturer(
            full_name="Dr. Eyal Cohen", 
            identity_number="556677889", 
            department="Software Engineering", 
            reception_day="Monday", 
            reception_hours="10:00-12:00", 
            location="Ficus 101"
        )
        l2 = Lecturer(
            full_name="Prof. Yaron Katz", 
            identity_number="998877665", 
            department="Electrical Engineering", 
            reception_day="Wednesday", 
            reception_hours="14:00-16:00", 
            location="Mitchell 202"
        )
        session.add_all([l1, l2])
        session.commit()
        session.refresh(l1)
        session.refresh(l2)
        
        # Link lecturers to user accounts
        lecturer_user1 = User(
            email="eyal@afeka.ac.il",
            hashed_password=get_password_hash("LecturerPass123!"),
            role="lecturer",
            lecturer_id=l1.id
        )
        session.add(lecturer_user1)

        # 4. Buildings
        b1 = Building(name="Ficus", total_rooms=40, description="Main Software Engineering Building")
        b2 = Building(name="Mitchell", total_rooms=30, description="Innovation and Electrical Engineering Laboratories")
        session.add_all([b1, b2])

        # 5. Classrooms
        c1 = Classroom(building_name="Ficus", room_number="101", availability_schedule="Sun-Thu 08:00-16:00")
        c2 = Classroom(building_name="Ficus", room_number="102", availability_schedule="Sun-Thu 10:00-18:00")
        c3 = Classroom(building_name="Mitchell", room_number="201", availability_schedule="Sun-Wed 08:00-14:00")
        session.add_all([c1, c2, c3])

        # 6. Courses
        crs1 = Course(course_name="Data Structures", course_code="SE201")
        crs2 = Course(course_name="C Programming", course_code="SE101")
        crs3 = Course(course_name="Python Applications", course_code="SE305")
        session.add_all([crs1, crs2, crs3])

        # 7. Exams
        e1 = Exam(course_name="Data Structures", classroom_name="Ficus 101", date=date(2026, 6, 15), hours=time(9, 0))
        e2 = Exam(course_name="C Programming", classroom_name="Ficus 102", date=date(2026, 6, 20), hours=time(14, 0))
        e3 = Exam(course_name="Python Applications", classroom_name="Mitchell 201", date=date(2026, 7, 5), hours=time(10, 30))
        session.add_all([e1, e2, e3])

        # 8. TechnicalFAQs & Events
        faq1 = TechnicalFAQ(issue="Student Union Marathon for Calculus", solution="Join us on Thursday at 18:00 in Mitchell 201 for a complete review of Calculus 1! Free pizza provided.")
        faq2 = TechnicalFAQ(issue="How to connect to the campus VPN", solution="Download the FortiClient VPN software from the Afeka portal. Use address 'vpn.afeka.ac.il' and login with your student credentials.")
        faq3 = TechnicalFAQ(issue="Moodle login fails", solution="Reset password via Afeka portal or contact IT via email.")
        session.add_all([faq1, faq2, faq3])

        session.commit()
        print("Database seeded completely with Afeka College data!")

if __name__ == "__main__":
    seed()
