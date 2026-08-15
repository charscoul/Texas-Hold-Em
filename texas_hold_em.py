import random
import numpy as np
from random import Random
from time import time


""" Section 1: Defining global constants and functions"""


def unique_list(input_list: list) -> list:
    """Custom function to find the unique items within a list, maintaining order

        floats of the same value as ints are considered different items"""

    unique = []
    for item in input_list:
        if item not in unique:
            unique.append(item)
        else:
            if type(item) != type(unique[unique.index(item)]):
                unique.append(item)

    return unique


def default_rows() -> tuple[str]:
    """Produces the top/ bottom edges and blank rows for the playing card"""
    edge = ' ------ '
    blank = '|      |'

    return edge, blank


SUIT_TO_EMOJI = {"H": "❤️", "D": "♦️", "S": "♠️", "C": "♣️"}
CARD_VALUES = ['2', '3', '4', '5', '6',
               '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_SUITS = ["H", "D", "S", "C"]
CARD_VALUES_RANKED = {'2': 13, '3': 12, '4': 11, '5': 10, '6': 9,
                      '7': 8, '8': 7, '9': 6, '10': 5, 'J': 4, 'Q': 3, 'K': 2, 'A': 1}
HAND_TYPES_RANKED = {"Royal Flush": 1,
                     "Straight Flush": 2,
                     "Four of a Kind": 3,
                     "Full House": 4,
                     "Flush": 5,
                     "Straight": 6,
                     "Three of a Kind": 7,
                     "Two Pair": 8,
                     "Pair": 9,
                     "High Card": 10}
CARD_VALUES_DESCRIBED = {'2': "Two", '3': "Three", '4': "Four", '5': "Five", '6': "Six",
                         '7': "Seven", '8': "Eight", '9': "Nine", '10': "Ten", 'J': "Jack", 'Q': "Queen", 'K': "King", 'A': "Ace"}
CARD_SUITS_DESCRIBED = {"H": "Hearts",
                        "D": "Diamonds", "S": "Spades", "C": "Clubs"}
CARD_ROWS = 7
POCKET_SIZE = 2
FLOP_SIZE = 3
TURN_SIZE = 4
RIVER_SIZE = 5
TABLE_SIZES = [FLOP_SIZE, TURN_SIZE, RIVER_SIZE]
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 8

"""Section 2: Defining card-based classes"""


class Card:
    """A playing card, represented by a value and a suit"""

    def __init__(self, value: str, suit: str):
        """Initiates a single instance of a card"""
        # validate input types
        if not isinstance(suit, str):
            raise TypeError("suit must be a string")
        if not isinstance(value, str):
            raise TypeError("value must be a string")

        # set core attributes form inputs
        self.value = value.upper()
        self.suit = suit.upper()

        # validate input types
        if not isinstance(self.suit, str):
            raise TypeError("suit must be a string")
        if not isinstance(self.value, str):
            raise TypeError("value must be a string")

        # validate input values
        if self.suit not in CARD_SUITS:
            raise ValueError("suit must be 'H', 'D', 'S' or 'C'")
        if self.value not in CARD_VALUES:
            raise ValueError("value must be '2', '3', '4', '5', '6', \
                             '7', '8', '9', '10', 'J', 'Q', 'K' or 'A'")

    @property
    def emoji(self) -> str:
        """Returns the emoji representation of the suit"""
        return SUIT_TO_EMOJI[self.suit]

    def __str__(self) -> str:
        return f"{CARD_VALUES_DESCRIBED[self.value]} of {CARD_SUITS_DESCRIBED[self.suit]}"

    def _get_detailed_rows(self) -> tuple[str]:
        """Produces the card string rows with the card details"""

        if self.value == "10":
            top_row = f'|   {self.value}{self.emoji}|'
            bottom_row = f'|{self.value}{self.emoji}   |'
        else:
            top_row = f'|    {self.value}{self.emoji}|'
            bottom_row = f'|{self.value}{self.emoji}    |'

        return top_row, bottom_row

    @property
    def format(self) -> tuple[str]:
        """Formats card details as a playing card"""
        edge, blank = default_rows()
        top, bottom = self._get_detailed_rows()

        return edge, top, blank, blank, blank, bottom, edge


class Deck:
    """A deck of cards"""

    def __init__(self):
        """Initiates an instance of a new deck"""
        self.cards = self.fresh_deck()
        self.burnt_cards = []

    def fresh_deck(self) -> list[Card]:
        """Assembles a fresh, ordered deck of cards

        ordered with aces high to align with card values for scoring"""

        return [Card(value, suit) for suit in CARD_SUITS for value in CARD_VALUES]

    def print_deck(self) -> None:
        """prints each card in a deck for debugging"""

        for card in self.cards:
            print(card)

    def shuffle(self, seed: int = time()) -> None:
        """Shuffles the deck of cards"""
        copied_deck = self.cards.copy()
        Random(seed).shuffle(copied_deck)

        self.cards = copied_deck

    def __str__(self) -> str:
        """returns a list of card strings"""
        return str([str(card) for card in self.cards])

    def burn(self) -> None:
        """removes a card from the deck and adds it to the burnt pile"""
        self.burnt_cards.append(self.cards.pop(0))

    def deal(self) -> Card:
        """Removes and returns the top card of the deck"""
        return self.cards.pop(0)


class CardGroup:
    """A collection of cards"""

    def __init__(self, cards: list[Card]):
        """Initializes an instance of a CardGroup"""
        self.cards = cards

        # Type Validate inputs
        if not isinstance(self.cards, list):
            raise TypeError("cards must be a list")
        if not all(isinstance(card, Card) for card in self.cards):
            raise TypeError("Every card in cards must be of type Card")

        # Value Validate inputs
        if self.cards != unique_list(self.cards):
            raise ValueError("Duplicate cards cannot exist")

        self.public = False

    def print(self) -> None:
        """Prints the cards, with an initial indentation if the cards are on the table (public view)"""

        # Validate printability:
        if len(self.cards) == 0:
            raise IndexError("No cards to print")

        print_list = []
        for _ in range(CARD_ROWS):
            if self.public:
                print_list.append("     ")
            else:
                print_list.append("")

        # add the card's details
        for card in self.cards:
            for i in range(CARD_ROWS):
                print_list[i] += card.format[i]
                if card is not self.cards[-1]:
                    print_list[i] += " "

        # print the list
        for line in print_list:
            print(line)

    def __str__(self) -> str:
        """returns the strings of the cards in order"""

        output = ""
        for card in self.cards:
            output += str(card)
            if card != self.cards[-1]:
                output += ", "

        return output


class Pocket(CardGroup):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)

        # additional length restrictions
        if len(self.cards) != POCKET_SIZE:
            raise ValueError("Pockets must contain exactly 2 cards")


class Table(CardGroup):
    def __init__(self, flop: list[Card]):
        super().__init__(flop)
        self.public = True

        # additional length restrictions
        if len(self.cards) not in TABLE_SIZES:
            raise ValueError("The table must contain 3, 4 or 5 cards")

    def _add_card(self, card: Card) -> None:
        """Adds a card to the table"""

        # validate inputs
        if not isinstance(card, Card):
            raise TypeError("Card must be of type Card")
        if card in self.cards:
            raise ValueError("Duplicate cards cannot exist")
        if len(self.cards) >= 5:
            raise ValueError("Cannot add cards to a full table")

        self.cards.append(card)


class Player:
    """A player in the tournament"""

    def __init__(self, current_indices: list[int], possible_names: list[str], seed: int = time()):
        """initiates an instance of a player"""

        # input type validations
        if not isinstance(current_indices, list):
            raise TypeError("current_indices must be a list")
        if not isinstance(possible_names, list):
            raise TypeError("possible names must be a list")
        if not all(isinstance(index, int) for index in current_indices):
            raise TypeError("all current indexes must be integers")
        if not all(isinstance(name, str) for name in possible_names):
            raise TypeError("all possible names must be integers")

        # input value validations
        if not all(index >= 0 for index in current_indices):
            raise ValueError("all possible indexes must be non-negative")
        if not all(len(name) in range(MIN_NAME_LENGTH, MAX_NAME_LENGTH) for name in possible_names):
            raise ValueError(
                f"all possible names must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} letters long")

        self.index = self._get_index(current_indices)
        self.name = self._get_name(possible_names, seed)
        self.pocket = None
        self.out = False

    def _get_name(self, name_list: list[str], seed: int = time()) -> str:
        """Randomly selects a name for the player from the list of possible names, and removes it from the possible names"""
        total_names = len(name_list)

        if total_names == 0:
            raise ValueError("No names remaining to select from")

        index = Random(seed).randint(0, total_names - 1)
        return name_list.pop(index)

    def _get_index(self, current_indices: list[int]) -> int:
        """Returns this player's index, and adds it to the global list of used indices"""
        if len(current_indices) == 0:
            highest = -1
        else:
            highest = max(current_indices)
        new_highest = highest + 1
        current_indices.append(new_highest)
        return new_highest

    def add_pocket(self, pocket: Pocket) -> None:
        """adds an inputted pocket as an attribute"""

        # type validations
        if not isinstance(pocket, Pocket):
            raise TypeError("pocket must be of class Pocket")

        self.pocket = pocket


