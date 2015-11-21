import string, sys, math, random

DECK_SIZE = 52
SUIT_SIZE = 13
HAND_SIZE = 5
CLUBS = 'c'
DIAMONDS = 'd'
HEARTS = 'h'
SPADES = 's'
SUITS = {CLUBS:'0', DIAMONDS:'1', HEARTS:'2', SPADES:'3'}
SUITS_REVERSE_ASCII = {0:CLUBS, 1:DIAMONDS, 2:HEARTS, 3:SPADES}
JACK = 'j'
QUEEN = 'q'
KING = 'k'
ACE = 'a'
FACES = {JACK:'11', QUEEN:'12', KING:'13', ACE:'1'}
FACES_REVERSE = {11:JACK, 12:QUEEN, 13:KING, 1:ACE}

CLUBS_F = u'\u2663'
DIAMONDS_F = u'\u2662'
HEARTS_F = u'\u2661'
SPADES_F = u'\u2660'
SUITS_REVERSE_F = {0:CLUBS_F, 1:DIAMONDS_F, 2:HEARTS_F, 3:SPADES_F}
SUITS_REVERSE = SUITS_REVERSE_F

def card_string_to_int(str):
    """Takes a string represenation of a card and returns its integer code, 0-51"""
    def bad_card():
        print 'You entered a bad card :\'('
        sys.exit()

    clean_str = str.strip().lower()

    if len(clean_str) == 2 or len(clean_str) == 3:
        val_string = clean_str[:-1]

        if val_string in FACES:
            val_string = FACES[val_string]
        elif val_string not in string.digits[1:] and val_string != '10':
            bad_card()

        suit_string = clean_str[-1:]
        if suit_string in SUITS:
            suit_string = SUITS[suit_string]
        else:
            bad_card()

        val = int(val_string)
        suit = int(suit_string)

        return suit*SUIT_SIZE + val - 1

    else:
        bad_card()


def card_int_to_string(card):
    """Takes an integer representation of a card and returns its string name"""

    suit = card/SUIT_SIZE
    value = card%SUIT_SIZE + 1
    s = ''
    if value in FACES_REVERSE:
        s += FACES_REVERSE[value]
    else:
        s += str(value)
    if suit in SUITS_REVERSE:
        s += SUITS_REVERSE[suit]
    else:
        s += '?'

    return s.upper()

def decode_cards(cards):

    # Find the card in front of the biggest gap
    big_gap_card = find_biggest_gap(cards)[0]

    # Interpret the permutation of the cards
    step_size = read_permutation(cards)

    return (big_gap_card + step_size)%DECK_SIZE

def encode_cards(cards):

    # Find the card in front of the biggest gap
    (card_to_omit, permutation_number) = find_biggest_gap(cards)

    cards.remove(card_to_omit)

    # Permute the 4 remaining cards, and return them with the missing card
    return (make_permutation(cards, permutation_number),card_to_omit)


def find_biggest_gap(cards):
    """Given a list of cards this finds the card that
    sits at the beginning of the biggest gap.
    """
    sorted_cards = sorted(cards)
    num_cards = len(cards)

    # Find the card in front of the biggest gap
    biggest_gap = 0
    big_gap_card = 0
    for i in range(num_cards):
        this_diff = (sorted_cards[(i+1)%num_cards]-sorted_cards[i])%DECK_SIZE
        #print 'diff: ' + str(this_diff)
        if this_diff > biggest_gap:
            biggest_gap = this_diff
            big_gap_card = sorted_cards[i]

    i = sorted_cards.index(big_gap_card)
    gap_before_biggest = (big_gap_card - sorted_cards[(i-1)%num_cards])%DECK_SIZE

    return big_gap_card, gap_before_biggest


def read_permutation(cards):
    """Given a permutation of the cards, return the permutation number"""
    sorted_cards = sorted(cards)
    num_cards = len(cards)

    permutation_number = 1
    multiplier = math.factorial(num_cards) #This is 24 for 4 cards
    for card in cards:
        multiplier /= len(sorted_cards)
        p = sorted_cards.index(card)
        permutation_number += p*multiplier
        sorted_cards.remove(card)

    return permutation_number

def make_permutation(c, n):
    n -=1
    sorted_cards = sorted(c)
    output_cards = []
    num_cards = len(c)
    divisor = math.factorial(num_cards) #This is 24 for 4 cards
    while sorted_cards:
        divisor /= len(sorted_cards)
        d = n/divisor
        output_cards.append(sorted_cards.pop(d))
        n %= divisor

    return output_cards

def pick_random_cards(n):
    cards = []
    while len(cards) < n:
        new_card = random.randint(0, DECK_SIZE-1)
        if new_card not in cards:
            cards.append(new_card)
    return cards

def print_cards(cards):
    out_string = ''
    for card in cards:
        out_string += card_int_to_string(card) + ' '
    print out_string[:-1]

def print_card(card):
    print card_int_to_string(card)

def run_magic():
    print 'Welcome.'
    print 'Mode 1: I give you 4 cards and you guess the 5th.'
    print 'Mode 2: You give me 4 cards and I guess the 5th.'
    mode = raw_input('Choose mode now: ')

    if mode == '2':
        print 'Enter your cards separated by commas. E.g. \"4C, Jd, kH, as\"'
        card_strings = raw_input('Enter your cards: ').split(',')

        if len(card_strings) < 4:
            print 'Not enough cards :\'('
            sys.exit()

        if len(card_strings) > 4:
            print 'Too many cards :\'('
            sys.exit()

        cards = []
        for card_string in card_strings:
            cards.append(card_string_to_int(card_string))

        print_card(decode_cards(cards))

    if mode == '1':
        cards = pick_random_cards(HAND_SIZE)
        four_cards, one_card = encode_cards(cards)
        print_cards(four_cards)
        raw_input('\nPress RETURN to see the hidden card.')
        print_card(one_card)



def run_magic_test():
    print 'You\'ve entered TEST MODE.'
    print 'I will test every possible hand of 5 cards using my algorithms.'
    print 'Please wait...\n',
    n = (52*51*50*49*48)/(5*4*3*2*1)
    num_success = 0
    num_fail = 0
    for a in range(DECK_SIZE):
        for b in range(a+1, DECK_SIZE):
            for c in range(b+1, DECK_SIZE):
                for d in range(c+1, DECK_SIZE):
                    for e in range(d+1, DECK_SIZE):
                        cards = [a,b,c,d,e]

                        # Encode the 5 cards
                        four_cards, one_card = encode_cards(cards)

                        # Decode the results of the encoding
                        one_card_guess = decode_cards(four_cards)
                        
                        # Check the result of the decoding against the encoding
                        if one_card_guess == one_card:
                            num_success += 1
                        else:
                            num_fail += 1

                        # Display percentage complete
                        sys.stdout.write("\r{:.1%}".format(float(num_success+num_fail)/n))

    print '\nsuccess: ' + str(num_success) + '; fail: ' + str(num_fail)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        run_magic()
    elif sys.argv[1] == 'test':
        run_magic_test()
    elif sys.argv[1] == 'ascii':
        SUITS_REVERSE = SUITS_REVERSE_ASCII
        run_magic()
    else:
        run_magic()
