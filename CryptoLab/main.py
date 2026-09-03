import sys

try:
    from rich.console import Console
    from rich.prompt import Prompt, IntPrompt
    console = Console()
    print = console.print
except ImportError:
    print("Tip: Install 'rich' for a better UI (`pip install rich`)")
    class Prompt:
        @staticmethod
        def ask(msg, choices=None): return input(msg + " ")
    class IntPrompt:
        @staticmethod
        def ask(msg): return int(input(msg + " "))

from classical import caesar, atbash, vigenere, playfair, affine, rail_fence

def main_menu():
    while True:
        print("\n[bold cyan]Welcome to CryptoLab 🔐[/bold cyan]")
        print("1. Caesar Cipher")
        print("2. Atbash Cipher")
        print("3. Vigenère Cipher")
        print("4. Playfair Cipher")
        print("5. Affine Cipher")
        print("6. Rail Fence Cipher")
        print("7. Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            cipher_menu("Caesar", caesar, key_type="int")
        elif choice == "2":
            cipher_menu("Atbash", atbash, key_type="none")
        elif choice == "3":
            cipher_menu("Vigenère", vigenere, key_type="str")
        elif choice == "4":
            cipher_menu("Playfair", playfair, key_type="str")
        elif choice == "5":
            cipher_menu("Affine", affine, key_type="tuple")
        elif choice == "6":
            cipher_menu("Rail Fence", rail_fence, key_type="int")
        elif choice == "7":
            print("[bold green]Goodbye![/bold green]")
            sys.exit(0)

def cipher_menu(name, module, key_type="str"):
    print(f"\n[bold yellow]--- {name} Cipher ---[/bold yellow]")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Learn Mode (Steps & Weaknesses)")
    print("4. Back to Main Menu")
    
    choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])
    
    if choice == "4":
        return
        
    text = Prompt.ask("Enter the text")
    key = None
    if key_type == "int":
        key = IntPrompt.ask("Enter the key (integer)")
    elif key_type == "str":
        key = Prompt.ask("Enter the key (string)")
    elif key_type == "tuple":
        a = IntPrompt.ask("Enter key 'a' (coprime with 26)")
        b = IntPrompt.ask("Enter key 'b'")
        key = (a, b)
    
    if choice == "1":
        ciphertext = module.encrypt(text, key) if key_type != "none" else module.encrypt(text)
        print(f"\n[bold green]Result:[/bold green] {ciphertext}")
    elif choice == "2":
        plaintext = module.decrypt(text, key) if key_type != "none" else module.decrypt(text)
        print(f"\n[bold green]Result:[/bold green] {plaintext}")
    elif choice == "3":
        if key_type != "none":
            module.show_steps(text, key)
        else:
            module.show_steps(text)
        module.show_strengths_weaknesses()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n[bold red]Exiting...[/bold red]")
        sys.exit(0)
