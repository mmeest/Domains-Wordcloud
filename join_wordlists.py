# Loeme inglise ja eesti sõnad
with open('data/wordlist_eng.txt', encoding='utf-8') as f:
    eng_words = set(word.strip() for word in f if word.strip())

with open('data/wordlist_est.txt', encoding='utf-8') as f:
    est_words = set(word.strip() for word in f if word.strip())

# Ühendame ja eemaldame duplikaadid
combined_words = eng_words.union(est_words)

# Sorteerime pikkuse järgi kahanevalt
sorted_words = sorted(combined_words, key=lambda w: (-len(w), w))

# Salvestame uude faili
with open('wordlist_combined.txt', 'w', encoding='utf-8') as f:
    for word in sorted_words:
        f.write(word + '\n')

print(f"Kokku {len(sorted_words)} unikaalset sõna kirjutatud faili 'wordlist_combined.txt'.")
