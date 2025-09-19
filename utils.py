import hashlib
import secrets

def hash_password(password: str) -> str:
    """Hashes a password with a salt."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a stored password against one provided by the user."""
    try:
        salt, pwd_hash = stored_password.split('$')
        return pwd_hash == hashlib.sha256((provided_password + salt).encode('utf-8')).hexdigest()
    except (ValueError, IndexError):
        hashlib.sha256(secrets.token_bytes(32)).hexdigest()
        return False