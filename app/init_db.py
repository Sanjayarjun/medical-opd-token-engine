from app.core.database import engine, Base
from app.models import entities  # important: import models so Base knows tables


def init():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


if __name__ == "__main__":
    init()