class HumanPlayer(Player):
    """The human controlled player in the tournament"""

    def __init__(self, current_indices, bot_names: list[str], seed=time()):
        """Initiates an instance of a human controlled player"""
        super().__init__(current_indices, bot_names, seed)

    def _get_name(self, name_list: list[str], seed) -> str:
        """The player inputs their name

        if the name is in the possible names list, it gets removed from the list"""
        while True:
            attempt = input("What is your name? ").capitalize()

            if attempt in name_list:
                name_list.remove(attempt)
                return attempt

            if len(attempt) not in range(MIN_NAME_LENGTH, MAX_NAME_LENGTH):
                print(
                    f"Your must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters\nConsider using a nickname?\n")
                continue

            return attempt


class Dealer:
    """A helper class to deal cards to players"""

    def __init__(self, players: list[Player], seed: int = time()):
        """Initiates an instance of the dealer class"""

        self.players = players

        # Type validate inputs
        if not isinstance(self.players, list):
            raise TypeError("players must be a list")
        if not all(isinstance(player, Player) for player in self.players):
            raise TypeError("all players must be of class Player")

        self.deck = Deck()
        self.deck.shuffle(seed)
        self.table = None

    @property
    def still_in(self) -> list[int]:
        """returns the indices of the players still in the tournament"""

        output = []

        for player in self.players:
            if player.out is False:
                output.append(player.index)

        return output

    def _make_pockets(self) -> dict[int:Pocket]:
        """returns a dictionary of the pockets to assign"""
        if len(self.still_in) == 0:
            raise IndexError("No indexes available for remaining players")

        self.deck.burn()

        indexed_pocket_cards = {}

        # first pass
        for index in self.still_in:
            indexed_pocket_cards[index] = [self.deck.deal()]

        # second pass
        for index in self.still_in:
            indexed_pocket_cards[index].append(self.deck.deal())

        return {index: Pocket(indexed_pocket_cards[index]) for index in self.still_in}

    def deal_pockets(self) -> None:
        """deals the pockets to the players still in the tournament"""
        pockets = self._make_pockets()

        for index in self.still_in:
            self.players[index].add_pocket(pockets[index])

    def _deal_flop(self) -> None:
        """Creates a table, filled with the flop"""
        # validations
        if self.table is not None:
            raise ValueError("Cannot deal flop to an existing table")

        self.deck.burn()

        flop = []
        for _ in range(FLOP_SIZE):
            flop.append(self.deck.deal())

        self.table = Table(flop)

    def _deal_turn(self) -> None:
        """Adds a card to the flop"""
        # validations
        if not isinstance(self.table, Table):
            raise TypeError("table must be of type Table")
        if len(self.table.cards) != FLOP_SIZE:
            raise ValueError("Cannot deal turn to anything other than a flop")

        self.deck.burn()

        turn_card = self.deck.deal()

        self.table._add_card(turn_card)

    def _deal_river(self) -> None:
        """Adds a card to the turn"""
        # validations
        if not isinstance(self.table, Table):
            raise TypeError("table must be of type Table")
        if len(self.table.cards) != TURN_SIZE:
            raise ValueError("Cannot deal turn to anything other than a turn")

        self.deck.burn()

        river_card = self.deck.deal()

        self.table._add_card(river_card)

    def deal_to_table(self):
        """Deals to table appropriately depending on state of table"""

        if self.table is None:
            self._deal_flop()
        elif len(self.table.cards) == FLOP_SIZE:
            self._deal_turn()
        elif len(self.table.cards) == TURN_SIZE:
            self._deal_river()
        else:
            raise ValueError("Can only deal to empty table, flop or turn")


class Hand(CardGroup):
    """A playable hand, consisting of 5 cards, with the ability to score"""

    def __init__(self, cards: list[Card]):
        """Initiates an instance of a hand"""
        super().__init__(cards)

        # extra validations
        if len(self.cards) != 5:
            raise ValueError("Hands must contain exactly 5 cards")

        self.public = True

        # store functional attributes
        self._value_ranks = sorted([CARD_VALUES_RANKED[card.value]
                                    for card in self.cards])

        self._suits = [card.suit for card in self.cards]

        self._unique_ranks = unique_list(self._value_ranks)
        self._unique_count = len(unique_list)

        self.hand_type = None
        self.kickers = None

    @property
    def _flush(self) -> bool:
        """Returns a boolean for whether a hand is a flush"""
        first_suit = self._suits[0]

        if all([suit == first_suit for suit in self._suits]):
            return True

        return False

    @property
    def _straight(self) -> bool:
        """Returns a boolean for whether a hand is a straight"""
        if self._unique_count != 5:
            return False

        for i in range(len(self._value_ranks) - 1):
            if self._value_ranks[i] != self._value_ranks[i+1] - 1:
                return False

        return True

    def _test_royal_flush(self) -> bool:
        """tests for a hand being a royal flush, and updates hand type if true"""
        if self._flush and self._straight and min(self._value_ranks) == 1:
            self.hand_type = "Royal Flush"
            return True
        return False

    def _test_straight_flush(self) -> bool | tuple[int, None, None, None, None]:
        """tests for a hand being a straight flush, and updates hand type and kickers if true"""
        if self._flush and self._straight:
            self.hand_type = "Straight Flush"
            self.kickers = (min(self._value_ranks))
            return True
        return False

    def _test_two_unique(self) -> bool:
        """tests for a hand being full house or four of a kind, updates hand type and kickers if true """
        if self._unique_count != 2:
            return False

        rank_a = self._unique_ranks[0]
        rank_b = self._unique_ranks[1]
        count_a = self._value_ranks.count(rank_a)
        count_b = self._value_ranks.count(rank_b)

        if count_a == 4:
            self.hand_type = "Four of a Kind"
            self.kickers = (rank_a, rank_b)
            return True
        if count_b == 4:
            self.hand_type = "Four of a Kind"
            self.kickers = (rank_b, rank_a)
            return True
        if count_a == 3:
            self.hand_type = "Full House"
            self.kickers = (rank_a, rank_b)
            return True
        if count_b == 3:
            self.hand_type = "Full House"
            self.kickers = (rank_b, rank_a)
            return True

        raise ValueError(
            "Two unique card value ranks in hand but not full house or four of a kind")

    def _test_flush(self) -> bool:
        """updates hand type and kicker if hand is a flush"""
        if self._flush:
            self.hand_type = "Flush"
            self.kickers = (rank for rank in self._value_ranks)
            return True
        return False

    def _test_straight(self) -> bool:
        """updates hand type and kicker if hand is a straight"""
        if self._straight:
            self.hand_type = "Straight"
            self.kickers = (min(self._value_ranks))
            return True
        return False

    def _test_three_unique(self) -> bool:
        """tests for a hand being two pair or three of a kind, updates hand type and kickers if true"""
        if self._unique_count != 3:
            return False

        rank_a = self._unique_ranks[0]
        rank_b = self._unique_ranks[1]
        rank_c = self._unique_ranks[2]

        count_a = self._value_ranks.count(rank_a)
        count_b = self._value_ranks.count(rank_b)
        count_c = self._value_ranks.count(rank_c)

        if count_a == 3:
            self.hand_type = "Three of a Kind"
            self.kickers = (rank_a, rank_b, rank_c)
            return True
        if count_b == 3:
            self.hand_type = "Three of a Kind"
            self.kickers = (rank_b, rank_a, rank_c)
            return True
        if count_c == 3:
            self.hand_type = "Three of a Kind"
            self.kickers = (rank_c, rank_a, rank_b)
            return True

        if count_a == count_b == 2:
            self.hand_type = "Two Pair"
            self.kickers = (rank_a, rank_b, rank_c)
            return True
        if count_a == count_c == 2:
            self.hand_type = "Two Pair"
            self.kickers = (rank_a, rank_c, rank_b)
            return True
        if count_b == count_c == 2:
            self.hand_type = "Two Pair"
            self.kickers = (rank_b, rank_c, rank_a)
            return True

        raise ValueError(
            "Three unique card value ranks in hand but not three of a kind or two pair")

    def _test_pair(self) -> bool:
        """tests for a hand being a pair, updates hand type and kickers if true"""
        if self._unique_count != 4:
            return False

        duplicate_ranks = [
            rank for rank in self._value_ranks if self._value_ranks.count(rank) == 2]
        if len(duplicate_ranks) == 0:
            raise ValueError(
                "four unique card value ranks in hand but no pairs found")
        if len(duplicate_ranks) >= 2:
            raise ValueError(
                "four unique card value ranks in hand but multiple pairs found")

        self.hand_type = "Pair"
        self.kickers = (duplicate_ranks[0], rank for rank in self._value_ranks if rank != duplicate_ranks[0])
        return True

    def _test_high_card(self) -> bool:
        """tests for a hand being a high card, updates hand type and kickers if true"""

        if self._unique_count != 5:
            return False

        self.hand_type = "High Card"
        self.kickers = (rank for rank in self._value_ranks)
        return True

    def _find_type(self) -> None:
        """updates self.hand_type and self.kickers with correct information"""
        if self._test_royal_flush():
            return None
        if self._test_straight_flush():
            return None
        if self._test_two_unique():
            return None
        if self._test_flush():
            return None
        if self._test_straight():
            return None
        if self._test_three_unique():
            return None
        if self._test_pair():
            return None
        if self._test_high_card():
            return None

        raise RuntimeError("The hand was not identified as any hand type")

    def _get_score(self) -> tuple[object]:
        """Returns the score information for a hand"""
        pass


