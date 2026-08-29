import pytest

from user_store import UserStore


class TestUserStore:

    def setup_method(self):
        self.user_store = UserStore()

    def test_register_success(self):
        payload = {
            "name": "test_name",
            "email": "test_email",
            "password": "test_password",
        }
        user = self.user_store.register(**payload)
        assert user is self.user_store.users["test_email"]
        assert len(self.user_store.users) == 1

    def test_register_email_already_exists(self):
        payload = {
            "name": "test_name",
            "email": "test_email",
            "password": "test_password",
        }
        self.user_store.register(**payload)
        with pytest.raises(ValueError):
            self.user_store.register(**payload)

    def test_register_stores_hashed_password(self):
        user = self.user_store.register(
            name="test_name",
            email="test_email",
            password="secret",
        )

        assert user.password_hash != "secret"
        assert isinstance(user.password_hash, bytes)

    def test_register_two_same_password(self):
        user1 = self.user_store.register(
            name="test_name",
            email="test_email1",
            password="secret",
        )
        user2 = self.user_store.register(
            name="test_name",
            email="test_email2",
            password="secret",
        )
        assert user1.password_hash != user2.password_hash
        assert user1.salt != user2.salt

    def test_login_success(self):
        user = self.user_store.register(
            name="test_name",
            email="test_email",
            password="test_password",
        )
        assert self.user_store.login(user.email, "test_password") is user
        assert self.user_store.users[user.email] is user

    def test_login_incorrect_password(self):
        user = self.user_store.register(
            name="test_name",
            email="test_email",
            password="test_password",
        )
        with pytest.raises(ValueError):
            self.user_store.login(user.email, "wrong_password")

    def test_login_no_exist_email(self):
        with pytest.raises(ValueError):
            self.user_store.login("wrong_email", "wrong_password")

