from utils.math_helpers import modinv
import math

def encrypt(text, keys):
    """Encrypts text using Affine cipher. keys is a tuple (a, b)."""
    a, b = keys
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime with 26.")
        
    result = ""
    for char in text.upper():
        if char.isalpha():
            # E(x) = (ax + b) mod 26
            x = ord(char) - 65
            result += chr(((a * x + b) % 26) + 65)
        else:
            result += char
    return result

def decrypt(cipher, keys):
    """Decrypts text using Affine cipher."""
    a, b = keys
    a_inv = modinv(a, 26)
    
    result = ""
    for char in cipher.upper():
        if char.isalpha():
            # D(x) = a^-1(x - b) mod 26
            y = ord(char) - 65
            result += chr(((a_inv * (y - b)) % 26) + 65)
        else:
            result += char
    return result

def show_steps(text, keys):
    a, b = keys
    print(f"\n[bold blue]Plaintext:[/bold blue] {text}")
    print(f"[bold blue]Key:[/bold blue] a={a}, b={b}")
    
    print("\n[bold]Step 1: Convert to numbers (A=0, B=1...)[/bold]")
    print("\n[bold]Step 2: Apply formula E(x) = (ax + b) mod 26[/bold]")
    steps = []
    for char in text.upper():
        if char.isalpha():
            x = ord(char) - 65
            val = (a * x + b) % 26
            steps.append(f"{char}({x}) -> ({a}*{x}+{b})%26 = {val} -> {chr(val+65)}")
    print(" | ".join(steps[:4]) + (" | ..." if len(steps) > 4 else ""))
    
    print(f"\n[bold green]Ciphertext:[/bold green] {encrypt(text, keys)}\n")

def show_strengths_weaknesses():
    print("\n[bold green]Strengths:[/bold green]")
    print("- Combines multiplication (decimation) and addition (shift)")
    
    print("\n[bold red]Weaknesses:[/bold red]")
    print("- Very small keyspace (only 12 valid 'a' values * 26 'b' values = 312 keys)")
    print("- Vulnerable to frequency analysis and known-plaintext attacks\n")
