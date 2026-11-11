word = input("Enter a word: ")
vowel_count = 0

for char in word.lower():
    if char in "aeiou":
        vowel_count += 1

print(f"'{word}' contains {vowel_count} vowel(s)")
