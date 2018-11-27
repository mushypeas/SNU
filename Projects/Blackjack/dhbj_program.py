'''
Blackjack?
'''
import os
import time
import sys
import dhbj_class_module
import dhbj_function_module

def betting():
    '''
    Do the players' betting
    '''
    _ = os.system('cls')
    string = f'============ Turn {turn} ============'
    for char in string:
        if char == '=':
            time.sleep(0.01)
        else:
            time.sleep(0.1)
        print(char, end = '', flush = True)
    time.sleep(0.2)
    for player in PLAYER.values():
        while True:
            _ = os.system('cls')
            print(f'============ Turn {turn} ============')
            print('\n D ┌-───-┐┌-───-┐       D ┌-───-┐')
            print(' E │ ▓▓▓▓││ ▓▓▓▓│       E │ ▓▓▓▓│')
            print(' A │ ▓▓▓▓││ ▓▓▓▓│       C │ ▓▓▓▓│')
            print(' L │ ▓▓▓▓││ ▓▓▓▓│       K │ ▓▓▓▓│')
            print(f' E └-───-┘└-───-┘         └-───-┘\n R   Dealer owning: {DEALER.balance} $\n')
            if mode == 'hard' and DEALER.balance < 15000:
                print('The Dealer is eager for a Blackjack...\n')
            try:
                    print(f'{player.name}, How much would you bet?')
                    player.bet = int(input(f"(Owning: {player.balance} $)\n"))
            except:
                print('Wrong input: Try again')
                time.sleep(0.4)
            else:
                if 0 < player.bet < player.balance:
                    input(f"{player.name} bets {player.bet} $\n")
                    break
                elif player.bet == player.balance:
                    if mode == 'lucky':
                        input(f'{player.name} is feeling lucky!')
                    else:
                        input(f'{player.name} is all in!')
                    break
                else:
                    print('Out of range. Try again.')
                    time.sleep(0.4)

def print_game():
    '''
    Print the ongoing situation of the game
    '''
    _ = os.system('cls')
    print(f'============ Turn {turn} ============')
    if not game_set: # Print dealer's cards. Deck is for decoration
        rank = DEALER.cards[0][1]
        suit = DEALER.cards[0][0]
        if rank == 10:
            print('\n D ┌-───-┐┌-───-┐       D ┌-───-┐')
            print(f' E │ {rank}  ││ ▓▓▓▓│       E │ ▓▓▓▓│')
            print(f' A │  {suit} ││ ▓▓▓▓│       C │ ▓▓▓▓│')
            print(f' L │   {rank}││ ▓▓▓▓│       K │ ▓▓▓▓│')
            print(f' E └-───-┘└-───-┘         └-───-┘\n R   Dealer owning: {DEALER.balance:<4} $\n')
        else:
            print('\n D ┌-───-┐┌-───-┐       D ┌-───-┐')
            print(f' E │ {rank}   ││ ▓▓▓▓│       E │ ▓▓▓▓│')
            print(f' A │  {suit} ││ ▓▓▓▓│       C │ ▓▓▓▓│')
            print(f' L │    {rank}││ ▓▓▓▓│       K │ ▓▓▓▓│')
            print(f' E └-───-┘└-───-┘         └-───-┘\n R   Dealer owning: {DEALER.balance:<4} $\n')
    else:
        n = len(DEALER.cards)
        print('\n D ' + '┌-───-┐' * n + '       D ┌-───-┐')
        print(' E ', end = '')
        for suit, rank, value in DEALER.cards:
            if rank == 10:
                print(f'│ {rank}  │', end = '')
            else:
                print(f'│ {rank}   │', end = '')
        print('       E │ ▓▓▓▓│\n A ', end = '')
        for suit, rank, value in DEALER.cards:
            print(f'│  {suit} │', end = '')
        print('       C │ ▓▓▓▓│\n L ', end = '')
        for suit, rank, value in DEALER.cards:
            if rank == 10:
                print(f'│   {rank}│', end = '')
            else:
                print(f'│    {rank}│', end = '')
        print("       K │ ▓▓▓▓│\n E "+"└-───-┘" * n + f"         └-───-┘\n R   Dealer owning: {DEALER.balance:<4} $  Dealer's value: {DEALER.sum_value()}\n")
    for player in PLAYER.values(): # Print each player's cards.
        n = len(player.cards)
        if '_split' in player.name:
            print(f'    {player.name:<10} Value: {player.sum_value():<2} Bet: {player.bet}$')
        else:
            print(f'    {player.name:<10} Value: {player.sum_value():<2} Owning: {player.balance:<4}$  Bet: {player.bet}$')
        if player.status == 'lost':
            print('  ' + '┌-───-┐' * n)
            print('  ' + '│ ▓▓▓▓│' * n)
            print('  ' + '│ ▓▓▓▓│' * n)
            print('  ' + '│ ▓▓▓▓│' * n)
            print('  ' + '└-───-┘' * n+'\n')
        else:
            print('  ' + '┌-───-┐' * n)
            print('  ', end = '')
            for suit, rank, value in player.cards:
                if rank == 10:
                    print(f'│ {rank}  │', end = '')
                else:
                    print(f'│ {rank}   │', end = '')
            print('\n  ', end = '')
            for suit, rank, value in player.cards:
                print(f'│  {suit} │', end = '')
            print('\n  ', end = '')
            for suit, rank, value in player.cards:
                if rank == 10:
                    print(f'│   {rank}│', end = '')
                else:
                    print(f'│    {rank}│', end = '')
            print('\n  '+'└-───-┘' * n + '\n')

