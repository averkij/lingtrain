from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auth_service import hash_password


def add_test_users(db: Session) -> None:
    test_users = [
        {
            "username": "admin",
            "email": "admin@lingtrain.local",
            "password": "adminadmin777",
            "role": "admin",
            "display_name": "Admin User",
        },
        {
            "username": "test",
            "email": "test@lingtrain.local",
            "password": "testtest777",
            "role": "user",
            "display_name": "Test User",
        },
        {
            "username": "googleuser",
            "email": "googleuser@gmail.com",
            "password": None,
            "role": "user",
            "auth_provider": "google",
            "provider_id": "google_117000000000000000001",
            "display_name": "Google User",
        },
    ]

    for data in test_users:
        exists = db.query(User).filter(User.username == data["username"]).first()
        if exists:
            continue
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=hash_password(data["password"]) if data["password"] else None,
            role=data["role"],
            auth_provider=data.get("auth_provider", "local"),
            provider_id=data.get("provider_id"),
            display_name=data.get("display_name"),
            is_active=True,
            is_email_verified=True,
        )
        db.add(user)

    db.commit()