class Score:
    """A helper class that stores a hand's scoring information"""

    def __init__(self, hand_type: str, kickers: tuple[int] | None):
        """Initialises an instance of a score"""
        self.hand_type = hand_type
        self.kickers = kickers

        # validate inputs
        if not isinstance(hand_type, str):
            raise TypeError("hand type must be a string")
        if not isinstance(kickers, tuple) and kickers is not None:
            raise TypeError("kickers must be a tuple or None")

        if hand_type not in HAND_TYPES_RANKED.keys():
            raise ValueError("hand type not found in valid hand types")
        if len(kickers) > 5:
            raise ValueError("Cannot have more than 5 kickers")
        if len(kickers) == 0:
            raise ValueError(
                "cannot have empty kickers tuple, use None instead")


##############################

# Thoughts:
    # create CardGroup scorer method

    # create temporary card groups (pocket + table)
        # card group compare
        # find best hand and all that

    # dealer compare (find winner)

    # dealer nuts

##############################


macro_rankings = {"Royal Flush": 1,
                  "Straight Flush": 2,
                  "Four of a Kind": 3,
                  "Full House": 4,
                  "Flush": 5,
                  "Straight": 6,
                  "Three of a Kind": 7,
                  "Two Pair": 8,
                  "Pair": 9,
                  "High Card": 10}

values_scored = {14: 1,
                 13: 2,
                 12: 3,
                 11: 4,
                 10: 5,
                 9: 6,
                 8: 7,
                 7: 8,
                 6: 9,
                 5: 10,
                 4: 11,
                 3: 12,
                 2: 13}

values_described = {14: "Ace",
                    13: "King",
                    12: "Queen",
                    11: "Jack",
                    10: "10",
                    9: "9",
                    8: "8",
                    7: "7",
                    6: "6",
                    5: "5",
                    4: "4",
                    3: "3",
                    2: "2"}


def find_type(hand: list):
    value_strings = []
    suits = []
    values = []

    for card in hand:
        value_strings.append(card[0])
        suits.append(card[1])

    # convert value strings to numbers for ease of manipulation
    for value in value_strings:
        if value == "J":
            values.append(11)
        elif value == "Q":
            values.append(12)
        elif value == "K":
            values.append(13)
        elif value == "A":
            values.append(14)
        else:
            values.append(int(value))

    values = sorted(values)

    # check for flush status
    first_suit = suits[0]
    flush_status = True
    for suit in suits:
        if suit != first_suit:
            flush_status = False
            break

    # check for straight status
    unique_values = unique_list(values)
    unique_values.sort()
    unique_no = len(unique_values)

    straight_status = True
    highest = max(values)
    lowest = min(values)
    if highest - lowest != 4 or unique_no != 5:
        straight_status = False

    # identify straight flush/ royal flush
    if flush_status == True and straight_status == True:
        high_card_value = max(values)
        if high_card_value == 14:
            return ("Royal Flush")
        else:
            return ("Straight Flush", high_card_value)

    # identify straight
    elif straight_status == True:
        high_card_value = max(values)
        return ("Straight", high_card_value)

    # identify flush
    elif flush_status == True:
        return ("Flush", values)

    # check for four of a kind / full house
    if unique_no == 2:
        value_a = unique_values[0]
        value_b = unique_values[1]
        count_a = values.count(value_a)
        count_b = values.count(value_b)

        if count_a == 4:
            return ("Four of a Kind", value_a)
        elif count_b == 4:
            return ("Four of a Kind", value_b)
        elif count_a == 3:
            return ("Full House", value_a, value_b)
        elif count_b == 3:
            return ("Full House", value_b, value_a)
        else:
            print(
                "Error: 2 contained values but not full house or four of a kind, check code")
            print(hand)

    # check for 2 pair / three of a kind
    elif unique_no == 3:
        value_a = unique_values[0]
        value_b = unique_values[1]
        value_c = unique_values[2]

        count_a = values.count(value_a)
        count_b = values.count(value_b)
        count_c = values.count(value_c)

        if count_a == 3:
            return ("Three of a Kind", value_a, value_c, value_b)
        elif count_b == 3:
            return ("Three of a Kind", value_b, value_c, value_a)
        elif count_c == 3:
            return ("Three of a Kind", value_c, value_b, value_a)

        elif count_a == 2:
            if count_b == 2:
                return ("Two Pair", value_b, value_a, value_c)
            elif count_c == 2:
                return ("Two Pair", value_c, value_a, value_b)
            else:
                print(
                    "Error: 3 contained values including one pair, but not 2 pair, check code")
                print(hand)

        elif count_b == 2:
            if count_c == 2:
                return ("Two Pair", value_c, value_b, value_a)
            else:
                print(
                    "Error: 3 contained values including one pair, but not 2 pair, check code")
                print(hand)

        elif count_c == 2:
            print(
                "Error: 3 contained values including one pair, but not 2 pair, check code")
            print(hand)

        else:
            print("Error: 3 contained values but not 3 of a kind or 2 pair, check code")
            print(hand)

    # check for pair
    elif unique_no == 4:
        value_a = unique_values[0]
        value_b = unique_values[1]
        value_c = unique_values[2]
        value_d = unique_values[3]

        count_a = values.count(value_a)
        count_b = values.count(value_b)
        count_c = values.count(value_c)
        count_d = values.count(value_d)

        if count_a == 2:
            return ("Pair", value_a, [value_d, value_c, value_b])
        elif count_b == 2:
            return ("Pair", value_b, [value_d, value_c, value_a])
        elif count_c == 2:
            return ("Pair", value_c, [value_d, value_b, value_a])
        elif count_d == 2:
            return ("Pair", value_d, [value_c, value_b, value_a])
        else:
            print("Error: 4 contained values not including any pairs, check code")
            print(hand)

    # high card
    elif unique_no == 5:
        return ("High Card", values)

    else:
        print("Error: not 2,3,4 or 5 unique values???? check code")

# Score hand


def score_hand(hand: list):
    type_tuple = find_type(hand)
    hand_type = type_tuple[0]
    type_score = macro_rankings[hand_type]

    if hand_type == "Royal Flush":
        description = "Royal Flush"
        return (description, type_score, np.nan, np.nan, np.nan, np.nan, np.nan)

    elif hand_type in ["Straight Flush", "Four of a Kind", "Straight"]:
        high_card_value = type_tuple[1]
        high_card_score = values_scored[high_card_value]

        high_card_described = values_described[high_card_value]
        if "Straight" in hand_type:
            description = f"{high_card_described} high {hand_type}"
        else:
            description = f"Four {high_card_described}'s"

        return (description, type_score, high_card_score, np.nan, np.nan, np.nan, np.nan)

    elif hand_type == "Full House":
        three_value = type_tuple[1]
        two_value = type_tuple[2]

        three_score = values_scored[three_value]
        two_score = values_scored[two_value]

        three_described = values_described[three_value]
        two_described = values_described[two_value]

        description = f"Full House with three {three_described}'s and two {two_described}'s"
        return (description, type_score, three_score, two_score, np.nan, np.nan, np.nan)

    elif hand_type == "Three of a Kind":
        three_value = type_tuple[1]
        higher_single_value = type_tuple[2]
        lower_single_value = type_tuple[3]

        three_score = values_scored[three_value]
        higher_score = values_scored[higher_single_value]
        lower_score = values_scored[lower_single_value]

        three_described = values_described[three_value]

        description = f"Three {three_described}'s"

        return (description, type_score, three_score, higher_score, lower_score, np.nan, np.nan)

    elif hand_type in ["Flush", "High Card"]:
        values = type_tuple[1]

        high_card_value = values[4]
        high_card_described = values_described[high_card_value]

        if hand_type == "Flush":
            description = f"{high_card_described} high {hand_type}"
        else:
            description = f"{high_card_described} high"

        return (description, type_score, values_scored[values[4]], values_scored[values[3]], values_scored[values[2]], values_scored[values[1]], values_scored[values[0]])

    elif hand_type == "Two Pair":
        high_pair = type_tuple[1]
        low_pair = type_tuple[2]
        last_card = type_tuple[3]

        high_pair_described = values_described[high_pair]
        low_pair_described = values_described[low_pair]

        high_pair_score = values_scored[high_pair]
        low_pair_score = values_scored[low_pair]
        last_card_scored = values_scored[last_card]

        description = f"Two Pair: {high_pair_described}'s and {low_pair_described}'s"

        return (description, type_score, high_pair_score, low_pair_score, last_card_scored, np.nan, np.nan)

    elif hand_type == "Pair":
        pair_value = type_tuple[1]
        other_3 = type_tuple[2]
        next_highest = other_3[0]

        pair_described = values_described[pair_value]
        next_highest_described = values_described[next_highest]

        description = f"Pair of {pair_described}'s with a {next_highest_described} high"

        pair_score = values_scored[pair_value]

        return (description, type_score, pair_score, values_scored[other_3[0]], values_scored[other_3[1]], values_scored[other_3[2]], np.nan)

