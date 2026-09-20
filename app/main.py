# In app/main.py

# Replace the top-level Base.metadata.create_all and seed function with:
@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        # Safe seed check
        admin_exists = db.query(User).filter(User.email == "admin@eventsystem.com").first()
        if not admin_exists:
            from .auth import hash_password
            admin = User(
                name="Admin User",
                email="admin@eventsystem.com",
                password_hash=hash_password("password123"),
                role="ADMIN"
            )
            db.add(admin)
            db.commit()
        db.close()
    except Exception as e:
        print(f"Startup warning/error: {e}")
