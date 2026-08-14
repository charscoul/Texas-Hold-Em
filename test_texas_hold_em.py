
from texas_hold_em import unique_list, default_rows, Card, Deck, CardGroup, Pocket, Table, burn_card, deal_card, deal_pockets, deal_flop, deal_turn, deal_river, deal_to_table
import pylint
import pytest


@pytest.fixture()
def ace_of_hearts() -> Card:
    return Card("A", "H")


@pytest.fixture()
def two_of_hearts() -> Card:
    return Card("2", "H")


@pytest.fixture()
def three_of_hearts() -> Card:
    return Card("3", "H")


@pytest.fixture()
def two_of_diamonds() -> Card:
    return Card("2", "D")


@pytest.fixture()
def seven_of_diamonds() -> Card:
    return Card("7", "D")


@pytest.fixture()
def jack_of_spades() -> Card:
    return Card("J", "S")


@pytest.fixture()
def ten_of_clubs() -> Card:
    return Card("10", "C")


@pytest.fixture()
def ace_of_clubs() -> Card:
    return Card("A", "C")


@pytest.fixture()
def jack_of_diamonds() -> Card:
    return Card("J", "D")


@pytest.fixture()
def new_deck() -> Deck:
    return Deck()


class TestCard:
    """Card initiation tests"""

    def test_non_str_value(self):
        with pytest.raises(TypeError):
            Card(7, "C")

    def test_non_letter_suit(self):
        with pytest.raises(ValueError):
            Card("7", "♦️")

    def test_success_1(self, ace_of_hearts):
        assert ace_of_hearts.suit == "H"
        assert ace_of_hearts.value == "A"

    def test_success_2(self, jack_of_spades):
        assert jack_of_spades.suit == "S"
        assert jack_of_spades.value == "J"

    def test_success_3(self, seven_of_diamonds):
        assert seven_of_diamonds.suit == "D"
        assert seven_of_diamonds.value == "7"

    def test_success_4(self, ten_of_clubs):
        assert ten_of_clubs.suit == "C"
        assert ten_of_clubs.value == "10"

    """Card emoji tests"""

    def test_emoji_1(self, ace_of_hearts):
        assert ace_of_hearts.emoji == "❤️"

    def test_emoji_2(self, jack_of_spades):
        assert jack_of_spades.emoji == "♠️"

    def test_emoji_3(self, seven_of_diamonds):
        assert seven_of_diamonds.emoji == "♦️"

    def test_emoji_4(self, ten_of_clubs):
        assert ten_of_clubs.emoji == "♣️"

    """Card string tests"""

    def test_string_1(self, ace_of_hearts):
        assert str(ace_of_hearts) == "Ace of Hearts"

    def test_string_2(self, jack_of_spades):
        assert str(jack_of_spades) == "Jack of Spades"

    def test_string_3(self, seven_of_diamonds):
        assert str(seven_of_diamonds) == "Seven of Diamonds"

    def test_string_4(self, ten_of_clubs):
        assert str(ten_of_clubs) == "Ten of Clubs"

    """Card format tests"""

    def test_format_1(self, ace_of_hearts):
        assert ace_of_hearts.format == (
            ' ------ ', '|    A❤️|',  '|      |', '|      |', '|      |', '|A❤️    |', ' ------ ')

    def test_format_2(self, jack_of_spades):
        assert jack_of_spades.format == (
            ' ------ ', '|    J♠️|',  '|      |', '|      |', '|      |', '|J♠️    |', ' ------ ')

    def test_format_3(self, seven_of_diamonds):
        assert seven_of_diamonds.format == (
            ' ------ ', '|    7♦️|',  '|      |', '|      |', '|      |', '|7♦️    |', ' ------ ')

    def test_format_4(self, ten_of_clubs):
        assert ten_of_clubs.format == (
            ' ------ ', '|   10♣️|',  '|      |', '|      |', '|      |', '|10♣️   |', ' ------ ')


