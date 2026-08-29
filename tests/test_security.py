import security


def test_verify_password_pass():
    password = "test_password"
    salt, hashed_password = security.hash_password(password)
    assert security.verify_password(password, salt, hashed_password) is True


def test_verify_password_fail():
    password = "test_password"
    salt, hashed_password = security.hash_password(password)
    assert security.verify_password("wrong_password", salt, hashed_password) is False


def test_hash_password_pass():
    password = "test_password"
    salt, hashed_password = security.hash_password(password)
    other_salt, other_hashed_password = security.hash_password(password)
    assert salt != other_salt
    assert hashed_password != other_hashed_password
