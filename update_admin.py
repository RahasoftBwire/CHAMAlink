from app import create_app, db
from app.models import User
from sqlalchemy import text

app = create_app()
with app.app_context():
    # Update the first user to admin
    result = db.session.execute(
        text("UPDATE users SET role='admin', is_email_verified=True WHERE email=:email"),
        {"email": "bilfordderek917@gmail.com"}
    )
    db.session.commit()
    
    # Verify the update
    user_result = db.session.execute(
        text("SELECT id, email, role, is_email_verified FROM users WHERE email=:email"),
        {"email": "bilfordderek917@gmail.com"}
    )
    user = user_result.first()
    
    print("✅ User updated successfully!")
    print(f"   Email: {user[1]}")
    print(f"   Role: {user[2]}")
    print(f"   Email Verified: {user[3]}")