class TestDeck:
    """Deck initiation tests"""

    def test_fresh_deck_order(self, new_deck, ace_of_hearts, jack_of_spades, seven_of_diamonds, ten_of_clubs):
        assert str(new_deck.cards[12]) == str(ace_of_hearts)
        assert str(new_deck.cards[18]) == str(seven_of_diamonds)
        assert str(new_deck.cards[35]) == str(jack_of_spades)
        assert str(new_deck.cards[-5]) == str(ten_of_clubs)
        assert len(new_deck.cards) == 52

    """Deck shuffle tests"""

    def test_shuffle_fresh_deck(self, new_deck, ace_of_hearts, jack_of_spades, seven_of_diamonds, ten_of_clubs):
        # arrange
        seed = 10

        # act
        new_deck.shuffle(seed)

        # assert
        assert str(new_deck.cards[26]) == str(ace_of_hearts)
        assert str(new_deck.cards[9]) == str(seven_of_diamonds)
        assert str(new_deck.cards[29]) == str(jack_of_spades)
        assert str(new_deck.cards[3]) == str(ten_of_clubs)
        assert len(new_deck.cards) == 52

    """burn method tests"""

    def test_burn_fresh_deck(self, new_deck, two_of_hearts, three_of_hearts):
        new_deck.burn()

        first_card_left = new_deck.cards[0]
        burn_list = new_deck.burnt_cards

        assert str(first_card_left) == str(three_of_hearts)
        assert str(burn_list[0]) == str(two_of_hearts)
        assert len(burn_list) == 1

    def test_burn_empty_deck(self, new_deck):
        new_deck.cards = []
        with pytest.raises(IndexError):
            new_deck.burn()

    def test_burn_partial_deck(self, new_deck, two_of_hearts, ace_of_hearts, two_of_diamonds):
        new_deck.burn()
        new_deck.cards = new_deck.cards[11:]

        new_deck.burn()

        first_card_left = new_deck.cards[0]
        burn_list = new_deck.burnt_cards

        assert str(first_card_left) == str(two_of_diamonds)
        assert str(burn_list[0]) == str(two_of_hearts)
        assert str(burn_list[1]) == str(ace_of_hearts)
        assert len(burn_list) == 2


class TestCardGroup:
    """CardGroup initialisation tests"""

    def test_non_list(self, seven_of_diamonds):
        with pytest.raises(TypeError):
            CardGroup(seven_of_diamonds)

    def test_non_cards(self):
        with pytest.raises(TypeError):
            CardGroup([("7", "D")])

    def test_duplicates(self, ace_of_hearts):
        with pytest.raises(ValueError):
            CardGroup([ace_of_hearts, ace_of_hearts])

    def test_suitable_list(self, ace_of_hearts, seven_of_diamonds, jack_of_spades):
        test_group = CardGroup(
            [ace_of_hearts, seven_of_diamonds, jack_of_spades])

        assert test_group.cards == [ace_of_hearts,
                                    seven_of_diamonds, jack_of_spades]

    """print method tests"""

    def test_print_one_card(self, capsys, seven_of_diamonds):
        test_group = CardGroup([seven_of_diamonds])

        test_group.print()

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert ' ------ ' in printed_lines
        assert printed_lines.count(' ------ ') == 2
        assert '|      |' in printed_lines
        assert printed_lines.count('|      |') == 3
        assert '|    7♦️|' in printed_lines
        assert '|7♦️    |' in printed_lines


class TestPocket:
    """Pocket initialisation tests"""

    def test_non_list_pocket(self, seven_of_diamonds):
        with pytest.raises(TypeError):
            Pocket(seven_of_diamonds)

    def test_non_cards_pocket(self):
        with pytest.raises(TypeError):
            Pocket([("7", "D")])

    def test_duplicates_pocket(self, ace_of_hearts):
        with pytest.raises(ValueError):
            Pocket([ace_of_hearts, ace_of_hearts])

    def test_short_list_pocket(self, ace_of_hearts):
        with pytest.raises(ValueError):
            Pocket([ace_of_hearts])

    def test_long_list_pocket(self, ace_of_hearts, seven_of_diamonds, jack_of_spades):
        with pytest.raises(ValueError):
            Pocket([ace_of_hearts, seven_of_diamonds, jack_of_spades])

    def test_suitable_list_pocket(self, ace_of_hearts, seven_of_diamonds):
        test_pocket = Pocket(
            [ace_of_hearts, seven_of_diamonds])

        assert test_pocket.cards == [ace_of_hearts,
                                     seven_of_diamonds]
        assert test_pocket.public is False

    """print method tests"""

    def test_print_pocket(self, capsys, seven_of_diamonds, jack_of_spades):
        test_group = Pocket([seven_of_diamonds, jack_of_spades])
        test_group.public = False

        test_group.print()

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert ' ------   ------ ' in printed_lines
        assert printed_lines.count(' ------   ------ ') == 2
        assert '|      | |      |' in printed_lines
        assert printed_lines.count('|      | |      |') == 3
        assert '|    7♦️| |    J♠️|' in printed_lines
        assert '|7♦️    | |J♠️    |' in printed_lines


