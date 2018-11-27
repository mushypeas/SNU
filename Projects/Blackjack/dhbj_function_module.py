import dhbj_class_module
import os

# ACTS
def split(player, PLAYER, deck):
    '''Performs a split'''
    temp_name = player.name
    temp = PLAYER.pop(player.name)
    PLAYER[temp_name] = temp # Makes the player who splits goes to the last, next to its split hand
    split_name = player.name
    while split_name in [names for names in PLAYER]:
        split_name += '_split'
    PLAYER[split_name] = dhbj_class_module.Player(split_name, [], player.balance, player.bet)
    PLAYER[split_name].cards.append(player.cards.pop())
    PLAYER[split_name].cards.append(deck.draw_card())
    player.cards.append(deck.draw_card())

def double_down(player,deck):
    '''Performs Double down'''
    player.cards.append(deck.draw_card())
    input(f'{player.name} has doubled the bet from {player.bet} $ to {player.bet * 2} $')
    player.bet *= 2
    player.in_game = False

def hit(player, deck):
    '''Performs hit'''
    player.cards.append(deck.draw_card())
    input(f'{player.name} hits')
    if player.sum_value() == 21:
        player.in_game = False

def stand(player):
    '''Performs stand'''
    input(f'{player.name} stands')
    player.in_game = False

def surrender(player, PLAYER, DEALER):
    '''Performs surrender'''
    if '_split' in player.name: # The player who performed the split loses the money
        PLAYER[player.name.strip('_split')].balance -= int(round(player.bet / 2))
        DEALER.balance += int(round(player.bet / 2))
        input(f"{player.name} surrenders and {PLAYER[player.name.strip('_split')].name} loses {int(round(player.bet / 2))} $ to the Dealer (Owning: {PLAYER[player.name.strip('_split')].balance} $)")
        player.status = 'ended'
        player.in_game = False
    else:
        player.balance -= int(round(player.bet / 2))
        DEALER.balance += int(round(player.bet / 2))
        input(f'{player.name} surrenders and loses {int(round(player.bet / 2))} $ to the Dealer (Owning: {player.balance} $)')
        player.status = 'ended'
        player.in_game = False

def insurance(PLAYER, DEALER):
    ''' Asks for & performs insurance and Even money '''
    print("The dealer's first card is an A!")
    for player in PLAYER.values():
        while True:
            if player.sum_value() == 21:
                decide = input(f'{player.name}: You have a Blackjack. Accept Even money? Y/N\n').upper()
                if decide == 'Y':
                    player.balance += player.bet
                    DEALER.balance -= player.bet
                    input(f'{player.name} accepted Even money and earns {player.bet} $ from the Dealer (Owning: {player.balance} $)')
                    player.status = 'ended'
                    player.in_game = False
                    player.even = True
                    break
                elif decide == 'N':
                    input(f'{player.name} denied Even money')
                    break
                else:
                    print('Wrong input: Try again')
            else:
                if player.balance < player.bet * 1.5:
                    input(f'{player.name} does not have enough money for an insurance')
                    break
                else:
                    decide = input(f'{player.name}: Get an insurance? Y/N\n').upper()
                    if decide == 'Y':
                        player.balance -= int(round(player.bet / 2))
                        DEALER.balance += int(round(player.bet / 2))
                        input(f'{player.name} accepted insurance and pays {int(round(player.bet / 2))} $ to the Dealer (Owning: {player.balance} $)')
                        player.insure = True
                        break
                    elif decide == 'N':
                        input(f'{player.name} denied insurance')
                        break
                    else:
                        print('Wrong input: Try again')

