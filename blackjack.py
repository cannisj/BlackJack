'''
This script is simple BlackJack game.

Author: Rudolf Hlavacek
Date: 04.08.2020
Version: 1.0.0
Python version: 3.7.6
Python enviroment: Python 3.7.6 (default, Jan  8 2020, 20:23:39) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
'''
import random

SHUFFLE_THRESHOLD = 52
SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',   \
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,       \
          'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10,             \
          'King':10, 'Ace':11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]


    def __str__(self):
        return '{} of {}'.format(self.rank, self.suit)


class Deck:

    def __init__(self, num_of_decks=6):
        self.deck = []  # start with an empty list
        for num in range(num_of_decks):
            for suit in SUITS:
                for rank in RANKS:
                    created_card = Card(suit, rank)
                    self.deck.append(created_card)


    def __str__(self):
        list_of_cards = []
        for card in self.deck:
            list_of_cards.append(str(card))

        return str(list_of_cards)

    def __len__(self):
        return len(self.deck)


    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def __str__(self):
        list_of_cards = []
        for card in self.cards:
            list_of_cards.append(str(card))

        return str(list_of_cards)

    def add_card(self, card):
        new_card = card
        self.cards.append(new_card)

        if new_card.rank == 'Ace':
            self.aces += 1

        self.value += new_card.value

        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def clear(self):
        self.cards.clear()
        self.value = 0
        self.aces = 0


