from backend.database.session import SessionLocal, engine, Base
from backend.models.user import User
from backend.models.course import Course, Department
from backend.auth.jwt_handler import hash_password

DEPARTMENTS = [
    "AI & Data Science", "Python Development", "Web Development",
    "Game Development", "Cyber Security", "Software Architecture",
    "Graphic Designing & Video Editing", "English Language", "Arabic Language",
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@ait.edu").first():
            db.add(User(email="admin@ait.edu", full_name="AiT Super Admin",
                        password_hash=hash_password("admin123"), role="super_admin"))
        if not db.query(Department).first():
            for d in DEPARTMENTS:
                code = "".join([w[0] for w in d.split()][:3]).upper()
                db.add(Department(name=d, code=code))
        if not db.query(Course).first():
            db.add(Course(department="Foundation", level="IT Level 0",
                          title="Computer & Digital Literacy Foundation", duration_months=6, fee=8000))
            for d in DEPARTMENTS:
                for lvl in ["Level 1", "Level 2", "Level 3"]:
                    db.add(Course(department=d, level=lvl, title=f"{d} - {lvl}",
                                  duration_months=6, fee=15000))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Database seeded.")