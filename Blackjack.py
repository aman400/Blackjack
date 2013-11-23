# project - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
button_not_working = simplegui.load_sound("https://www.dropbox.com/s/fyd6o2bu2fq5v3g/button%20not%20working.ogg?dl=1")
won_game = simplegui.load_sound("https://www.dropbox.com/s/um0decuhbs5ljd9/won.ogg?dl=1")
#deal_cards = simplegui.load_sound("https://www.dropbox.com/s/uumn47d5w5wcaha/new%20deal.ogg?dl=1")
deal_new_card = simplegui.load_sound("https://www.dropbox.com/s/47zech3mdxs4nzx/deal_card.ogg?dl=1")
button_not_working.set_volume(1)
won_game.set_volume(1)
#deal_cards.set_volume(0.1)
deal_new_card.set_volume(0.3)

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank + " "

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	
        self.value = 0

    def __str__(self):
        string = "Hand contains "
        for c in self.cards:
            string += str(c)
        return string
        
    def add_card(self, card):
        c = Card(card.get_suit(), card.get_rank())
        self.cards.append(c)
        
    def get_value(self):
        """ count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust. """
        self.value = 0
        flag = False
        for c in self.cards:
            self.value += VALUES[c.get_rank()]
            if c.get_rank() == 'A':
                flag = True
        if flag and self.value + 10 <= 21:
            self.value += 10
        return self.value
                
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + 100*i, pos[1]])
            i += 1
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        """ shuffle the deck """
        random.shuffle(self.deck)

    def deal_card(self):
        """ deal a card from the deck """
        deal_new_card.play()
        random_card = random.choice(self.deck)
        self.deck.remove(random_card)
        return random_card
    
    def __str__(self):
        """ return a string representing the deck """
        s = "Deck Contains "
        for card in self.deck:
            s += str(card)
        return s

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, new_deal, display_dealer, message, score
#    deal_cards.play()
    if in_play:
        score -= 1
        outcome = 'You lose'
    else:
        outcome = ''
        
    new_deal = Deck()
    new_deal.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(new_deal.deal_card())
    player.add_card(new_deal.deal_card())
    dealer.add_card(new_deal.deal_card())
    dealer.add_card(new_deal.deal_card())
    display_dealer = False
    in_play = True
    message = "Hit or Stand?"

def hit():
    """ if the hand is in play, hit the player
        if busted, assign a message to outcome, update in_play and score		    
    """
    global outcome, in_play, score, message  
    if in_play:        
        #deal a new card from deck.
        player.add_card(new_deal.deal_card())
        
        # If player gets busted.
        if player.get_value() > 21:
            score -= 1
            message = "New Deal?"
            outcome = "You are busted."
            in_play = False
        else:
            outcome = ''
    else:
        button_not_working.play()
       
def stand():
    """	if hand is in play, repeatedly hit dealer until his hand has value 17 or more.
        Assign a message to outcome, update in_play and score
    """
    global outcome, in_play, score, display_dealer, message
    if in_play:
        display_dealer = True
        
        #deal new cards for dealer until dealer stands
        while dealer.get_value() < 17:
            dealer.add_card(new_deal.deal_card())

        # If dealer gets busted or value of dealer's cards is less than player's cards then player wins else player losses.
        if dealer.get_value() > 21:
            score += 1
            outcome = "Dealer busted."
            won_game.play()
        elif dealer.get_value() < player.get_value():
            score += 1
            outcome = "You won."
            won_game.play()
        else:
            score -= 1
            outcome = "You lose."
        message = "New deal?"
        in_play = False
    else:
        button_not_working.play()

# draw handler    
def draw(canvas):
    #draw scores
    canvas.draw_text("score  "+str(score), (450, 130), 30, "Black")
    
    #draw dealer cards
    canvas.draw_text("Blackjack", (175, 70), 50, "Lime")
    canvas.draw_text("Dealer         "+outcome, (50,175), 30, "Black")        
    dealer.draw(canvas, [50, 200])
    
    #draw card_back
    if not display_dealer:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [85, 250], CARD_BACK_SIZE)
    
    #draw player cards
    canvas.draw_text("Player          "+message, (50, 375), 30, "Black") 
    player.draw(canvas, [50, 400])
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()