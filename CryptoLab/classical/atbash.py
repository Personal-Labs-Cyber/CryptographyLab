def encrypt(text):
    """Encrypts text using the Atbash cipher."""
    result = ""
    for char in text.upper():
        if char.isalpha():
            # A (65) maps to Z (90), B (66) maps to Y (89)
            # Formula: 90 - (ord(char) - 65)
            result += chr(155 - ord(char))
        else:
            result += char
    return result

def decrypt(cipher):
    """Decrypts text using the Atbash cipher. (Same as encryption)"""
    return encrypt(cipher)

def show_steps(text):
    """Shows step-by-step breakdown of Atbash encryption."""
    print(f"\n[bold blue]Plaintext:[/bold blue] {text}")
    
    print("\n[bold]Step 1: Map each letter to its reverse alphabet counterpart (A<->Z, B<->Y...)[/bold]")
    step1 = [f"{char} <-> {chr(155 - ord(char))}" for char in text.upper() if char.isalpha()]
    print(" → ".join(step1[:10]) + ("..." if len(step1) > 10 else ""))
    
    print("\n[bold]Step 2: Replace letters[/bold]")
    print(f"[bold green]Ciphertext:[/bold green] {encrypt(text)}\n")

def show_strengths_weaknesses():
    """Prints strengths and weaknesses of the Atbash cipher."""
    print("\n[bold green]Strengths:[/bold green]")
    print("- Extremely simple to implement")
    print("- Does not require a key to remember")
    
    print("\n[bold red]Weaknesses:[/bold red]")
    print("- Zero security (no key, anyone who knows it's Atbash can read it)")
    print("- Vulnerable to frequency analysis (E maps to V, T maps to G, etc.)\n")
