import random


# Card class
class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return str(self.value) + " of " + self.suit


# Deck class
class Deck:

    def __init__(self):
        self.deck = []
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        for i in range(4):
            for j in range(1, 14):
                card = Card(j, suits[i])
                self.deck.append(card)

    # shuffles the order of the deck
    def shuffle(self):
        # Fisher-Yates: choose uniformly within the remaining prefix.
        for i in range(len(self.deck) - 1, 0, -1):
            j = random.randint(0, i)
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]

    # draws the top card in deck
    def draw_card(self):
        if len(self.deck) > 0:
            return self.deck.pop(0)
        else:
            print("No cards left to draw")

    def __str__(self):
        ret = ""
        for card in self.deck:
            ret += str(card) + "\n"
        return ret


# Test the Card class
c1 = Card(5, "Hearts")
print(c1)

# Test the Deck Class
deck = Deck()
print(deck)
print()
deck.shuffle()
print(deck)
print(deck.draw_card())
print(deck.draw_card())
print(deck.draw_card())
print()
print(deck)
