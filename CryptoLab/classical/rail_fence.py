def encrypt(text, key):
    """Encrypts text using Rail Fence cipher. key is number of rails."""
    if key <= 1:
        return text
        
    text = "".join(text.split())
    rails = [[] for _ in range(key)]
    
    row = 0
    direction = 1
    
    for char in text:
        rails[row].append(char)
        row += direction
        
        if row == key - 1 or row == 0:
            direction *= -1
            
    return "".join(["".join(rail) for rail in rails])

def decrypt(cipher, key):
    """Decrypts text using Rail Fence cipher."""
    if key <= 1:
        return cipher
        
    cipher = "".join(cipher.split())
    
    # Mark positions
    rails = [[None] * len(cipher) for _ in range(key)]
    row = 0
    direction = 1
    for i in range(len(cipher)):
        rails[row][i] = '*'
        row += direction
        if row == key - 1 or row == 0:
            direction *= -1
            
    # Fill marked positions
    idx = 0
    for r in range(key):
        for c in range(len(cipher)):
            if rails[r][c] == '*' and idx < len(cipher):
                rails[r][c] = cipher[idx]
                idx += 1
                
    # Read zigzag
    result = ""
    row = 0
    direction = 1
    for i in range(len(cipher)):
        result += rails[row][i]
        row += direction
        if row == key - 1 or row == 0:
            direction *= -1
            
    return result

def show_steps(text, key):
    print(f"\n[bold blue]Plaintext:[/bold blue] {text}")
    print(f"[bold blue]Key (Rails):[/bold blue] {key}")
    print("\n[bold]Step 1: Write text in a zigzag pattern across rails[/bold]")
    
    # Simplified visualization for learning
    text_clean = "".join(text.split())
    matrix = [["." for _ in range(len(text_clean))] for _ in range(key)]
    row = 0
    direction = 1
    for i, char in enumerate(text_clean):
        matrix[row][i] = char
        row += direction
        if row == key - 1 or row == 0:
            direction *= -1
            
    for r in matrix:
        print("".join(r))
        
    print("\n[bold]Step 2: Read row by row[/bold]")
    print(f"[bold green]Ciphertext:[/bold green] {encrypt(text, key)}\n")

def show_strengths_weaknesses():
    print("\n[bold green]Strengths:[/bold green]")
    print("- Simple transposition cipher, changes positions rather than letters")
    print("- Does not alter letter frequencies (anagram of plaintext)")
    
    print("\n[bold red]Weaknesses:[/bold red]")
    print("- Easy to break with brute force (key is just the number of rails)")
    print("- Bigrams and trigrams are often split predictably\n")
