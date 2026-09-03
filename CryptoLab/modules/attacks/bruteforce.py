from classical import caesar
import re

# Simple list of common English words for heuristic scoring
COMMON_WORDS = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'hello', 'world', 'secret'])

def score_text(text):
    """Gives a score to a text based on how many common English words it contains."""
    words = re.findall(r'\w+', text.lower())
    score = 0
    for word in words:
        if word in COMMON_WORDS:
            score += 1
    return score

def bruteforce_caesar(ciphertext):
    """
    Tries all 25 possible shifts for Caesar cipher.
    Returns a list of dictionaries with shift, plaintext, and a score.
    """
    results = []
    
    for shift in range(1, 26):
        # Decrypting with shift X is same as encrypting with shift -X
        plaintext = caesar.decrypt(ciphertext, shift)
        score = score_text(plaintext)
        results.append({
            'shift': shift,
            'plaintext': plaintext,
            'score': score
        })
        
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
