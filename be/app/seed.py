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
        },
        {
            "username": "test",
            "email": "test@lingtrain.local",
            "password": "testtest777",
            "role": "user",
        },
    ]

    for data in test_users:
        exists = db.query(User).filter(User.username == data["username"]).first()
        if exists:
            continue
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=hash_password(data["password"]),
            role=data["role"],
            is_active=True,
            is_email_verified=True,
        )
        db.add(user)

    db.commit()