# Finding best current hand for specific player


def compare_hands(hand_1: list, hand_2: list, draw=False):
    score_1 = score_hand(hand_1)
    score_2 = score_hand(hand_2)

    for i in range(5):
        if score_1[i+1] < score_2[i+1]:
            if draw == False:
                return hand_1
            else:
                return False, hand_1
        elif score_1[i+1] > score_2[i+1]:
            if draw == False:
                return hand_2
            else:
                return False, hand_2
        else:
            continue
    if draw == False:
        return hand_1
    else:
        return True, hand_1, hand_2


def best_hand(pocket: list, table: list, draw=False):
    available_cards = []
    for card in pocket:
        available_cards.append(card)
    for card in table:
        available_cards.append(card)

    if len(available_cards) == 5:
        best_hand = available_cards
        return best_hand
    elif len(available_cards) == 6:
        hand_1 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[3], available_cards[4]]
        hand_2 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[3], available_cards[5]]
        hand_3 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[4], available_cards[5]]
        hand_4 = [available_cards[0], available_cards[1],
                  available_cards[3], available_cards[4], available_cards[5]]
        hand_5 = [available_cards[0], available_cards[2],
                  available_cards[3], available_cards[4], available_cards[5]]
        hand_6 = [available_cards[1], available_cards[2],
                  available_cards[3], available_cards[4], available_cards[5]]

        hands = [hand_1, hand_2, hand_3, hand_4, hand_5, hand_6]

    elif len(available_cards) == 7:
        hand_1 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[3], available_cards[4]]
        hand_2 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[3], available_cards[5]]
        hand_3 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[4], available_cards[5]]
        hand_4 = [available_cards[0], available_cards[1],
                  available_cards[3], available_cards[4], available_cards[5]]
        hand_5 = [available_cards[0], available_cards[2],
                  available_cards[3], available_cards[4], available_cards[5]]
        hand_6 = [available_cards[1], available_cards[2],
                  available_cards[3], available_cards[4], available_cards[5]]
        hand_7 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[3], available_cards[6]]
        hand_8 = [available_cards[0], available_cards[1],
                  available_cards[2], available_cards[4], available_cards[6]]
        hand_9 = [available_cards[0], available_cards[1],
                  available_cards[3], available_cards[4], available_cards[6]]
        hand_10 = [available_cards[0], available_cards[2],
                   available_cards[3], available_cards[4], available_cards[6]]
        hand_11 = [available_cards[1], available_cards[2],
                   available_cards[3], available_cards[4], available_cards[6]]
        hand_12 = [available_cards[0], available_cards[1],
                   available_cards[2], available_cards[5], available_cards[6]]
        hand_13 = [available_cards[0], available_cards[1],
                   available_cards[3], available_cards[5], available_cards[6]]
        hand_14 = [available_cards[0], available_cards[2],
                   available_cards[3], available_cards[5], available_cards[6]]
        hand_15 = [available_cards[1], available_cards[2],
                   available_cards[3], available_cards[5], available_cards[6]]
        hand_16 = [available_cards[0], available_cards[1],
                   available_cards[4], available_cards[5], available_cards[6]]
        hand_17 = [available_cards[0], available_cards[2],
                   available_cards[4], available_cards[5], available_cards[6]]
        hand_18 = [available_cards[1], available_cards[2],
                   available_cards[4], available_cards[5], available_cards[6]]
        hand_19 = [available_cards[0], available_cards[3],
                   available_cards[4], available_cards[5], available_cards[6]]
        hand_20 = [available_cards[1], available_cards[3],
                   available_cards[4], available_cards[5], available_cards[6]]
        hand_21 = [available_cards[2], available_cards[3],
                   available_cards[4], available_cards[5], available_cards[6]]

        hands = [hand_1, hand_2, hand_3, hand_4,
                 hand_5, hand_6, hand_7, hand_8, hand_9, hand_10, hand_11, hand_12, hand_13, hand_14, hand_15, hand_16, hand_17, hand_18, hand_19, hand_20, hand_21]

    winning_hand = None
    for hand in hands:
        if winning_hand == None:
            winning_hand = hand_1
        else:
            if draw == False:
                winning_hand = compare_hands(winning_hand, hand)

            else:
                comparison = compare_hands(winning_hand, hand, draw)
                if comparison[0] == False:
                    winning_hand = comparison[1]
                    current_draw = False
                else:
                    winning_hand = comparison[1]
                    tied_hand = comparison[2]
                    current_draw = True

    if draw == False:
        return winning_hand
    else:
        if current_draw == False:
            return False, winning_hand
        else:
            return True, winning_hand, tied_hand


# Finding the nuts


def find_nuts(table: list):
    not_tabled = game_deck()
    for card in table:
        not_tabled.remove(card)

    if len(table) == 3:
        best_hand = None
        for i in range(len(not_tabled)):
            for j in range(len(not_tabled)):
                if i < j:
                    current_hand = [table[0], table[1],
                                    table[2], not_tabled[i], not_tabled[j]]
                    if best_hand == None:
                        best_hand = current_hand
                    else:
                        best_hand = compare_hands(best_hand, current_hand)

        return (best_hand)

    elif len(table) == 4:
        best_hand = None
        for i in range(len(not_tabled)):
            for j in range(len(not_tabled)):
                if i < j:
                    for x in range(4):
                        current_hand = []
                        for y in range(4):
                            if x != y:
                                current_hand.append(table[y])

                        current_hand.append(not_tabled[i])
                        current_hand.append(not_tabled[j])

                        if best_hand == None:
                            best_hand = current_hand
                        else:
                            best_hand = compare_hands(best_hand, current_hand)

            current_hand = [table[0], table[1],
                            table[2], table[3], not_tabled[i]]
            best_hand = compare_hands(best_hand, current_hand)

    elif len(table) == 5:
        best_hand = None
        for i in range(len(not_tabled)):
            for j in range(len(not_tabled)):
                if i < j:
                    for x in range(5):
                        for y in range(5):
                            if x != y:
                                current_hand = []
                                for z in range(5):
                                    if z != x and z != y:
                                        current_hand.append(table[z])

                                current_hand.append(not_tabled[i])
                                current_hand.append(not_tabled[j])

                                if best_hand == None:
                                    best_hand = current_hand
                                else:
                                    best_hand = compare_hands(
                                        best_hand, current_hand)

            for x in range(5):
                current_hand = []
                for y in range(5):
                    if x != y:
                        current_hand.append(table[y])

                current_hand.append(not_tabled[i])

                best_hand = compare_hands(best_hand, current_hand)

        best_hand = compare_hands(best_hand, table)

    nuts = best_hand
    required = []
    for card in best_hand:
        if card not in table:
            required.append(card)

    return nuts, required

    # check for straight_flush / royal flush possibility
    # first identify any combination of 3 cards from table that are of same suit

    # then for each of those combinations, identify if the difference between highest and lowest value are

# Revealing hands and finding the winning hand given each remaining player's pockets and the river, provided the game makes it to that stage


def find_winner_comparison(pockets: dict, river: list):
    current_winner_name = None
    current_winning_hand = None
    current_tied_names = []
    current_tied_hands = []
    for player, pocket in pockets.items():
        players_winning_hand = best_hand(pocket, river)
        best_score = score_hand(players_winning_hand)

        print(f'Player {player}, had: ')
        print("")
        print_card_list(pocket, False)
        print("")
        print(f"Their best hand was {best_score[0]}")
        print("")
        print_card_list(players_winning_hand, True)

        if current_winning_hand == None:
            current_winning_hand = players_winning_hand
            current_winner_name = player
        else:
            winning_test = compare_hands(
                current_winning_hand, players_winning_hand, draw=True)

            if winning_test[0] == False:
                new_winning_hand = winning_test[1]

                if new_winning_hand != current_winning_hand:
                    current_winning_hand = new_winning_hand
                    current_winner_name = player
                    current_tied_hands = []
                    current_tied_names = []

            else:
                current_tied_names.append(player)
                current_tied_hands.append(players_winning_hand)

    if current_tied_names == []:
        print(f"{current_winner_name} won the hand!")
        return [current_winner_name]
    else:
        current_tied_names.append(current_winner_name)
        current_tied_hands.append(current_winning_hand)

        string = f"The hand was a tie between: "
        for i in range(len(current_tied_names)):
            if i == 0:
                string += f"{current_tied_names[i]}"
            elif i != len(current_tied_names) - 1:
                string += f", {current_tied_names[i]}"
            else:
                string += f" and {current_tied_names[i]}!"

        print(string)
        return current_tied_names


