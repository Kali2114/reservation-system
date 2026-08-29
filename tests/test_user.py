from user import User


def test_user_id_increases():
    user1 = User("test_name1", "test_email1", password="test_password1", salt="test_salt1")
    user2 = User("test_name2", "test_email2", password="test_password2", salt="test_salt2")
    assert user2.id > user1.id