def give_cards():
    '''
    Dealer and Players get their cards
    '''
    DECK.refresh_deck(mode)
    DEALER.cards = []
    DEALER.cards.append(DECK.draw_card())  # Dealer draws two cards from the deck
    DEALER.cards.append(DECK.draw_card())
    for player in PLAYER.values():
        player.cards = []
        player.cards.append(DECK.draw_card()) # Each player draws two cards from the deck
        player.cards.append(DECK.draw_card())

def proceed_turn():
    '''
    The actual procedure of one game
    '''
    global game_set # Checks if current game is over
    give_cards()
    game_set = False
    if mode == 'hard': # Higher chances of Blackjack
        if DEALER.balance < 15000:
            itr = (10 - int(DEALER.balance/1500)) * 2
            while DEALER.sum_value() != 21 and itr > 0:
                give_cards()
                itr -= 1
        if DEALER.sum_value() != 21:
            give_cards()
            if DEALER.cards[0][1] == 'A':
                print_game()
                dhbj_function_module.insurance(PLAYER, DEALER)
                if DEALER.sum_value() != 21:
                    print_game()
                    input('Dealer was not Blackjack')
            if DEALER.sum_value() == 21:
                game_set = True
                print_game()
                dhbj_function_module.dealer_bj(DEALER, PLAYER, mode)
        else:
            if DEALER.cards[0][1] == 'A':
                print_game()
                dhbj_function_module.insurance(PLAYER, DEALER)
            game_set = True
            print_game()
            dhbj_function_module.dealer_bj(DEALER, PLAYER, mode)
    else:
        if DEALER.cards[0][1] == 'A':
            print_game()
            dhbj_function_module.insurance(PLAYER, DEALER)
            if DEALER.sum_value() != 21:
                print_game()
                input('Dealer was not Blackjack')
        if DEALER.sum_value() == 21: # Checks if the dealer has a Blackjack
            game_set = True
            print_game()
            dhbj_function_module.dealer_bj(DEALER, PLAYER, mode)
    while not game_set:
        while any([((p.cards[0][1] == p.cards[1][1]) and not p.denied_split) for p in PLAYER.values()]): 
        # Checks if there is someone who can and didn't reject to split
            split = False
            for player in PLAYER.values():
                print_game()
                if all([(player.cards[0][1] == player.cards[1][1]), not player.denied_split, player.in_game]):
                    if player.balance >= player.bet * (len(list(filter(lambda name: f"{player.name.strip('_split')}" in name, list(PLAYER)))) + 1):
                        print(f'{player.name} can perform a Split!')
                        print('Will you perform a split? Y/N')
                        while True:
                            ans = input('').upper()
                            if ans == 'Y':
                                split = True
                                split_name = player.name
                                input(f'{player.name} splits')
                                break
                            elif ans == 'N':
                                input(f'{player.name} does not split')
                                player.denied_split = True
                                break
                            else:
                                print('Wrong input: Try again')
                        break
                    else:
                        input(f"{player.name.strip('_split')}'s balance is low for {player.name}'s Split")
                        player.denied_split = True
            if split:
                dhbj_function_module.split(PLAYER[split_name], PLAYER, DECK) # Done outside of for loop since it changes the length of PLAYER library
        for player in PLAYER.values():
            print_game()
            if not player.in_game:
                continue
            if len(player.cards) == 2:
                if (player.sum_value() == 21):
                    if (player.name.strip('_split') + '_split' in [names for names in PLAYER]):
                        player.in_game = False
                    else:
                        dhbj_function_module.bj(player, mode, DEALER)
                    continue
                total_bet = 0
                for name in list(filter(lambda name: f"{player.name.strip('_split')}" in name, list(PLAYER))):
                    total_bet += PLAYER[name].bet
                if player.balance >= total_bet + player.bet:
                    while True:
                        ans = input(f'{player.name}, What would you do?\nsr: Surrender\nd:  Double Down\nst: Stand\nh:  Hit\n').lower()
                        if ans in ['sr','d','st','h']:
                            break
                        else:
                            print('Wrong input: Try again\n')
                else:
                    print('Your balance is low for a Double Down!')
                    while True:
                        ans = input(f'{player.name}, What would you do?\nsr: Surrender\nst: Stand\nh:  Hit\n').lower()
                        if ans in ['sr', 'st', 'h']:
                            break
                        else:
                            print('Wrong input: Try again\n')
            else:
                while True:
                    ans = input(f'{player.name}, What would you do?\nsr: Surrender\nst: Stand\nh:  Hit\n').lower()
                    if ans in ['sr', 'st', 'h']:
                        break
                    else:
                        print('Wrong input: Try again\n')
            if ans == 'sr':
                dhbj_function_module.surrender(player, PLAYER, DEALER)
            elif ans == 'd':
                dhbj_function_module.double_down(player, DECK)
            elif ans == 'st':
                dhbj_function_module.stand(player)
            else:
                dhbj_function_module.hit(player, DECK)
            if player.sum_value() == 21 and mode == 'lucky':
                print_game()
                ls = []
                for suit, rank, value in player.cards:
                    ls.append(value == 7)
                if all(ls):
                    dhbj_function_module.jackpot(player, PLAYER, DEALER)
            if player.sum_value() > 21:
                print_game()
                dhbj_function_module.bust(player)
        game_set = True
        for player in PLAYER.values():
            if player.in_game:
                game_set = False # Continues game if at least one player is left

def end_turn():
    '''
    Sums up the results of one turn
    Players who lost lose money
    Players who won gain money
    '''
    while DEALER.sum_value() < 17:
        DEALER.cards.append(DECK.draw_card())
    print_game()
    if DEALER.sum_value() > 21:
        print('Dealer busts')
        for player in PLAYER.values():
            if player.status == '':
                player.status = 'won'
    else:
        for player in PLAYER.values():
            if player.status == '':
                if player.sum_value() > DEALER.sum_value():
                    player.status = 'won'
                elif player.sum_value() == DEALER.sum_value():
                    if mode == 'easy':
                        player.status = 'won'
                    else:
                        player.status = 'push'
                else:
                    player.status = 'lost'
    input_trigger = False
    for player in PLAYER.values():
        if player.status == 'won':
            dhbj_function_module.win(player, PLAYER, DEALER)
            input_trigger = True
        elif player.status == 'lost':
            dhbj_function_module.lose(player, PLAYER, DEALER)
            input_trigger = True
        elif player.status == 'push':
            dhbj_function_module.push(player, PLAYER)
            input_trigger = True
    if input_trigger: # Makes it able to read the results if anything happened.
        input()

def sum_game():
    '''
    Check if game has ended
    Eliminate split players

    '''
    print_game()
    game_over = True # becomes False if game is not over
    pop_list = []
    for player in PLAYER.values():
        if DEALER.balance <= 0: # Game ends if someone achieves more than 10000 $
            DEALER.balance = '───'
            print_game()
            input("Congratulations! You've achieved victory!")
            _ = os.system('cls & color 0f')
            quit()
        if player.balance <= 0 and '_split' not in player.name:
            print(f'{player.name} seems to be out of money... GG')
            pop_list.append(player.name)
        if '_split' in player.name:
            pop_list.append(player.name)
        if player.balance > 0:
            game_over = False # Game isn't over if someone has money left
            player.in_game = True
            player.even = False   # Return specific values
            player.insure = False # of remaining players 
            player.status = ''    # to default( Not all, since some have to stay )
            player.denied_split = False
    for name in pop_list:
        PLAYER.pop(name) 
    if game_over:
        print('=========== GAME OVER ===========')
        input('Seems like everyone is out of money.\nBetter luck next time...')
        _ = os.system('cls & color 0f')
        quit()
    input('Press enter to continue...')

if __name__ == '__main__':
    _ = os.system('color 0a & cls')
    time.sleep(0.2)
    print('===Python DealerRaid Blackjack===')
    time.sleep(0.2)
    string = ('        Bankrupt the Dealer!')
    for char in string:
        time.sleep(0.03)
        print(char,end='',flush=True)
    time.sleep(1)
    while True:
        ans = input("\n\n-Select-\n\nE: Easy mode\nN: Normal mode\nH: Hard mode\n?: Help\nX: Exit\n!: I'm feeling lucky...\n").upper()
        if ans == 'E':
            _ = os.system('cls')
            print('===Python DealerRaid Blackjack===\n        Bankrupt the Dealer!\n\n')
            print('Start as Easy mode\n\n• 3 to 2 Blackjack\n• Dealer Balance: 5000  $\n• Push disabled\n• Up to 4 Players\n• One Deck\n')
            mode = 'easy'
            DEALER = dhbj_class_module.Player('Dealer', cards = [], balance = 5000)
            break
        elif ans == 'N':
            _ = os.system('cls')
            print('===Python DealerRaid Blackjack===\n        Bankrupt the Dealer!\n\n')
            print('Start as Normal mode\n')
            time.sleep(0.15)
            print('• 3 to 2 Blackjack')
            time.sleep(0.15)
            print('• Dealer Balance: 10000 $')
            time.sleep(0.15)
            print('• Push enabled')
            time.sleep(0.15)
            print('• Up to 4 Players')
            time.sleep(0.15)
            print('• One Deck\n')
            time.sleep(0.15)
            mode = 'normal'
            DEALER = dhbj_class_module.Player('Dealer', cards = [], balance = 10000)
            break
        elif ans == 'H':
            _ = os.system('cls & color 0c')
            print('===Python DealerRaid Blackjack===\n        Bankrupt the Dealer!\n\n')
            string = 'Start as HARD MODE\n\n'
            for char in string:
                if char in 'HARDMODE':
                    time.sleep(0.15)
                else:
                    time.sleep(0.01)
                print(char,end='',flush=True)
            print('• 5 to 6 Blackjack')
            time.sleep(0.15)
            print('• Dealer Balance: 20000 $')
            time.sleep(0.15)
            print('• Push enabled')
            time.sleep(0.15)
            print('• Dealer gets a Blackjack more often')
            time.sleep(0.15)
            print('• Up to 6 Players')
            time.sleep(0.15)
            print('• Two Decks\n\n')
            time.sleep(0.15)
            mode = 'hard'
            DEALER = dhbj_class_module.Player('Dealer', cards = [], balance = 20000)
            break
        elif ans == '!':
            _ = os.system('cls & color 0e')
            print('===Python DealerRaid Blackjack===\n        Bankrupt the Dealer!\n\n')
            print('Are you?\n')
            mode = 'lucky'
            DEALER = dhbj_class_module.Player('Dealer', cards = [], balance = 777777)
            break
        elif ans == '?':
            _ = os.system('cls')
            print('===Python DealerRaid Blackjack===\n        Bankrupt the Dealer!\n\n')
            print('• Instructions\n\n')
            manual = open('instructions.txt')
            _ = manual.seek(0)
            print(f'{manual.read()}')
            manual.close()
            input('Press Enter to return...')
            _ = os.system('cls')
            print('===Python DealerRaid Blackjack===\n        Bankrupt the Dealer!\n\n')
        elif ans == 'X':
            input('Okay bye...')
            _ = os.system('cls & color 0f')
            quit()
        else:
            print('Wrong input: Try again\n')
    input('Press Enter to begin...')
    _ = os.system('cls')
    PLAYER = {} # The dictionary of all the players that are left in the game
    while mode != 'lucky': # Decide number of players to play
        try:
            if mode == 'hard':
                PLAYERS = int(input('How many players?(1~6)\n'))
            else:
                PLAYERS = int(input('How many players?(1~4)\n'))
        except:
            print('Wrong input: Try again\n')
        else:
            if mode == 'hard' and PLAYERS in list(range(1,7)):
                if PLAYERS == 1:
                    print(f'Starts as {PLAYERS} player')
                else:
                    print(f'Starts as {PLAYERS} players')
                break
            elif mode != 'hard' and PLAYERS in list(range(1,5)):
                if PLAYERS == 1:
                    print(f'Starts as {PLAYERS} player')
                else:
                    print(f'Starts as {PLAYERS} players')
                break
            else:
                print('Out of range: Try again\n')
    if mode == 'lucky':
        while True:
            player_name = input(f"Input Player's name: ")
            if player_name == '':
                print('Name needs to be at least a letter long')
            else:
                break
        if player_name.endswith('s'): # Prevents the s evaporation when stripping _split
            player_name += ' '
        PLAYER[player_name] = dhbj_class_module.Player(f'{player_name}', [], 10000, 0, False)
    else:
        num = 1
        while PLAYERS >= num:
            while True:
                player_name = input(f"Input Player {num}'s name: ")
                if len(PLAYER) != 0:
                    det = False
                    for player in PLAYER.values():
                        if player_name == player.name:
                            det = True
                    if det:
                        print('Name already taken: Try a different name')
                    elif player_name == '':
                        print('Name needs to be at least a letter long')
                    else:
                        break
                elif player_name == '':
                    print('Name needs to be at least a letter long')
                else:
                    break
            if player_name.endswith('s'): # Prevents the s evaporation when stripping _split
                player_name += ' '
            PLAYER[player_name] = dhbj_class_module.Player(f'{player_name}', [], 1000, 0, False)
            num += 1

    game_set = False # True if one game is over. False if not.
    turn = 1
    while True:
        DECK = dhbj_class_module.Deck() # Refresh deck
        betting()
        proceed_turn()
        end_turn()
        sum_game()
        turn += 1
