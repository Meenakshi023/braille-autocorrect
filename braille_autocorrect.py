import Levenshtein
import time
import os

qwerty_to_dot = {'D': 1, 'W': 2, 'Q': 3, 'K': 4, 'O': 5, 'P': 6}

braille_to_char = {
    frozenset([1]): 'a', frozenset([1, 2]): 'b', frozenset([1, 4]): 'c',
    frozenset([1, 4, 5]): 'd', frozenset([1, 5]): 'e', frozenset([1, 2, 4]): 'f',
    frozenset([1, 2, 4, 5]): 'g', frozenset([1, 2, 5]): 'h', frozenset([2, 4]): 'i',
    frozenset([2, 4, 5]): 'j', frozenset([1, 3]): 'k', frozenset([1, 2, 3]): 'l',
    frozenset([1, 3, 4]): 'm', frozenset([1, 3, 4, 5]): 'n', frozenset([1, 3, 5]): 'o',
    frozenset([1, 2, 3, 4]): 'p', frozenset([1, 2, 3, 4, 5]): 'q', frozenset([1, 2, 3, 5]): 'r',
    frozenset([2, 3, 4]): 's', frozenset([2, 3, 4, 5]): 't', frozenset([1, 3, 6]): 'u',
    frozenset([1, 2, 3, 6]): 'v', frozenset([2, 4, 5, 6]): 'w', frozenset([1, 3, 4, 6]): 'x',
    frozenset([1, 3, 4, 5, 6]): 'y', frozenset([1, 3, 5, 6]): 'z'
}

def load_dictionary(file="google-10000-english.txt", min_len=2):
    if not os.path.exists(file):
        print(f" File '{file}' not found.")
        return []
    with open(file, "r") as f:
        return [
            word.strip().lower()
            for word in f
            if word.strip().isalpha() and len(word.strip()) >= min_len
        ]


def load_learned_words(file="user_learned_words.txt"):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return [line.strip().lower() for line in f if line.strip().isalpha()]

def save_learned_word(word, file="user_learned_words.txt"):
    with open(file, "a") as f:
        f.write(word.strip().lower() + "\n")

def interpret_braille_keys(key_input):
    try:
        dots = {qwerty_to_dot[k.upper()] for k in key_input if k.upper() in qwerty_to_dot}
        return braille_to_char.get(frozenset(dots), '?')
    except KeyError:
        return '?'

def get_closest_words(word, dictionary, learned, max_suggestions=5):
    combined_dict = list(set(dictionary + learned))
    scored = []

    for entry in combined_dict:
        distance = Levenshtein.distance(word, entry)
        boost = 0

        
        if entry.startswith(word[0]):
            boost -= 2
        if all(char in entry for char in word):
            boost -= 2
        if entry in learned:
            boost -= 3

        scored.append((entry, distance + boost))

    scored.sort(key=lambda x: x[1])
    return [w for w, _ in scored[:max_suggestions]]



def braille_autocorrect():
    print("\n Welcome Braille AutoCorrect")
    

    dictionary = load_dictionary()
    learned_words = load_learned_words()
    if not dictionary:
        return

    final_word = ''
    while True:
        keys = input(" Enter Braille keys: ").strip().upper()
        if keys == "":
            break
        if keys == "SPACE":
            final_word += ' '
            print("␣ Space added")
        elif keys == "BACK":
            final_word = final_word[:-1]
            print("⌫ Deleted last character")
        else:
            letter = interpret_braille_keys(keys)
            final_word += letter
            print(f"⟶ Interpreted as: {letter}")

    print(f"\n Final interpreted input: {final_word}")
    start_time = time.time()
    suggestions = get_closest_words(final_word.strip(), dictionary, learned_words)
    duration = time.time() - start_time

    print(f" Suggestions: {suggestions if suggestions else ['(no close matches)']}")
    

    if suggestions:
        choice = input(f" Enter correct word from suggestions (or leave blank to skip): ").strip().lower()
        if choice in suggestions:
            save_learned_word(choice)
            print(f" Learned word '{choice}' added for better future suggestions.")

if __name__ == "__main__":
    braille_autocorrect()
