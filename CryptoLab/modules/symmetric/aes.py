import os
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def generate_key_iv():
    """Generates a 32-byte (256-bit) key and 16-byte IV for AES."""
    key = os.urandom(32)
    iv = os.urandom(16)
    return binascii.hexlify(key).decode('utf-8'), binascii.hexlify(iv).decode('utf-8')

def pad_data(data):
    """Pads data to 16-byte boundary for AES block size."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def unpad_data(data):
    """Unpads data."""
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def blockify(hex_data):
    """Splits a hex string into a list of 16-byte (32 hex char) blocks for visualization."""
    return [hex_data[i:i+32] for i in range(0, len(hex_data), 32)]

def encrypt_aes(text, key_hex, mode_str, iv_hex=None):
    """Encrypts text using AES in ECB or CBC mode."""
    key = binascii.unhexlify(key_hex)
    
    if mode_str.upper() == 'ECB':
        mode = modes.ECB()
    elif mode_str.upper() == 'CBC':
        if not iv_hex:
            raise ValueError("CBC mode requires an IV")
        iv = binascii.unhexlify(iv_hex)
        mode = modes.CBC(iv)
    else:
        raise ValueError("Unsupported mode")

    cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
    encryptor = cipher.encryptor()
    
    padded_data = pad_data(text.encode('utf-8'))
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    ct_hex = binascii.hexlify(ciphertext).decode('utf-8')
    pt_hex = binascii.hexlify(padded_data).decode('utf-8')
    
    return {
        'ciphertext': ct_hex,
        'blocks': blockify(ct_hex),
        'plaintext_blocks': blockify(pt_hex)
    }

def decrypt_aes(ciphertext_hex, key_hex, mode_str, iv_hex=None):
    """Decrypts AES ciphertext."""
    key = binascii.unhexlify(key_hex)
    ciphertext = binascii.unhexlify(ciphertext_hex)
    
    if mode_str.upper() == 'ECB':
        mode = modes.ECB()
    elif mode_str.upper() == 'CBC':
        if not iv_hex:
            raise ValueError("CBC mode requires an IV")
        iv = binascii.unhexlify(iv_hex)
        mode = modes.CBC(iv)
    else:
        raise ValueError("Unsupported mode")

    cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpad_data(padded_data)
    
    return plaintext.decode('utf-8')
