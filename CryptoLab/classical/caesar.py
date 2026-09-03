def encrypt(text, key):
    """Encrypts text using the Caesar cipher."""
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + key) % 26 + 65)
        else:
            result += char
    return result

def decrypt(cipher, key):
    """Decrypts text using the Caesar cipher."""
    return encrypt(cipher, -key)

def show_steps(text, key):
    """Shows step-by-step breakdown of Caesar encryption."""
    print(f"\n[bold blue]Plaintext:[/bold blue] {text}")
    print(f"[bold blue]Key:[/bold blue] {key}")
    
    print("\n[bold]Step 1: Convert letters to numbers (A=0, B=1...)[/bold]")
    step1 = [f"{char}={ord(char)-65}" for char in text.upper() if char.isalpha()]
    print(" → ".join(step1[:10]) + ("..." if len(step1) > 10 else ""))
    
    print("\n[bold]Step 2: Add key and apply Modulo 26[/bold]")
    step2 = [f"({ord(char)-65}+{key})%26 = {(ord(char)-65+key)%26}" for char in text.upper() if char.isalpha()]
    print(" → ".join(step2[:5]) + ("..." if len(step2) > 5 else ""))
    
    print("\n[bold]Step 3: Convert back to letters[/bold]")
    print(f"[bold green]Ciphertext:[/bold green] {encrypt(text, key)}\n")

def show_strengths_weaknesses():
    """Prints strengths and weaknesses of the Caesar cipher."""
    print("\n[bold green]Strengths:[/bold green]")
    print("- Extremely simple to implement")
    print("- Good for learning basic modular arithmetic")
    
    print("\n[bold red]Weaknesses:[/bold red]")
    print("- Very small keyspace (only 25 possible keys, easy to brute force)")
    print("- Vulnerable to frequency analysis (letter distribution is preserved)")
    print("- A known-plaintext attack of just one letter reveals the key\n")