class TestTable:
    """Table initialisation tests"""

    def test_non_list_table(self, seven_of_diamonds):
        with pytest.raises(TypeError):
            Table(seven_of_diamonds)

    def test_non_cards_table(self):
        with pytest.raises(TypeError):
            Table([("7", "D")])

    def test_duplicates_table(self, ace_of_hearts):
        with pytest.raises(ValueError):
            Table([ace_of_hearts, ace_of_hearts, ace_of_hearts])

    def test_short_list_table(self, ace_of_hearts):
        with pytest.raises(ValueError):
            Table([ace_of_hearts, ace_of_hearts])

    def test_long_list_table(self, ace_of_hearts, seven_of_diamonds, jack_of_spades, jack_of_diamonds, ten_of_clubs, ace_of_clubs):
        with pytest.raises(ValueError):
            Table([ace_of_hearts, seven_of_diamonds, jack_of_spades,
                  ten_of_clubs, jack_of_diamonds, ace_of_clubs])

    def test_flop_table(self, ace_of_hearts, seven_of_diamonds, jack_of_spades):
        test_table = Table(
            [ace_of_hearts, seven_of_diamonds, jack_of_spades])

        assert test_table.cards == [ace_of_hearts,
                                    seven_of_diamonds, jack_of_spades]
        assert test_table.public is True

    def test_turn_table(self, ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs):
        test_table = Table(
            [ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs])

        assert test_table.cards == [ace_of_hearts,
                                    seven_of_diamonds, jack_of_spades, ten_of_clubs]
        assert test_table.public is True

    def test_river_table(self, ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds):
        test_table = Table(
            [ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds])

        assert test_table.cards == [ace_of_hearts,
                                    seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds]
        assert test_table.public is True

    """print method tests"""

    def test_print_flop(self, capsys, jack_of_spades, seven_of_diamonds, jack_of_diamonds):
        test_group = Table(
            [seven_of_diamonds, jack_of_spades, jack_of_diamonds])

        test_group.print()

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert '      ------   ------   ------ ' in printed_lines
        assert printed_lines.count('      ------   ------   ------ ') == 2
        assert '     |      | |      | |      |' in printed_lines
        assert printed_lines.count('     |      | |      | |      |') == 3
        assert '     |    7♦️| |    J♠️| |    J♦️|' in printed_lines
        assert '     |7♦️    | |J♠️    | |J♦️    |' in printed_lines

    def test_print_turn(self, capsys, jack_of_spades, seven_of_diamonds, jack_of_diamonds, ace_of_hearts):
        test_group = Table(
            [seven_of_diamonds, jack_of_spades, jack_of_diamonds, ace_of_hearts])

        test_group.print()

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert '      ------   ------   ------   ------ ' in printed_lines
        assert printed_lines.count(
            '      ------   ------   ------   ------ ') == 2
        assert '     |      | |      | |      | |      |' in printed_lines
        assert printed_lines.count(
            '     |      | |      | |      | |      |') == 3
        assert '     |    7♦️| |    J♠️| |    J♦️| |    A❤️|' in printed_lines
        assert '     |7♦️    | |J♠️    | |J♦️    | |A❤️    |' in printed_lines

    def test_print_river(self, capsys, jack_of_spades, seven_of_diamonds, jack_of_diamonds, ace_of_hearts, ten_of_clubs):
        test_group = Table(
            [seven_of_diamonds, jack_of_spades, jack_of_diamonds, ace_of_hearts, ten_of_clubs])

        test_group.print()

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert '      ------   ------   ------   ------   ------ ' in printed_lines
        assert printed_lines.count(
            '      ------   ------   ------   ------   ------ ') == 2
        assert '     |      | |      | |      | |      | |      |' in printed_lines
        assert printed_lines.count(
            '     |      | |      | |      | |      | |      |') == 3
        assert '     |    7♦️| |    J♠️| |    J♦️| |    A❤️| |   10♣️|' in printed_lines
        assert '     |7♦️    | |J♠️    | |J♦️    | |A❤️    | |10♣️   |' in printed_lines


def test_already_unique_ints():
    test_list = [1, 2, 3]

    assert unique_list(test_list) == test_list


