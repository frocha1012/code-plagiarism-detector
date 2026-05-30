def count_vowels(text):
    vowels = {"a", "e", "i", "o", "u"}
    total = 0

    for character in text.lower():
        if character in vowels:
            total += 1

    return total


message = "plagiarism detector"
vowel_count = count_vowels(message)
print(vowel_count)
