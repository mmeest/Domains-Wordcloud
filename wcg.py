import pandas as pd
import re
import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 0. Hardcoded Estonian stopwords list
estonian_stopwords = {
    'ja', 'et', 'on', 'ei', 'kui', 'kas', 'oma', 'aga', 'mis', 'see', 'meie',
    'olen', 'oleme', 'oled', 'nad', 'siis', 'või', 'kõik', 'ka', 'sest', 'mida',
    'kes', 'kus', 'millal', 'sina', 'tema', 'neid', 'sind', 'mind', 'teie', 'ees',
    'loo', 'est', 'aha', 'mar', 'pia', 'ori', 'illa', 'ell', 'ana', 'anna', 'utu',
    'amine', 'mam', 'alar', 'kai', 'oka', 'mine', 'ala'
}

# 1. Hardcoded English stopwords list
english_stopwords = {
    'the', 'and', 'you', 'for', 'are', 'not', 'with', 'this', 'that', 'have',
    'from', 'was', 'your', 'but', 'they', 'his', 'her', 'its', 'all', 'can',
    'there', 'their', 'been', 'what', 'when', 'where', 'who', 'how', 'will', 'one',
    'do', 'if', 'so', 'out', 'up', 'about', 'more', 'just', 'like', 'than', 'some',
    'other', 'into', 'over', 'after', 'before', 'down', 'back', 'now', 'get', 'see',
    'make', 'know', 'take', 'go', 'come', 'think', 'say', 'want', 'use', 'find',
    'hit', 'dio', 'kat', 'mat', 'apia', 'aba', 'ene', 'ast', 'kos', 'ama', 'oft',
    'dita', 'per', 'kal', 'val', 'ein', 'ani', 'ame', 'ave', 'nut', 'tar', 'ate',
    'ade', 'par', 'uti', 'did', 'dis', 'che', 'bib', 'lek', 'ter', 'dee', 'des',
    'ken', 'rit', 'lev', 'rote', 'ote', 'gre', 'lin', 'gre', 'tor', 'nam', 'oka',
    'jut', 'lee'
}

# 2. Combine Estonian and English stopwords
combined_stopwords = estonian_stopwords | english_stopwords

# 3. Loading the CSV file with domain names
df = pd.read_csv('data/domains.csv', header=None, names=['domain'])

# 4. Cleaning domain names
def clean_domain(domain):
    domain = domain.lower()
    domain = re.sub(r'\.ee$', '', domain)
    domain = re.sub(r'[\d-]', ' ', domain)
    domain = re.sub(r'\s+', ' ', domain)
    return domain.strip()

cleaned_domains = df['domain'].dropna().apply(clean_domain).tolist()

# 5. Load the wordlist and filter out stopwords
with open('data/wordlist.txt', encoding='utf-8') as f:
    wordlist = [
        word.strip().lower()
        for word in f
        if word.strip() and word.strip().lower() not in combined_stopwords
    ]

# 6. Find words in cleaned domains
found_words = []

for word in sorted(wordlist, key=len, reverse=True):  # longest words first
    for i in range(len(cleaned_domains)):
        domain = cleaned_domains[i]
        if word in domain:
            found_words.append(word)
            # Remove the word from the domain
            cleaned_domains[i] = domain.replace(word, ' ', 1).strip()

# 6. Filter out short words and count occurrences
cleaned_words = [w for w in found_words if len(w) > 2]
word_counts = Counter(cleaned_words)

# 7. Top 20
top_20 = word_counts.most_common(20)
print("Top 20 sõna:\n")
for word, count in top_20:
    print(f"{word}: {count}")

# 8. Prepare text for WordCloud
text_for_wc = ' '.join([word for word, count in word_counts.items() for _ in range(count)])

# 9. Load custom mask image
custom_mask = np.array(Image.open("data/mask.png"))

# 10. Generate and save WordCloud
wc = WordCloud(
    width=800,
    height=400,
    background_color="white",
    mask=custom_mask,
    contour_color='black',
    contour_width=1.5
).generate_from_frequencies(word_counts)
wc.to_file("wordcloud.png")

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.show()