# RULES
def dealer_bj(DEALER, PLAYER, mode):
    ''' When the dealer is a Blackjack '''
    print('The Dealer is Blackjack')
    _ = os.system('color 0f')
    _ = os.system('color 0c')
    _ = os.system('color 0f')
    _ = os.system('color 0c')
    _ = os.system('color 0f')
    if mode == 'hard':
        _ = os.system('color 0c')
    elif mode == 'lucky':
        _ = os.system('color 0e')
    else:
        _ = os.system('color 0a')
    for player in PLAYER.values():
        if player.sum_value() == 21:
            if player.even:
                print(f'{player.name} accepted Even money')
            else:
                print(f'{player.name} is Blackjack, too')
                if mode == 'easy':
                    player.status = 'won'
                else:
                    player.status = 'push'
        elif player.insure:
            player.balance += player.bet
            DEALER.balance -= player.bet
            print(f'{player.name} earns {player.bet} $ from the Dealer by insurance! (Owning: {player.balance} $)')
            player.status = 'lost'
    input('')

def bj(player, mode, DEALER):
    ''' When a player is a blackjack '''
    if mode == 'hard':
        player.balance += int(player.bet * 1.2)
        DEALER.balance -= int(player.bet * 1.2)
        input(f'{player.name} Blackjack!\n{player.name} gains {int(round(player.bet * 1.2))} $ from the Dealer (Owning: {player.balance} $)')
    elif mode == 'lucky':
        player.balance += int(player.bet * 3)
        DEALER.balance -= int(player.bet * 3)
        input(f'{player.name} Blackjack!\n{player.name} gains {int(round(player.bet * 3))} $ from the Dealer (Owning: {player.balance} $)')
    else:
        player.balance += int(player.bet * 1.5)
        DEALER.balance -= int(player.bet * 1.5)
        input(f'{player.name} Blackjack!\n{player.name} gains {int(round(player.bet * 1.5))} $ from the Dealer (Owning: {player.balance} $)')
    player.status = 'ended'
    player.in_game = False

def bust(player):
    ''' When a player busts '''
    input(f'{player.name} busts')
    player.status = 'lost'
    player.in_game = False

def jackpot(player, PLAYER, DEALER): # Only in lucky mode
    print('JackPot!')
    _ = os.system('color 0f')
    _ = os.system('color 0e')
    _ = os.system('color 0f')
    _ = os.system('color 0e')
    _ = os.system('color 0f')
    _ = os.system('color 0e')
    if '_split' in player.name: # The player who performed the split earns the Jackpot
        PLAYER[player.name.strip('_split')].balance += player.bet * 7
        DEALER.balance -= player.bet * 7
    else:
        player.balance += player.bet * 7
        DEALER.balance -= player.bet * 7
    input(f'{player.name:<10} earns {player.bet * 7} $ from the Dealer (Owning: {player.balance} $)')
    player.status = 'ended'

# SUM UP
def lose(player, PLAYER, DEALER):
    ''' Players who lost loses money '''
    if '_split' in player.name: # The player who performed the split loses the money
        PLAYER[player.name.strip('_split')].balance -= player.bet
        DEALER.balance += player.bet
        print(f"{player.name:<10} lost and {PLAYER[player.name.strip('_split')].name} loses {player.bet} $ to the Dealer (Owning: {PLAYER[player.name.strip('_split')].balance} $)")
    else:
        player.balance -= player.bet
        DEALER.balance += player.bet
        print(f'{player.name:<10} lost and loses {player.bet} $ to the Dealer (Owning: {player.balance} $)')

def win(player, PLAYER, DEALER):
    ''' Players who won earns money '''
    if '_split' in player.name: # The player who performed the split earns the money
        PLAYER[player.name.strip('_split')].balance += player.bet
        DEALER.balance -= player.bet
        print(f"{player.name:<10} won and {PLAYER[player.name.strip('_split')].name} earns {player.bet} $ from the Dealer (Owning: {PLAYER[player.name.strip('_split')].balance} $)")
    else:
        player.balance += player.bet
        DEALER.balance -= player.bet
        print(f'{player.name:<10} won and earns {player.bet} $ from the Dealer (Owning: {player.balance} $)')

def push(player, PLAYER):
    ''' Player pushes'''
    if '_split' in player.name:
        print(f'{player.name:<10} push')
    else:
        print(f'{player.name:<10} push (Owning: {player.balance} $)')

