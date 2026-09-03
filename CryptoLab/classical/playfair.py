def generate_matrix(key):
    """Generates the 5x5 Playfair matrix."""
    key = "".join([c.upper() for c in key if c.isalpha()])
    key = key.replace("J", "I")
    
    matrix = []
    seen = set()
    
    for char in key:
        if char not in seen:
            seen.add(char)
            matrix.append(char)
            
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)
            
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def prepare_text(text):
    """Prepares text for Playfair (uppercase, remove non-alpha, replace J with I, handle duplicates/odd length)."""
    text = "".join([c.upper() for c in text if c.isalpha()])
    text = text.replace("J", "I")
    
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            prepared += a + 'X'
            i += 1
        else:
            prepared += a + b
            i += 2
    
    if len(prepared) % 2 != 0:
        prepared += 'X'
        
    return prepared

def find_position(matrix, char):
    """Finds row and col of a character in the matrix."""
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return -1, -1

def process_digraph(matrix, a, b, encrypting=True):
    """Encrypts or decrypts a pair of characters."""
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)
    
    shift = 1 if encrypting else -1
    
    if row_a == row_b:
        return matrix[row_a][(col_a + shift) % 5] + matrix[row_b][(col_b + shift) % 5]
    elif col_a == col_b:
        return matrix[(row_a + shift) % 5][col_a] + matrix[(row_b + shift) % 5][col_b]
    else:
        return matrix[row_a][col_b] + matrix[row_b][col_a]

def encrypt(text, key):
    """Encrypts text using the Playfair cipher."""
    matrix = generate_matrix(key)
    prepared = prepare_text(text)
    
    result = ""
    for i in range(0, len(prepared), 2):
        result += process_digraph(matrix, prepared[i], prepared[i+1], True)
    return result

def decrypt(cipher, key):
    """Decrypts text using the Playfair cipher."""
    matrix = generate_matrix(key)
    # Ciphertext should already be in pairs and clean
    cipher = "".join([c.upper() for c in cipher if c.isalpha()]).replace("J", "I")
    
    result = ""
    for i in range(0, len(cipher), 2):
        result += process_digraph(matrix, cipher[i], cipher[i+1], False)
    return result

def show_steps(text, key):
    """Shows step-by-step breakdown of Playfair encryption."""
    matrix = generate_matrix(key)
    prepared = prepare_text(text)
    
    print(f"\n[bold blue]Plaintext:[/bold blue] {text}")
    print(f"[bold blue]Key:[/bold blue] {key}")
    
    print("\n[bold]Step 1: Generate 5x5 Key Matrix (I/J combined)[/bold]")
    for row in matrix:
        print(" ".join(row))
        
    print("\n[bold]Step 2: Prepare plaintext (group in 2s, insert X between double letters, pad with X)[/bold]")
    pairs = [prepared[i:i+2] for i in range(0, len(prepared), 2)]
    print(" ".join(pairs))
    
    print("\n[bold]Step 3: Encrypt pairs (Rectangle rule, Row rule, Column rule)[/bold]")
    steps = []
    for i in range(min(3, len(pairs))):
        a, b = pairs[i][0], pairs[i][1]
        c, d = process_digraph(matrix, a, b, True)
        steps.append(f"{a}{b} -> {c}{d}")
    print(" | ".join(steps) + (" | ..." if len(pairs) > 3 else ""))
    
    print(f"\n[bold green]Ciphertext:[/bold green] {encrypt(text, key)}\n")

def show_strengths_weaknesses():
    """Prints strengths and weaknesses of the Playfair cipher."""
    print("\n[bold green]Strengths:[/bold green]")
    print("- Encrypts digraphs (pairs) instead of single letters")
    print("- Flattens single-letter frequencies, making it harder to break than Caesar/substitution")
    print("- Used heavily in WWI because it required no equipment")
    
    print("\n[bold red]Weaknesses:[/bold red]")
    print("- Still vulnerable to frequency analysis, but using digraph frequencies (which is harder)")
    print("- Digraphs and their reverses (e.g., RE and ER) map to similar encrypted pairs")
    print("- A plaintext letter is never encrypted to itself\n")
