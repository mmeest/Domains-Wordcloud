import pandas as pd
import re
from collections import Counter

def clean_domain(domain):
    # Remove common TLDs and special characters
    domain = re.sub(r'\.(com|ee|org|net|edu|gov|int|mil|biz|info|name|mobi|pro|aero|coop|museum)$', '', domain)
    # Split by common separators
    words = re.split(r'[^a-zA-ZäöüõÄÖÜÕ]', domain)
    # Filter out empty strings and very short words
    return [word.lower() for word in words if len(word) > 2]

def main():
    # Read the CSV file
    df = pd.read_csv('data/report.csv')
    
    # Read existing wordlist
    with open('data/wordlist.txt', 'r', encoding='utf-8') as f:
        existing_words = set(line.strip().lower() for line in f)
    
    # Extract and count words from domains
    all_words = []
    for domain in df['word']:  # Using 'word' column instead of 'domain'
        words = clean_domain(domain)
        all_words.extend(words)
    
    # Count word frequencies
    word_counts = Counter(all_words)
    
    # Filter out words that are already in wordlist.txt
    new_words = {word: count for word, count in word_counts.items() 
                 if word not in existing_words}
    
    # Sort by frequency
    sorted_words = sorted(new_words.items(), key=lambda x: x[1], reverse=True)
    
    # Print top 50 most common new words
    print("\nTop 50 most common words not in wordlist.txt:")
    print("-" * 40)
    for word, count in sorted_words[:50]:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main() 