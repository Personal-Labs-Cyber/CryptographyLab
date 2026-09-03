def _generate_key(text, key):
    """Generates the key in a cyclic manner until it matches the length of the text."""
    key = list(key.upper())
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "" . join(key)

def encrypt(text, key):
    """Encrypts text using the Vigenère cipher."""
    text = text.upper()
    key_stream = _generate_key(text, key)
    result = ""
    key_idx = 0
    for char in text:
        if char.isalpha():
            # E_i = (P_i + K_i) mod 26
            shift = ord(key_stream[key_idx]) - 65
            result += chr((ord(char) - 65 + shift) % 26 + 65)
            key_idx += 1
        else:
            result += char
    return result

def decrypt(cipher, key):
    """Decrypts text using the Vigenère cipher."""
    cipher = cipher.upper()
    key_stream = _generate_key(cipher, key)
    result = ""
    key_idx = 0
    for char in cipher:
        if char.isalpha():
            # P_i = (E_i - K_i) mod 26
            shift = ord(key_stream[key_idx]) - 65
            result += chr((ord(char) - 65 - shift + 26) % 26 + 65)
            key_idx += 1
        else:
            result += char
    return result

def show_steps(text, key):
    """Shows step-by-step breakdown of Vigenère encryption."""
    print(f"\n[bold blue]Plaintext:[/bold blue] {text}")
    print(f"[bold blue]Key:[/bold blue] {key}")
    
    text_clean = "".join([c for c in text.upper() if c.isalpha()])
    key_stream = _generate_key(text_clean, key)
    
    print(f"\n[bold]Step 1: Repeat key to match plaintext length[/bold]")
    print(f"Plaintext (letters only): {text_clean}")
    print(f"Key stream:               {key_stream}")
    
    print("\n[bold]Step 2: Add character values modulo 26 (A=0, B=1...)[/bold]")
    steps = []
    for i in range(min(5, len(text_clean))):
        p_val = ord(text_clean[i]) - 65
        k_val = ord(key_stream[i]) - 65
        c_val = (p_val + k_val) % 26
        steps.append(f"({text_clean[i]}={p_val} + {key_stream[i]}={k_val})%26 = {chr(c_val+65)}")
    print(" → ".join(steps) + ("..." if len(text_clean) > 5 else ""))
    
    print("\n[bold]Step 3: Convert back to letters[/bold]")
    print(f"[bold green]Ciphertext:[/bold green] {encrypt(text, key)}\n")

def show_strengths_weaknesses():
    """Prints strengths and weaknesses of the Vigenère cipher."""
    print("\n[bold green]Strengths:[/bold green]")
    print("- Polyalphabetic: masks letter frequencies, defeating simple frequency analysis")
    print("- Historically considered 'le chiffre indéchiffrable' (the unbreakable cipher) for centuries")
    
    print("\n[bold red]Weaknesses:[/bold red]")
    print("- Key repetition creates patterns in the ciphertext")
    print("- Kasiski examination can find the key length by looking for repeated sequences")
    print("- Once key length is known, it can be broken like multiple Caesar ciphers using frequency analysis\n")