class Chips:

    def __init__(self, total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total +=  self.bet

    def lose_bet(self):
        self.total -= self.bet

class NoFundsError(Exception):
    pass

def player_wants_buyback(chips):
    buyback_choice = input("You're out of chips! Buy back in? (Y/N):" )
    if buyback_choice.upper() == 'Y':
        chips.total = 100  # Reset the chip count to 100
        print("Chips reset to: {}".format(chips.total))
        return True
    else:
        return False

def reset_game_state(deck, hand, dealer_hand, chips):
    # Check for null pointers
    if not all([deck, hand, dealer_hand, chips]):
        raise ValueError("One or more of the game objects is null.")

    chips.total = 100
    print("Chips reset to: {}".format(chips.total))

    # Clear all hands
    clear_hands(hand, dealer_hand)

    # Reshuffle deck
    if len(deck) < SHUFFLE_THRESHOLD:
        print("\n---------")
        print("RESHUFFLING DECK")
        print("---------\n")
        deck = Deck(DECKS_IN_GAME)

        # Check for unhandled exceptions
        try:
            deck.__init__()
        except Exception as e:
            print("Exception caught while reshuffling deck:", e)
            raise

    return deck  # return the updated deck

def take_bet(chips):
    while True:
        try:
            print('Your chips: {}'.format(chips.total))
            player_bet = int(input('Please, make your bet: \n'))
            if player_bet <= 0:
                raise Exception()

            if chips.total < player_bet:
                raise NoFundsError()

        except NoFundsError:
            print('Not enough chips. Your total amound is: {}\n'.format(chips.total))

        except:
            print('Sorry, no valid bet. Use positive integer numbers only!\n')

        else:
            chips.bet = player_bet
            break


def hit(deck, hand):
    hand.add_card(deck.deal())

def hit_or_stand(deck, hand):

    choise = ''
    while choise not in ('H', 'S'):
        choise = input('HIT or STAND? (H / S): ').upper()

    if choise == 'H':
        hit(deck, hand)
        return True
    else:
        return False

def clear_hands(*args):
    for hand in args:
        hand.clear()

def show_some(player_hand, dealer_hand):
    print("\nDEALERS HAND: {}+".format(dealer_hand.cards[1].value))
    print("['XXXXXXXXXXXX', '{}']".format(dealer_hand.cards[1]))
    if player_hand.aces == 0:
        print("\nPLAYERS HAND: {}".format(player_hand.value))
    else:
        print("\nPLAYERS HAND: {} / {}".format(player_hand.value-10, player_hand.value))
    print("{}\n\n".format(player_hand))


def show_all(player_hand, dealer_hand):
    print("\nDEALERS HAND: {}".format(dealer_hand.value))
    print("{}".format(dealer_hand))
    if player_hand.aces == 0:
        print("\nPLAYERS HAND: {}".format(player_hand.value))
    else:
        print("\nPLAYERS HAND: {} / {}".format(player_hand.value-10, player_hand.value))
    print("{}\n\n".format(player_hand))



def player_busts(player_hand, dealer_hand, player_chips):
    player_chips.lose_bet()

    print('\nPLAYER BUST!\n')

def player_wins(player_hand, dealer_hand, player_chips):
    player_chips.win_bet()

    print('\nPLAYER WINS\n')

def dealer_busts(player_hand, dealer_hand, player_chips):
    player_chips.win_bet()

    print('\nDEALER BUSTED! PLAYER WINS\n')

def dealer_wins(player_hand, dealer_hand, player_chips):
    player_chips.lose_bet()

    print('\nDEALER WINS\n')

def push(player_hand, dealer_hand):
    print('\nDealer and Player tie! PUSH\n')


WELCOME_TITLE = '''
****      *           *        ****     *   *     *****       *        ****     *   *
*   *     *          * *      *         *  *          *      * *      *         *  *
****      *         *****     *         ***           *     *****     *         ***
*   *     *         *   *     *         *  *      *   *     *   *     *         *  *
****      *****     *   *      ****     *   *      ****     *   *      ****     *   *
\n\n\n'''

DECKS_IN_GAME = 6

def game():
    
    SHUFFLE_THRESHOLD = 52

    # Print an opening statement
    print(WELCOME_TITLE)

    # Create & shuffle the deck, create player's & dealer's hand.
    deck = Deck(DECKS_IN_GAME)
    deck.shuffle()


    hand = Hand()
    dealer_hand = Hand()


    # Set up the Player's chips
    chips = Chips()

    while True:
        if chips.total == 0:
            print('Sorry, but you have lost all your chips! Time to go home, pal!!!')
            print('Hope you enjoyed the game :)')
            if not player_wants_buyback(chips):
                break
        else:
            deck = reset_game_state(deck, hand, dealer_hand, chips)

        # Prompt the Player for their bet
        take_bet(chips)

        # Deal two cards to each player.
        for num in range(2):
            dealer_hand.add_card(deck.deal())
            hand.add_card(deck.deal())

        # Show cards (but keep one dealer card hidden)
        show_some(hand, dealer_hand)

        playing = True
        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            playing = hit_or_stand(deck, hand)

            # Show cards (but keep one dealer card hidden)
            show_some(hand, dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if hand.value > 21:
                player_busts(hand, dealer_hand, chips)
                break


        if hand.value <= 21:

            # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
            while dealer_hand.value <= 16:
                hit(deck, dealer_hand)

            # Show all cards
            show_all(hand, dealer_hand)

            # Run different winning scenarios
            # If dealer is busted.
            if dealer_hand.value > 21:
                dealer_busts(hand, dealer_hand, chips)

            # If dealer wins.
            elif dealer_hand.value > hand.value:
                dealer_wins(hand, dealer_hand, chips)

            # If Player wins.
            elif dealer_hand.value < hand.value:
                player_wins(hand, dealer_hand, chips)

            # If Nobody wins.
            else:
                push(hand, dealer_hand)

        clear_hands(hand, dealer_hand)

        # Inform Player of their chips total.
        print('You have: {:>5}'.format(chips.total))
        
        # Ask to play again
        replay = input('Wanna play ANOTHER round (Y / N): ')
        if replay.upper() == 'N':
            break

        # Only few cards left in the box -> time to shuffle all cards.
        if len(deck) < SHUFFLE_THRESHOLD:
            del deck
            deck = Deck(DECKS_IN_GAME)
            deck.shuffle()
            print("\n-------------")
            print("DECK SHUFLLED")
            print("-------------\n")


if __name__ == '__main__':
    game()
