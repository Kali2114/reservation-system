import hashlib
import hmac
import os


def _derive(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000
    )


def hash_password(password):
    salt = os.urandom(16)
    password_hash = _derive(password, salt)
    return salt, password_hash


def verify_password(password, salt, expected_hash):
    password_hash = _derive(password, salt)
    return hmac.compare_digest(password_hash, expected_hash)