###
# Section 2: Defining the betting elements and the pot
###

# general set-up should be a list of dictionaries, with the list index equalling the player index. each dictionary should contain booleans for whether the player is the small blind, the big blind, whether the player has folded, their chip total, how much they are currently in for
def create_blank_list(player_count: int, buy_in: int):
    play_state_list = []
    for i in range(player_count):
        player_dict = {}
        player_dict["Small Blind"] = False
        player_dict["Big Blind"] = False
        player_dict["Dealer"] = False
        player_dict["Pre-flop First"] = False
        player_dict["Folded"] = False
        player_dict["All In"] = False
        player_dict["Chip Total"] = buy_in
        player_dict["Out"] = False
        player_dict["In For"] = 0
        player_dict["Played At Stake"] = False

        play_state_list.append(player_dict)

    return play_state_list

# Find list of player indexes for those still in tournament


def still_in_tourney(play_state_list: list):
    players_in = []
    for i in range(len(play_state_list)):
        if play_state_list[i]["Out"] == False:
            players_in.append(i)

    return players_in

# tracking dealer token and blinds (hand number refers to the point at which the full deck is restored)


def move_tokens(play_state_list: list, players_in: list, hand_number: int):
    rem = hand_number % len(players_in)

    dealer_index_index = rem - 1
    small_index_index = rem
    big_index_index = rem + 1
    pre_flop_first_index_index = rem + 2

    # form as index number
    if dealer_index_index >= len(players_in):
        dealer_index_index += -len(players_in)
    if small_index_index >= len(players_in):
        small_index_index += -len(players_in)
    if big_index_index >= len(players_in):
        big_index_index += -len(players_in)
    if pre_flop_first_index_index >= len(players_in):
        pre_flop_first_index_index += -len(players_in)

    dealer_index = players_in[dealer_index_index]
    small_index = players_in[small_index_index]
    big_index = players_in[big_index_index]
    pre_flop_first_index = players_in[pre_flop_first_index_index]

    play_state_list[small_index]["Small Blind"] = True
    play_state_list[big_index]["Big Blind"] = True
    play_state_list[dealer_index]["Dealer"] = True
    play_state_list[pre_flop_first_index]["Pre-flop First"] = True

    return play_state_list

# check


def check(play_state_list: list, player_index: int):

    play_state_list[player_index]["Played At Stake"] = True

    return play_state_list

# raising


def raise_bet(play_state_list: list, player_index: int, current_bet: int, last_raise_size: int, cap: int, bypass_type=None):

    if bypass_type == None:
        while True:
            raise_size = int(input(
                f"How much would you like to raise by (it has to be at least {last_raise_size}, and less than the highest possible raise of {cap - current_bet} chips)"))
            if raise_size >= last_raise_size and raise_size < cap - current_bet:
                break
            else:
                print(
                    f"Error: invalid raise, please enter a number greater than or equal to {last_raise_size}, but less than {cap - current_bet}")
    elif bypass_type == "Rand":
        min_raise = last_raise_size
        max_raise = play_state_list[player_index]["Chip Total"] - \
            (current_bet + 1)

        raise_size = random.randint(min_raise, max_raise)

    new_bet = current_bet + raise_size
    play_state_list[player_index]["In For"] = new_bet

    for i in range(len(play_state_list)):
        if i == player_index:
            play_state_list[player_index]["Played At Stake"] = True
        elif play_state_list[i]["All In"] == True or play_state_list[i]["Folded"] == True:
            play_state_list[i]["Played At Stake"] = True
        else:
            play_state_list[i]["Played At Stake"] = False

    return play_state_list, new_bet, raise_size

# Folding


def fold(play_state_list: list, player_index: int):
    play_state_list[player_index]["Folded"] = True

    play_state_list[player_index]["Played At Stake"] = True

    return play_state_list


# calling
def call(play_state_list: list, player_index: int, current_bet: int):
    play_state_list[player_index]["In For"] = current_bet

    play_state_list[player_index]["Played At Stake"] = True

    return play_state_list

# re-raising


def re_raise(play_state_list: list, player_index: int, current_bet: int, raise_size: int, cap: int, bypass_type=None):

    if bypass_type == None:
        while True:
            re_raise_size = int(input(
                f"How much would you like to raise by (it has to be at least {raise_size}, and less than the highest possible raise of {cap - current_bet} chips)"))
            if raise_size >= current_bet and raise_size < cap - current_bet:
                break
            else:
                print(
                    f"Error: invalid raise, please enter a number greater than or equal to {raise_size}, but less than {cap - current_bet}")
    elif bypass_type == "Rand":
        min_raise = raise_size
        max_raise = play_state_list[player_index]["Chip Total"] - \
            (current_bet + 1)

        re_raise_size = random.randint(min_raise, max_raise)

    new_bet = current_bet + re_raise_size
    raise_size = re_raise_size
    play_state_list[player_index]["In For"] = new_bet

    for i in range(len(play_state_list)):
        if i == player_index:
            play_state_list[player_index]["Played At Stake"] = True
        elif play_state_list[i]["All In"] == True or play_state_list[i]["Folded"] == True:
            play_state_list[i]["Played At Stake"] = True
        else:
            play_state_list[i]["Played At Stake"] = False

    return play_state_list, new_bet, raise_size

# all-in


def all_in(play_state_list: list, player_index: int, current_bet: int, raise_size: int):
    player_budget = play_state_list[player_index]["Chip Total"]

    play_state_list[player_index]["All In"] = True
    play_state_list[player_index]["In For"] = player_budget

    if player_budget >= current_bet:
        new_bet = player_budget
        raise_size = new_bet - current_bet

        for i in range(len(play_state_list)):
            if i == player_index:
                play_state_list[player_index]["Played At Stake"] = True
            elif play_state_list[i]["All In"] == True or play_state_list[i]["Folded"] == True:
                play_state_list[i]["Played At Stake"] = True
            else:
                play_state_list[i]["Played At Stake"] = False

    else:
        new_bet = current_bet

        play_state_list[player_index]["Played At Stake"] = True

    return play_state_list, new_bet, raise_size

# Take chips from players to put into pots (do at end of hand, before deciding winner)


def take_chips(play_state_list: list):
    for i in range(len(play_state_list)):
        play_state_list[i]["Chip Total"] += (0 - play_state_list[i]["In For"])

    return play_state_list

# Form dictionary of pots and the players eligible to win the money in those pots


def form_pots(play_state_list: list, highest_bet: int):
    pots = {}

    highest_bets = [highest_bet]
    for i in range(len(play_state_list)):
        if play_state_list[i]["All In"] == True and play_state_list[i]["In For"] not in highest_bets:
            highest_bets.append(play_state_list[i]["In For"])

    highest_bets = sorted(highest_bets)
    pot_count = len(highest_bets)

    while True:
        if pot_count == 1:
            main_pot = 0
            main_competitors = []
            for i in range(len(play_state_list)):
                player_in_for = play_state_list[i]["In For"]
                if player_in_for >= highest_bets[0]:
                    main_pot += highest_bets[0]
                else:
                    main_pot += player_in_for

                if player_in_for >= highest_bets[0]:
                    main_competitors.append(i)

            pots["Main Pot"] = (main_pot, main_competitors)

            break

        else:
            pot_bet = highest_bets[- 1]
            below_pot_bet = highest_bets[-2]
            pot_name = f"Side Pot {pot_count - 1}"

            pot_value = 0
            pot_competitors = []

            for i in range(len(play_state_list)):

                if play_state_list[i]["In For"] > below_pot_bet:
                    player_extra = min(
                        pot_bet, play_state_list[i]["In For"] - below_pot_bet)
                    pot_value += player_extra

                    if player_extra >= 0:
                        pot_competitors.append(i)

            pots[pot_name] = (pot_value, pot_competitors)

            pot_count = pot_count - 1

    print(pots)
    return pots

# decide winnings


def decide_winnings_by_hand(pots: dict, pockets: dict, river: list):
    winnings_list = []

    for pot_name, pot_details in pots.items():
        pot_value = pot_details[0]
        pot_competitors = pot_details[1]

        sub_pockets = {}
        for player_index in pot_competitors:
            sub_pockets[player_index] = pockets[player_index]

        print(f"Playing for the {pot_name} are {pot_competitors}")
        print("")
        pot_winners = find_winner_comparison(sub_pockets, river)

        winnings_per_winner = pot_value // len(pot_winners)
        winnings_tuple = (pot_winners, winnings_per_winner)

        winnings_list.append(winnings_tuple)

    return winnings_list


