from user import User


def test_user_id_increases():
    user1 = User("test_name1", "test_email1", password_hash="test_hash1", salt="test_salt1")
    user2 = User("test_name2", "test_email2", password_hash="test_hash2", salt="test_salt2")
    assert user2.id > user1.id