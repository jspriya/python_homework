def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)

        # Build the display string
        word = ""
        for l in secret_word:
            if l in guesses:
                word += l
            else:
                word += "_"
        print(word)

        return all(l in guesses for l in secret_word)
    return hangman_closure

if __name__ == "__main__":
    secret_word = input("Enter the secret word: ").lower()
    game = make_hangman(secret_word)

    print("_" * len(secret_word))

    while True:
        guess = input("Guess a letter: ").lower()

        if not guess:
            continue

        done = game(guess[0])  # take first character only

        if done:
            print("You guessed the word!")
            break

    