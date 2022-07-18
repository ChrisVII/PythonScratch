
import random

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

class Card:    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank        
        self.value = values[rank]
    
    def __str__(self):
        return '{} of {}'.format(self.rank, self.suit)

class Deck:    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        return 'This deck has {} cards'.format(len(self.deck))

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value

        if card.rank == 'Ace':
            self.aces += 1 
    
    def adjust_for_ace(self):
        if (self.aces > 0)  and (self.value > 21):
            self.value -= 10
            self.aces -= 1
            return True
        else:
            return False
            

class Chips:    
    def __init__(self, total, bet):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = bet
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    valid = False

    while not valid:
        try:
            chips_to_bet = int(input("Enter number of chips to bet this round: "))
        except:
            print("Invalid input, must be non negative number.")
        else:
            if chips.total < chips_to_bet:
                print("Insufficient funds, try lower bet")
            else:
                valid = True
                chips.bet = chips_to_bet
                #print("Betting {} chips".format(chips.bet))
                print("")


def hit(deck,hand):    
    if len(deck.deck) != 0:
        hand.add_card(deck.deal())
        hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:
        try:
            result =int (input("Do you want to Hit [1] or Stand [2]? "))
        except:
            print("Invalid input, try again")
        else:
            if result == 1:
                hit(deck, hand)
                playing = True
                return True
            elif result == 2:
                playing = False
                return False
            else:
                print("Invalid input, try again")

def show_hands(player,dealer,hide=True):

    #find max hand size
    if len(player.cards) >= len(dealer.cards):
        maxsize = len(player.cards)
    else:
        maxsize = len(dealer.cards)

    if hide:
        dealer_score = "??"
    else:
        dealer_score = "{:2d}".format(dealer.value)

    print("DEALER HAND          PLAYER HAND")
    for index in range(0,maxsize):

        #check dealer hand
        if index == 0 and hide:
            dealer_card = "[Hidden]"
        elif index < len(dealer.cards):
            dealer_card = '[{}]'.format(str(dealer.cards[index]))
        else:
            dealer_card = " "

        #check playa hand
        if index < len(player.cards):
            player_card = '[{}]'.format(str(player.cards[index]))
        else:
            player_card = " "


        print('{:19s}  {:15s}'.format( dealer_card, player_card))

    print(" ")


def player_busts(chips):
    print(">>> PLAYER BUSTS! Lost {} chips".format(chips.bet))
    chips.lose_bet()

def player_wins(chips):
    print(">>> PLAYER WINS! Gained {} chips".format(chips.bet))
    chips.win_bet()

def dealer_busts(chips):
    print(">>> DEALER BUSTS! Gained {} chips".format(chips.bet))
    chips.win_bet()
    
def dealer_wins(chips):
    print(">>> DEALER WINS! Lost {} chips".format(chips.bet))
    chips.lose_bet()


## START GAME LOGIC HERE ##
# Print an opening statement
print("=================================================")
print("Welcome to BLACKJACK by Villabernal Game Studios")
print("=================================================")

# Set up the Player's chips
player_chips = Chips(100, 0) #defaults
round = 0

while True:
    
    print("\nPlayer chips: {}".format(player_chips.total))

    playing = True
    round += 1

    # Create & shuffle the deck, deal two cards to each player
    mydeck = Deck()
    mydeck.shuffle()

    player = Hand()
    player.add_card(mydeck.deal())
    player.add_card(mydeck.deal())

    dealer = Hand()
    dealer.add_card(mydeck.deal())
    dealer.add_card(mydeck.deal())

    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    print("=========== ROUND {} START! ===========".format(round))
    show_hands(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        if hit_or_stand(mydeck,player):
            # Show cards if another was added (but keep one dealer card hidden)
            print("")
            show_hands(player, dealer)
            
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        
        while dealer.value < 17:
            dealer.add_card(mydeck.deal())
            dealer.adjust_for_ace()
        
        # Show all cards
        print("")
        show_hands(player, dealer, False)
        temp = input("Press enter to step")

        # Run different winning scenarios
        if dealer.value > 21:
            #dealer busts, player wins
            dealer_busts(player_chips)

        elif dealer.value >= player.value:
            #dealer closer to 21, dealer wins
            dealer_wins(player_chips)

        else:
            #player closer to 21, player wins 
            player_wins(player_chips)
        
        print("----- Score -----\n  Dealer:{}\n  Player:{}".format(dealer.value,player.value))

            
    
    # Inform Player of their chips total
    print("\nPlayer's chips: {} Total".format(player_chips.total))
    
    # Ask to play again
    play_again = False

    while True:
        try:
            result = input("Play again? Enter [Y] or [N]")
        except:
            print('Invalid input')
        else:
            if result.upper() == 'N':
                play_again = False
                break
            if result.upper() == 'Y':
                if player_chips.total > 0:
                    play_again = True
                else:
                    print("Sorry, you are out of chips, get the fuck out!\n")
                    play_again = False
                break
            else:
                print('Invalid input')
    
    if not play_again:
        break

    print("")


