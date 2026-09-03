import re

def clean_text(text):
    """Removes all non-alphabetic characters and converts to uppercase."""
    return re.sub(r'[^A-Z]', '', text.upper())

def group_text(text, n):
    """Groups text into blocks of size n."""
    return ' '.join(text[i:i+n] for i in range(0, len(text), n))
