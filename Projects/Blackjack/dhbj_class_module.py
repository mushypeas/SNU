import random
class Deck:
    ''' Includes features of the deck '''
    def __init__(self,cards_left = {'♠':[],'♥':[],'◆':[],'♣':[]}):
        self.cards_left = cards_left

    def refresh_deck(self,mode):
        '''
        Resets deck every new game
        '''
        for suits in self.cards_left:
            if mode == 'hard':
                self.cards_left[suits] = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'] * 2
            elif mode == 'lucky':
                self.cards_left[suits] = ['A', 7, 7, 7, 'J', 'Q', 'K'] * 10
            else:
                self.cards_left[suits] = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
            random.shuffle(self.cards_left[suits])
    def draw_card(self):
        '''
        Picks a random card from a deck and returns the identity of the drawn card
        '''
        drawn_suit = random.choice(list(self.cards_left.keys()))
        drawn_rank = random.choice(self.cards_left[drawn_suit])
        self.cards_left[drawn_suit].remove(drawn_rank)
        if type(drawn_rank) == int:
            drawn_value = drawn_rank
        elif drawn_rank == 'A':
            drawn_value = 11
        else:
            drawn_value = 10
        return (drawn_suit,drawn_rank,drawn_value)
    def __str__(self):
        return f'{self.cards_left}'

class Player:
    """
    Attributes each player needs during the game
    """
    def __init__(self, name = '', cards = [], balance = 1000, bet = 0, denied_split = False,in_game = True, status = '', even = False, insure = False):
        self.name = name
        self.balance = balance # Amount of money the player owns
        self.bet = bet # Amount of money the player bets
        self.cards = cards # Cards in the player's current hand as a list of tuples - tuple of a single card: (suit, rank, value)
        self.in_game = in_game # True if player is playing, False if player lost or ended(e.g. Blackjack or Double Down) game
        self.denied_split = denied_split
        self.status = status
        """
        ''     : Default
        'ended': Player's game ended by surrenderring or without losing
        'lost' : Player has lost the game
        'won'  : Player has won the game
        """
        self.even = even # True if player does Even money
        self.insure = insure # True if player gets as unsurance
    def sum_value(self): 
        '''
        Sum of values of a player's hand
        '''
        sum = 0
        for suit, rank, value in self.cards:
            sum += value
        for suit, rank, value in self.cards:
            if (rank is "A") and (sum > 21):
                sum -= 10 # A's value becomes 1 from 11 if value's sum is high
        return sum
