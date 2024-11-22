import pytest
import os
from app.db import User, Expense, db
from werkzeug.security import generate_password_hash

from app import create_app


@pytest.fixture(scope="module")
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def new_user():
    return User(username="john_doe", password="strong_password")


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()

    first_user = User(
        username="Mary",
        password=generate_password_hash("strong_password", method="pbkdf2"),
    )

    second_user = User(
        username="Patrik",
        password=generate_password_hash("strong_password", method="pbkdf2"),
    )
    db.session.add(first_user)
    db.session.add(second_user)
    db.session.commit()

    expense_1 = Expense(title="Expense_1", amount=5, user_id=first_user.id)
    expense_2 = Expense(title="Expense_2", amount=15, user_id=first_user.id)
    expense_3 = Expense(title="Expense_3", amount=20, user_id=first_user.id)
    db.session.add_all([expense_1, expense_2, expense_3])
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="module")
def first_user_token(test_client):
    respose = test_client.post(
        "/users/login", json={"username": "Mary", "password": "strong_password"}
    )

    yield respose.json["access_token"]


@pytest.fixture(scope="module")
def second_user_token(test_client):
    respose = test_client.post(
        "/users/login", json={"username": "Patrik", "password": "strong_password"}
    )

    yield respose.json["access_token"]
