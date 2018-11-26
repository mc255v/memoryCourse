# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
back = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print
            "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = ""
        for card in self.cards:
            ans += card.__str__() + " "
        return "Hand contains: " + ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.cards:
            value += VALUES.get(card.get_rank())
        for card in self.cards:
            if card.get_rank() == 'A':
                if (value + 10) <= 21:
                    value += 10
        return value

    def draw(self, canvas, pos):
        loc = list(pos)
        for card in self.cards:
            card.draw(canvas, loc)
            loc[0] += 75


# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        ans = ""
        for card in self.deck:
            ans += card.__str__() + " "
        return "Deck contains: " + ans


# define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score, back
    back = True
    outcome = "Hit or Stand?"
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    i = 0
    while i <= 1:
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        i += 1
    if in_play:
        score -= 1
    in_play = True


def hit():
    global in_play, outcome, score
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            in_play = False
            outcome = "You have busted!"
            score -= 1


def stand():
    global outcome, in_play, score, back
    back = False
    if in_play:
        if player.get_value() > 21:
            outcome = "You have already busted!"
            in_play = False
        else:
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
            if player.get_value() > dealer.get_value() or dealer.get_value() > 21:
                outcome = "You won!"
                score += 1
                in_play = False
            else:
                outcome = "You lost!"
                score -= 1
                in_play = False


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (125, 65), 30, 'White')
    canvas.draw_text(outcome, (300, 150), 30, 'White')
    canvas.draw_text(("Score: " + str(score)), (425, 65), 30, 'White')
    if not in_play:
        canvas.draw_text("New deal?", (55, 550), 30, 'White')
    canvas.draw_text("Dealer:", (55, 150), 30, 'White')
    canvas.draw_text("Player:", (55, 375), 30, 'White')
    player.draw(canvas, [55, 400])
    dealer.draw(canvas, [55, 175])
    if back:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (55 + CARD_CENTER[0], 175 + CARD_CENTER[1]),
                          CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric