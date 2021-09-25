# blackjack.py
#   This program simulates playing blackjack.
# by: Scott Gordon

import random
import sys

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'


def main():
    print('***** Blackjack *****')

    money = 5000
    while True:
        if money <= 0:
            print("You're broke!")
            print("Thanks for playing!")
            sys.exit()

        print(f'Money {money}')
        bet = get_bet(money)

        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        print(f'Bet: {bet}')  # Players actions
        while True:
            display_hands(player_hand, dealer_hand, False)
            print()

            if get_hand_value(player_hand) > 21:
                break

            move = get_move(player_hand, money - bet)

            if move == 'D':
                additional_bet = get_bet(min(bet, (money - bet)))
                bet += additional_bet
                print(f'Bet increased to {bet}')
                print(f'Bet: {bet}')

            if move in ('H', 'D'):
                new_card = deck.pop()
                rank, suit = new_card
                print(f'You drew a {rank} or {suit}.')
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        if get_hand_value(player_hand) <= 21:  # Dealer action
            while get_hand_value(dealer_hand) < 17:
                print('Dealer hits...')
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)

                if get_hand_value(dealer_hand) > 21:
                    break
                input('Press Enter to continue...')

            display_hands(player_hand, dealer_hand, True)

            player_value = get_hand_value(player_hand)
            dealer_value = get_hand_value(dealer_hand)
            if dealer_value > 21:
                print(f'Dealer busts! You win {bet}')
                money += bet
            elif (player_value > 21) or (player_value < dealer_value):
                print('You lost!')
            elif player_value > dealer_value:
                print(f'You won {bet}')
                money += bet
            elif player_value == dealer_value:
                print('It\'s a tie, the bet is returned to you.')

            input('Press Enter to continue...')
            print('\n\n')


def get_bet(max_bet):
    '''Ask player how much they want to bet on round.'''
    while True:
        print(f'How much do you bet? (1-{max_bet}')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet


def get_deck():
    '''Return a list of (rank, suit) tuples for all 52 cards.'''
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    '''Show player and dealer cards. Hide dealer first card if 
    show_dealer_hand is False.'''
    print()
    if show_dealer_hand:
        print(f'DEALER: {get_hand_value(dealer_hand)}')
        display_cards(dealer_hand)
    else:
        print('DEALER: ???')
        display_cards([BACKSIDE] + dealer_hand[1:])

    print(f'PLAYER: {get_hand_value(player_hand)}')
    display_cards(player_hand)


def get_hand_value(cards):
    '''Return the value of the cards (function chooses best ace value).'''
    value = 0
    num_of_aces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            num_of_aces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    value += num_of_aces
    for i in range(num_of_aces):
        if value + 10 <= 21:
            value += 10

    return value


def display_cards(cards):
    '''Display the cards in the cards list.'''
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___ '
        if card == BACKSIDE:
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '|_##|'
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} |'
            rows[2] += f'| {suit} |'
            rows[3] += f'|_{rank.rjust(2)}|'

    for row in rows:
        print(row)


def get_move(player_hand, money):
    '''Ask player for move, return H for hit, S for stand
    and D for double down'''
    while True:
        moves = ['(H)it', '(S)tand']

        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')

        move_prompt = ', '.join(moves) + '> '
        move = input(move_prompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move


if __name__ == '__main__':
    main()
