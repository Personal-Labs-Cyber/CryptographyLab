import hashlib
import bcrypt
import time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def hash_sha256(password):
    """Computes SHA-256 (Fast, weak for passwords)."""
    start = time.perf_counter()
    digest = hashlib.sha256(password.encode('utf-8')).hexdigest()
    end = time.perf_counter()
    return digest, (end - start) * 1000  # ms

def hash_pbkdf2(password, salt_hex, iterations=100000):
    """Computes PBKDF2 (Slower, better for passwords)."""
    import os
    if not salt_hex:
        # Use a cryptographically secure random salt if none provided
        salt = os.urandom(16)
    else:
        try:
            salt = bytes.fromhex(salt_hex)
        except ValueError:
            salt = salt_hex.encode('utf-8')
            
    start = time.perf_counter()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    digest = base64.b64encode(key).decode('utf-8')
    end = time.perf_counter()
    return digest, (end - start) * 1000 # ms

def hash_bcrypt(password, rounds=12):
    """Computes bcrypt (Slow, standard for passwords). Includes own salt."""
    start = time.perf_counter()
    # bcrypt requires bytes, returns bytes
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    digest = hashed.decode('utf-8')
    end = time.perf_counter()
    return digest, (end - start) * 1000 # ms