def is_last_man_standing(play_state_list: list):
    still_in_count = 0
    for i in range(len(play_state_list)):
        if play_state_list[i]["Folded"] == False and play_state_list[i]["Out"] == False:
            still_in_count += 1

    if still_in_count <= 0:
        print("Error, no players remaining?")
    elif still_in_count > 1:
        return False
    else:
        return True


def decide_winnings_by_last(play_state_list: list):
    still_in = still_in_tourney(play_state_list)

    winnings = 0
    for i in still_in:
        winnings += play_state_list[i]["In For"]

        if play_state_list[i]["Folded"] == False and play_state_list[i]["Out"] == False:
            winner = i

    print("")
    print(f"{i} wins, as all active players have folded")
    print("")

    return [([winner], winnings)]


def apply_winnings(play_state_list: list, winnings_list: list):
    for winnings_tuple in winnings_list:
        winners = winnings_tuple[0]
        winnings = winnings_tuple[1]

        for winner in winners:
            play_state_list[winner]["Chip Total"] += winnings

    return play_state_list

# reset play_state (except chip_total, Out)


def post_winnings_reset(play_state_list: list):
    for i in range(len(play_state_list)):
        play_state_list[i]["Small Blind"] = False
        play_state_list[i]["Big Blind"] = False
        play_state_list[i]["Dealer"] = False
        play_state_list[i]["Pre-flop First"] = False
        play_state_list[i]["Folded"] = False
        play_state_list[i]["All In"] = False
        play_state_list[i]["In For"] = 0
        play_state_list[i]["Played At Stake"] = False

        if play_state_list[i]["Chip Total"] <= 0:
            play_state_list[i]["Out"] = True

    return play_state_list

# find available actions for a player, return as a dictionary keyed by number 1+, each corresponding to an action, or return True to trigger next deal / winner check, or false to skip player (folded /out)


def find_possible_actions(play_state_list: list, player_index: int, current_bet: int, min_raise_size: int):
    possible = {}
    action_counter = 1
    if play_state_list[player_index]["Played At Stake"] == True:
        return True, None
    elif play_state_list[player_index]["Folded"] == True or play_state_list[player_index]["Out"] == True or play_state_list[player_index]["All In"] == True:
        return False, None
    else:
        player_in_for = play_state_list[player_index]["In For"]
        player_budget = play_state_list[player_index]["Chip Total"]
        other_players_highest_budget = 0
        cap = find_cap(play_state_list)

        if player_in_for == current_bet:
            possible[action_counter] = "Check"
            action_counter += 1

            if current_bet + min_raise_size < player_budget and current_bet + min_raise_size < cap:
                possible[action_counter] = "Raise"
                action_counter += 1

            if player_budget <= cap:
                possible[action_counter] = "All In"
                action_counter += 1

        elif player_in_for < current_bet:
            possible[action_counter] = "Fold"
            action_counter += 1

            if current_bet < player_budget:
                possible[action_counter] = "Call"
                action_counter += 1

                if current_bet + min_raise_size < player_budget and current_bet + min_raise_size < cap:
                    possible[action_counter] = "Re-Raise"
                    action_counter += 1

            if player_budget <= cap:
                possible[action_counter] = "All In"
                action_counter += 1

        else:
            print("Error, player in for more than current bet")

        return possible, cap

# create function to find the raise cap


def find_cap(play_state_list: list, still_in=None):
    if still_in == None:
        still_in = still_in_tourney(play_state_list)

    # check if player's bet is at bet cap based on removing folders
    cap_without_folders = None
    highest_without_folders = None
    for index in still_in:
        if play_state_list[index]["Folded"] == False:
            if highest_without_folders == None:
                highest_without_folders = play_state_list[index]["Chip Total"]
            else:
                if cap_without_folders == None:
                    if highest_without_folders <= play_state_list[index]["Chip Total"]:
                        cap_without_folders = highest_without_folders
                        highest_without_folders = play_state_list[index]["Chip Total"]
                    else:
                        cap_without_folders = play_state_list[index]["Chip Total"]
                else:
                    if play_state_list[index]["Chip Total"] > highest_without_folders:
                        cap_without_folders = highest_without_folders
                        highest_without_folders = play_state_list[index]["Chip Total"]
                    elif play_state_list[index]["Chip Total"] > cap_without_folders:
                        cap_without_folders = play_state_list[index]["Chip Total"]

    return cap_without_folders


# choose and execute action from possible dictionary

def player_choose_and_act(possible_actions_dict: dict, play_state_list: list, player_index: int, current_bet: int, min_raise_size: int, cap: int):
    string = "What action would you like to take? ("
    for key, action in possible_actions_dict.items():
        string += f"{key}: {action}"
        if key != max(possible_actions_dict.keys()):
            string += ", "
        else:
            string += ")"

    while True:
        attempt = int(input(string))
        if attempt not in possible_actions_dict.keys():
            print("Error, input not in the possible selection, please try again")
            continue
        else:
            action = possible_actions_dict[attempt]
            break

    print(f"{player_index} chose {action}")

    if action == "Check":
        play_state_list = check(play_state_list, player_index)
    elif action == "Raise":
        play_state_list, current_bet, min_raise_size = raise_bet(
            play_state_list, player_index, current_bet, min_raise_size, cap)
    elif action == "Call":
        play_state_list = call(play_state_list, player_index, current_bet)
    elif action == "Re-Raise":
        play_state_list, current_bet, min_raise_size = re_raise(
            play_state_list, player_index, current_bet, min_raise_size, cap)
        print(f"The current bet is now {current_bet}")
        print(f"The minimum raise amount is now {min_raise_size}")
    elif action == "All In":
        play_state_list, current_bet, min_raise_size = all_in(
            play_state_list, player_index, current_bet, min_raise_size)
        print(f"The current bet is now {current_bet}")
        print(f"The minimum raise amount is now {min_raise_size}")
    elif action == "Fold":
        play_state_list = fold(play_state_list, player_index)

    return play_state_list, current_bet, min_raise_size


def random_choose_and_act(possible_actions_dict: dict, play_state_list: list, player_index: int, current_bet: int, min_raise_size: int, cap: int):
    keys = possible_actions_dict.keys()

    random_attempt = random.randint(min(keys), max(keys))

    action = possible_actions_dict[random_attempt]

    print(f"{player_index} chose {action}")

    if action == "Check":
        play_state_list = check(play_state_list, player_index)
    elif action == "Raise":
        play_state_list, current_bet, min_raise_size = raise_bet(
            play_state_list, player_index, current_bet, min_raise_size, cap, bypass_type="Rand")
    elif action == "Call":
        play_state_list = call(play_state_list, player_index, current_bet)
    elif action == "Re-Raise":
        play_state_list, current_bet, min_raise_size = re_raise(
            play_state_list, player_index, current_bet, min_raise_size, cap, bypass_type="Rand")
        print(f"The current bet is now {current_bet}")
        print(f"The minimum raise amount is now {min_raise_size}")
    elif action == "All In":
        play_state_list, current_bet, min_raise_size = all_in(
            play_state_list, player_index, current_bet, min_raise_size)
        print(f"The current bet is now {current_bet}")
        print(f"The minimum raise amount is now {min_raise_size}")

    elif action == "Fold":
        play_state_list = fold(play_state_list, player_index)

    return play_state_list, current_bet, min_raise_size

# reset played at current bet before dealing the next stage


def reset_played_at(play_state_list: list, still_in=None):
    if still_in == None:
        still_in = still_in_tourney(play_state_list)

    # check if player's bet is at bet cap based on removing folders
    cap = find_cap(play_state_list, still_in)

    for index in still_in:
        if play_state_list[index]["Folded"] == False and play_state_list[index]["All In"] == False:
            if play_state_list[index]["In For"] >= cap:
                play_state_list[index]["Played At Stake"] = True
            else:
                play_state_list[index]["Played At Stake"] = False
        else:
            play_state_list[index]["Played At Stake"] = True

    return play_state_list

# determine whether all eligible players have played at current stake


def all_played_at(play_state_list: list, still_in=None):
    if still_in == None:
        still_in = still_in_tourney(play_state_list)

    all_played = True
    for index in still_in:
        if play_state_list[index]["Played At Stake"] == False:
            all_played = False
            return all_played

    return all_played

###
# Section 3: Creating the game to a basic level
###

# summarise the current gamestate


