import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305, AESGCM
from cryptography.hazmat.backends import default_backend

def pad(text, block_size):
    """PKCS7 padding"""
    padding_len = block_size - (len(text) % block_size)
    return text + (chr(padding_len) * padding_len)

def process_aes_ecb(text, key_hex, encrypt=True):
    key = bytes.fromhex(key_hex)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    
    if encrypt:
        encryptor = cipher.encryptor()
        padded = pad(text, 16).encode('utf-8')
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode('utf-8')
    else:
        # Simplification for demo
        return "Decryption not implemented for ECB demo"

def process_aes_gcm(text, key_hex, encrypt=True):
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    if encrypt:
        ciphertext = aesgcm.encrypt(nonce, text.encode('utf-8'), b"demo_aad")
        # Prepend nonce to ciphertext for demo purposes
        combined = nonce + ciphertext
        return base64.b64encode(combined).decode('utf-8')
    else:
        return "Decryption not implemented for GCM demo"

def process_chacha20(text, key_hex, encrypt=True):
    key = bytes.fromhex(key_hex)
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    
    if encrypt:
        ciphertext = chacha.encrypt(nonce, text.encode('utf-8'), b"demo_aad")
        combined = nonce + ciphertext
        return base64.b64encode(combined).decode('utf-8')
    else:
        return "Decryption not implemented for ChaCha demo"

def process_3des(text, key_hex, encrypt=True):
    key = bytes.fromhex(key_hex)[:24] # 3DES uses 192 bits (24 bytes)
    # Generate random IV for CBC
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    
    if encrypt:
        encryptor = cipher.encryptor()
        padded = pad(text, 8).encode('utf-8')
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        combined = iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')
    else:
        return "Decryption not implemented for 3DES demo"