def test_not_unique_ints():
    test_list = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 777, 7, 5, 5]

    assert unique_list(test_list) == [1, 2, 3, 4, 777, 7, 5]


def test_unique_mixed_data():
    test_list = [1, "1", "a", "A", 1.0]

    assert unique_list(test_list) == test_list


def test_default_rows():
    assert default_rows() == (' ------ ', '|      |')


def test_burn_start_of_game():
    remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = []

    burn_card(remaining_deck, burnt_cards)

    assert remaining_deck == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️')]


def test_burn_mid_game():
    remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'),
                   ('10', '♣️'), ('5', '♣️'), ('5', '♦️')]

    burn_card(remaining_deck, burnt_cards)

    assert remaining_deck == [('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️'), ('K', '♠️'), ('3', '♣️'),
                           ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️')]


def test_burn_empty_deck():
    remaining_deck = []
    burnt_cards = [('3', '❤️')]

    with pytest.raises(IndexError):
        burn_card(remaining_deck, burnt_cards)


def test_deal_start_of_game():
    remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]

    card = deal_card(remaining_deck)

    assert remaining_deck == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert card == ('J', '♦️')


def test_deal_mid_game():
    remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]

    card = deal_card(remaining_deck)

    assert remaining_deck == [('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert card == ('3', '❤️')


def test_deal_empty_deck():
    remaining_deck = []

    with pytest.raises(IndexError):
        deal_card(remaining_deck)


def test_deal_pockets_all_players():
    remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = []
    still_in = [0, 1, 2, 3]

    pockets = deal_pockets(remaining_deck, burnt_cards, still_in)

    assert remaining_deck == [('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️')]
    assert pockets == {0: [('K', '♠️'), ('5', '♦️')],
                       1: [('3', '♣️'), ('3', '❤️')],
                       2: [('10', '♣️'), ('8', '♠️')],
                       3: [('5', '♣️'), ('5', '❤️')]}


def test_deal_pockets_nobody_still_in():
    remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = []
    still_in = []

    with pytest.raises(IndexError):
        deal_pockets(remaining_deck, burnt_cards, still_in)


def test_deal_flop():
    remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = []

    flop = deal_flop(remaining_deck, burnt_cards)

    assert remaining_deck == [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️')]
    assert flop == [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]


def test_deal_turn_normal():
    remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️')]
    flop = [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]

    turn = deal_turn(remaining_deck, burnt_cards, flop)

    assert remaining_deck == [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️'), ('5', '♣️')]
    assert turn == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]


def test_deal_turn_no_flop():
    remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️')]
    flop = []

    with pytest.raises(ValueError):
        deal_turn(remaining_deck, burnt_cards, flop)


def test_deal_river_normal():
    remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️'), ('5', '♣️')]
    turn = [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]

    river = deal_river(remaining_deck, burnt_cards, turn)

    assert remaining_deck == [('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️'), ('5', '♣️'), ('3', '❤️')]
    assert river == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'),
                     ('5', '♦️'), ('8', '♠️')]


def test_deal_river_to_flop():
    remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️')]
    flop = [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]

    with pytest.raises(ValueError):
        deal_river(remaining_deck, burnt_cards, flop)


def test_deal_to_empty():
    remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = []
    table = []

    table = deal_to_table(remaining_deck, burnt_cards, table)

    assert remaining_deck == [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️')]
    assert table == [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]


def test_deal_to_3():
    remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️')]
    table = [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]

    table = deal_to_table(remaining_deck, burnt_cards, table)

    assert remaining_deck == [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️'), ('5', '♣️')]
    assert table == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]


def test_deal_to_4():
    remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️'), ('5', '♣️')]
    table = [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]

    table = deal_to_table(remaining_deck, burnt_cards, table)

    assert remaining_deck == [('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    assert burnt_cards == [('J', '♦️'), ('5', '♣️'), ('3', '❤️')]
    assert table == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'),
                     ('5', '♦️'), ('8', '♠️')]


def test_deal_to_5():
    remaining_deck = [('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
    burnt_cards = [('J', '♦️'), ('5', '♣️'), ('3', '❤️')]
    table = [('K', '♠️'), ('3', '♣️'), ('10', '♣️'),
             ('5', '♦️'), ('8', '♠️')]

    with pytest.raises(ValueError):
        table = deal_to_table(remaining_deck, burnt_cards, table)