def post_hand_summary(play_state_list: list, player_index: int):
    player_row = "|      Player     |"
    status_row = "|      Status     |"
    in_for_row = "|      In For     |"
    remain_row = "| Remaining Chips |"

    for i in range(len(play_state_list)):
        player_string = f" {i} "
        if i == player_index:
            player_string += "(You) "

        if play_state_list[i]["Out"] == True:
            continue
        elif play_state_list[i]["Folded"] == True:
            status_string = " Folded "
        elif play_state_list[i]["All In"] == True:
            status_string = " All In "
        else:
            status_string = " In "

        in_for_string = " " + str(play_state_list[i]["In For"]) + " "
        remaining_string = " " + \
            str(play_state_list[i]["Chip Total"] -
                play_state_list[i]["In For"]) + " "

        string_list = [player_string, status_string,
                       in_for_string, remaining_string]
        lengths_list = []
        for entry in string_list:
            lengths_list.append(len(entry))
        max_width = max(lengths_list)

        for i in range(4):
            if lengths_list[i] != max_width:
                difference = max_width - lengths_list[i]

                half = difference // 2
                remainder = difference % 2

                h_adder = half * " "
                r_adder = remainder * " "

                string_list[i] = h_adder + string_list[i] + h_adder + r_adder

            lengths_list[i] = len(string_list[i])

        player_row = player_row + string_list[0] + "|"
        status_row = status_row + string_list[1] + "|"
        in_for_row = in_for_row + string_list[2] + "|"
        remain_row = remain_row + string_list[3] + "|"

    total_len = len(player_row)
    horizontal = ""
    for i in range(total_len):
        horizontal += "-"

    print("")
    print(player_row)
    print(horizontal)
    print(status_row)
    print(in_for_row)
    print(remain_row)
    print("")


# temporary function to print information for debugging

def debug(play_state_list: list, current_bet: int):
    for i in range(len(play_state_list)):
        if play_state_list[i]["Out"] == True:
            print(f"{i} is Out of the tournament")
        elif play_state_list[i]["Folded"] == True:
            print(
                f"{i} has folded, they were in for {play_state_list[i]['In For']}, it is {play_state_list[i]['Played At Stake']} that they have played at {current_bet}")
        elif play_state_list[i]["All In"] == True:
            print(
                f"{i} is all in, they are in for {play_state_list[i]['In For']}, it is {play_state_list[i]['Played At Stake']} that they have played at {current_bet}")
        else:
            print(
                f"{i} is is in for {play_state_list[i]['In For']}, it is {play_state_list[i]['Played At Stake']} that they have played at {current_bet}")

# Play hand with random opponent behaviors (to be fixed later) and with fresh buy-ins, not tracking player budgets


def basic_play_hand(play_state_list=None, player_count=4, buy_ins=100, small_blind=1, hand_number=0, player_index=0):
    full_deck = game_deck()
    big_blind = 2 * small_blind

    if play_state_list == None:
        play_state_list = create_blank_list(player_count, buy_ins)
        all_indexes = []
        for i in range(len(play_state_list)):
            all_indexes.append(i)
        play_state_list = move_tokens(
            play_state_list, all_indexes, hand_number)

    still_in = still_in_tourney(play_state_list)
    if player_index not in still_in:
        print("You are out of the tournament :(")
        player_out = True
    else:
        player_out = False

    # force blinds
    for index in still_in:
        if play_state_list[index]["Small Blind"] == True:
            if play_state_list[index]["Chip Total"] > small_blind:
                print(f"{index} is the small blind and bets {small_blind}")
                play_state_list[index]["In For"] = small_blind
            else:
                print(
                    f"{index} is the small blind, but they only have {play_state_list[index]['Chip Total']}, so. they are all in!")
                play_state_list[index]["In For"] = play_state_list[index]["Chip Total"]
                play_state_list[index]["All In"] = True

        elif play_state_list[index]["Big Blind"] == True:
            if play_state_list[index]["Chip Total"] > big_blind:
                print(f"{index} is the big blind and bets {big_blind}")
                play_state_list[index]["In For"] = big_blind
            else:
                print(
                    f"{index} is the big blind, but they only have {play_state_list[index]['Chip Total']}, so. they are all in!")
                play_state_list[index]["In For"] = play_state_list[index]["Chip Total"]
                play_state_list[index]["All In"] = True
        if play_state_list[index]["Pre-flop First"] == True:
            starter_index = index

    current_bet = big_blind
    min_raise_size = big_blind

    # deal pockets
    print("")
    input("Press enter to deal everybody's pockets")
    print("")

    pockets = deal_pockets(
        full_deck, [], still_in)

    if player_out == False:
        print("Your Cards")
        print("")
        print_card_list(pockets[player_index], False)
        print("")

    # pre-flop betting (Start w/ player after big blind)
    first_pass = True
    pre_flop_over = False
    while True:
        # debug(play_state_list, current_bet)

        # start betting w /starting player
        for index in still_in:
            possible_actions, cap = find_possible_actions(
                play_state_list, index, current_bet, min_raise_size)
            if isinstance(possible_actions, bool):
                if all_played_at(play_state_list, still_in) == True:
                    pre_flop_over = True
                    break
                else:
                    continue

            if first_pass == True and index == starter_index:
                first_pass = False

            if first_pass == False:
                print("")
                if index == player_index:
                    post_hand_summary(play_state_list, player_index)
                    print("")
                    play_state_list, current_bet, min_raise_size = player_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)

                else:
                    play_state_list, current_bet, min_raise_size = random_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)
                print("")

            # debug(play_state_list, current_bet)
        if pre_flop_over == True:
            print("")
            print("Pre-flop betting is complete")
            print("")
            break

    # see if someone won, if not move on
    if is_last_man_standing(play_state_list) == True:
        play_state_list = take_chips(play_state_list)
        winnings_list = decide_winnings_by_last(play_state_list)
        play_state_list = apply_winnings(play_state_list, winnings_list)
        play_state_list = post_winnings_reset(play_state_list)
        return play_state_list
    else:
        play_state_list = reset_played_at(play_state_list, still_in)
        # debug(play_state_list, current_bet)

    # deal flop
    print("")
    input("Press enter to deal the flop")
    print("")
    remaining_deck, burnt_cards, flop = deal_flop(remaining_deck, burnt_cards)

    print("Table:")
    print("")
    print_card_list(flop, True)
    print("")

    if player_out == False and play_state_list[player_index]["Folded"] == False:
        print("Your Cards:")
        print("")
        print_card_list(pockets[player_index], False)

        players_best = best_hand(pockets[player_index], flop)
        best_score = score_hand(players_best)
        best_description = best_score[0]
        print("")
        print(f"Your best hand is {best_description}")
        print("")

    # flop betting (Start w/ small blind)

    first_pass = True
    flop_over = False
    all_false_at_start = False
    while True:
        # start betting w /starting player
        for index in still_in:

            if first_pass == True and play_state_list[index]["Small Blind"] == True:
                first_pass = False

            possible_actions, cap = find_possible_actions(
                play_state_list, index, current_bet, min_raise_size)

            if isinstance(possible_actions, bool):
                if all_played_at(play_state_list, still_in) == True:
                    flop_over = True
                    break
                else:
                    continue

            if first_pass == False:
                print("")
                if index == player_index:
                    post_hand_summary(play_state_list, player_index)
                    print("")
                    play_state_list, current_bet, min_raise_size = player_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)

                else:
                    play_state_list, current_bet, min_raise_size = random_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)
                print("")

            # debug(play_state_list, current_bet)

        if flop_over == True:
            print("")
            print("Betting on the flop is complete")
            print("")
            break

    # see if someone won, if not move on
    if is_last_man_standing(play_state_list) == True:
        play_state_list = take_chips(play_state_list)
        winnings_list = decide_winnings_by_last(play_state_list)
        play_state_list = apply_winnings(play_state_list, winnings_list)
        play_state_list = post_winnings_reset(play_state_list)
        return play_state_list
    else:
        play_state_list = reset_played_at(play_state_list, still_in)
        # debug(play_state_list, current_bet)

    # deal turn
    print("")
    input("Press enter to deal the turn")
    print("")
    remaining_deck, burnt_cards, turn = deal_turn(
        remaining_deck, burnt_cards, flop)

    print("Table:")
    print("")
    print_card_list(turn, True)
    print("")

    if player_out == False and play_state_list[player_index]["Folded"] == False:

        print("Your Cards:")
        print("")
        print_card_list(pockets[player_index], False)

        players_best = best_hand(pockets[player_index], turn)
        best_score = score_hand(players_best)
        best_description = best_score[0]
        print("")
        print(f"Your best hand is {best_description}")
        print("")

    # turn betting

    first_pass = True
    turn_over = False
    while True:
        # debug(play_state_list, current_bet)
        # start betting w /starting player
        for index in still_in:
            if first_pass == True and play_state_list[index]["Small Blind"] == True:
                first_pass = False

            possible_actions, cap = find_possible_actions(
                play_state_list, index, current_bet, min_raise_size)
            if isinstance(possible_actions, bool):
                if all_played_at(play_state_list, still_in) == True:
                    turn_over = True
                    break
                else:
                    continue

            if first_pass == False:
                print("")
                if index == player_index:
                    post_hand_summary(play_state_list, player_index)
                    print("")
                    play_state_list, current_bet, min_raise_size = player_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)

                else:
                    play_state_list, current_bet, min_raise_size = random_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)
                print("")

            # debug(play_state_list, current_bet)
        if turn_over == True:
            print("")
            print("Betting on the turn is complete")
            print("")
            break

    # see if someone won, if not move on
    if is_last_man_standing(play_state_list) == True:
        play_state_list = take_chips(play_state_list)
        winnings_list = decide_winnings_by_last(play_state_list)
        play_state_list = apply_winnings(play_state_list, winnings_list)
        play_state_list = post_winnings_reset(play_state_list)
        return play_state_list
    else:
        play_state_list = reset_played_at(play_state_list, still_in)
        # debug(play_state_list, current_bet)

    # deal river
    print("")
    input("Press enter to deal the river")
    print("")
    remaining_deck, burnt_cards, river = deal_river(
        remaining_deck, burnt_cards, turn)

    print("Table:")
    print("")
    print_card_list(river, True)
    print("")

    if player_out == False and play_state_list[player_index]["Folded"] == False:
        print("Your Cards:")
        print("")
        print_card_list(pockets[player_index], False)

        players_best = best_hand(pockets[player_index], river)
        best_score = score_hand(players_best)
        best_description = best_score[0]
        print("")
        print(f"Your best hand is {best_description}")
        print("")

    # river betting
    first_pass = True
    river_over = False
    while True:
        # debug(play_state_list, current_bet)
        # start betting w /starting player
        for index in still_in:
            if first_pass == True and play_state_list[index]["Small Blind"] == True:
                first_pass = False

            possible_actions, cap = find_possible_actions(
                play_state_list, index, current_bet, min_raise_size)
            if isinstance(possible_actions, bool):
                if all_played_at(play_state_list, still_in) == True:
                    river_over = True
                    break
                else:
                    continue

            if first_pass == False:
                print("")
                if index == player_index:
                    post_hand_summary(play_state_list, player_index)
                    print("")
                    play_state_list, current_bet, min_raise_size = player_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)

                else:
                    play_state_list, current_bet, min_raise_size = random_choose_and_act(
                        possible_actions, play_state_list, index, current_bet, min_raise_size, cap)
                print("")

            # debug(play_state_list, current_bet)
        if river_over == True:
            print("")
            print("Betting is complete")
            print("")
            break

    # see if someone won, if not move on
    if is_last_man_standing(play_state_list) == True:
        play_state_list = take_chips(play_state_list)
        winnings_list = decide_winnings_by_last(play_state_list)
        play_state_list = apply_winnings(play_state_list, winnings_list)
        play_state_list = post_winnings_reset(play_state_list)
        return play_state_list

    # set up pots and take funds
    max_bet = 0
    for i in range(player_count):
        if play_state_list[i]["In For"] > max_bet:
            max_bet = play_state_list[i]["In For"]

    pots = form_pots(play_state_list, max_bet)

    play_state_list = take_chips(play_state_list)

    # for each pot, find winner by comparison, apply winnings
    winnings_list = decide_winnings_by_hand(pots, pockets, river)
    play_state_list = apply_winnings(play_state_list, winnings_list)
    play_state_list = post_winnings_reset(play_state_list)
    return play_state_list


# play tournament with random opponent behaviours (to be improved later), tracking player budgets

def basic_play_tournament():
    player_count = int(input("How many players are there? "))
    buy_ins = int(input("What are the buy ins? "))
    play_state_list = create_blank_list(player_count, buy_ins)

    small_blind = int(buy_ins / 100)

    hand_number = 1
    player_index = random.randint(0, player_count - 1)
    print(f"You are player index {player_index}")

    post_hand_summary(play_state_list, player_index)

    player_out = False
    spectator = False
    while True:
        print("")
        print(f"Hand Number {hand_number}: ")
        print("")

        still_in = still_in_tourney(play_state_list)

        play_state_list = move_tokens(
            play_state_list, still_in, hand_number)

        print("")
        input("Press enter to start the hand")
        print("")

        play_state_list = basic_play_hand(
            play_state_list, player_count, buy_ins, small_blind, hand_number, player_index)

        # eliminate busted players
        for i in range(len(play_state_list)):
            if play_state_list[i]["Chip Total"] == 0 or play_state_list[i]["Out"] == True:
                play_state_list[i]["Out"] = True

                if i == player_index and player_out == False:
                    while True:
                        yn = input(
                            "You are out, would you like to spectate the rest of the tournament? (Y/N) ")
                        yn = yn.upper()
                        if yn == "Y":
                            player_out = True
                            spectator = True
                            break
                        elif yn == "N":
                            player_out = True
                            break
                        else:
                            print("Invalid input, try again")
                            continue

                    if player_out == True and spectator == False:
                        print(
                            f"Wow, You're a sore loser, you played {hand_number} hands")
                        break
                    else:
                        print(
                            f"Unlucky, you made it to hand {hand_number}, lets see who wins the tournament!")
                elif i in still_in:
                    print(f"{i} is now out!")

        if player_out == True and spectator == False:
            break

        post_hand_summary(play_state_list, player_index)

        # count remaining players
        still_in = still_in_tourney(play_state_list)
        if len(still_in) == 1:
            print("We have a winner!")

            if player_index in still_in:
                print("Congrats, You Won!!!")
                print(
                    f"You beat {player_count - 1} players in {hand_number} rounds!")

            else:
                print(f"Player {still_in[0]} won!")
                print("Better luck next time!")

            break

        hand_number += 1


###
# Section 4: Opponent behaviors
###

# Determining 'aggressiveness' (willingness to bluff / attempts to price people out / calling of bluffs)

# determining quality of their hand

# determining what action they will take

# determining whether they will reveal cards


###
# tests & main function
###


def section_1_test():
    deck = game_deck()
    pockets = deal_pockets(deck, [], 4)
    player = 0

    print("Your Cards")
    print("")
    print_card_list(pockets[player], False)
    print("")
    input("Press anything to deal flop")
    print("")

    remaining_deck, burnt_cards, flop = deal_flop(remaining_deck, burnt_cards)
    print("Table:")
    print("")
    print_card_list(flop, True)
    print("")
    print("Your Cards:")
    print("")
    print_card_list(pockets[player], False)

    players_best = best_hand(pockets[player], flop)
    best_score = score_hand(players_best)
    best_description = best_score[0]
    print("")
    print(f"Your best hand is {best_description}")
    print("")

    input("Press anything to deal turn")
    print("")

    remaining_deck, burnt_cards, turn = deal_turn(
        remaining_deck, burnt_cards, flop)
    print("Table:")
    print("")
    print_card_list(turn, True)
    print("")
    print("Your Cards:")
    print("")
    print_card_list(pockets[player], False)

    players_best = best_hand(pockets[player], turn)
    best_score = score_hand(players_best)
    best_description = best_score[0]
    print("")
    print(f"Your best hand is {best_description}")
    print("")

    input("Press anything to deal river")
    print("")

    remaining_deck, burnt_cards, river = deal_river(
        remaining_deck, burnt_cards, turn)
    print("Table:")
    print("")
    print_card_list(river, True)
    print("")
    print("Your Cards:")
    print("")
    print_card_list(pockets[player], False)

    players_best = best_hand(pockets[player], river)
    best_score = score_hand(players_best)
    best_description = best_score[0]
    print("")
    print(f"Your best hand is {best_description}")
    print("")

    input("Press anything to find winner")
    print("")

    winners = find_winner_comparison(pockets, river)
    if player in winners:
        print("Congrats, you won!")
    else:
        print("better luck next time")
# test success


# test basic_play_hand
# print(basic_play_hand())
# test success


# test basic_play_tournament
# basic_play_tournament()
# test success based on

def main_game():
    print("It is recommended that you do not play this game on a dark background")
    print("")
    print("This is a basic version of texas hold 'em poker, where opponent bots take random betting actions based on the options available to them, with equal probability")
    print("A more advanced opponent betting strategy is being worked on, but this version serves to demonstrate the functionality of the game, the scoring, and the betting mechanics")
    print("")
    basic_play_tournament()


if __name__ == "__main__":
    # main_game()

    seed = 10

    no_indexes = []
    test_names = ["Barry", "Andy", "Mikey", "Sally", "Scotty", "Mary",
                  "Eddy", "Stevie", "Woody", "Julie", "Suzie", "Ruby", "Judy"]

    julie = Player(no_indexes, test_names, seed)
    suzie = Player(no_indexes, test_names, seed)
    judy = Player(no_indexes, test_names, seed)
    ruby = Player(no_indexes, test_names, seed)

    ladies = [julie, suzie, judy, ruby]

    test_dealer = Dealer(ladies, seed)

    pockets_dict = test_dealer._make_pockets()

    print(pockets_dict[0])
    print(pockets_dict[1])
    print(pockets_dict[2])
    print(pockets_dict[3])
