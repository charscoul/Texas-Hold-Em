
from texas_hold_em import unique_list, default_rows, MIN_NAME_LENGTH, MAX_NAME_LENGTH, Card, Deck, CardGroup, Pocket, Table, Player, HumanPlayer, Dealer, deal_pockets, deal_flop, deal_turn, deal_river, deal_to_table

import pylint
import pytest

from support.testing_util import player_chooses


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


@pytest.fixture()
def new_deck() -> Deck:
    return Deck()


@pytest.fixture()
def test_names() -> list[str]:
    return ["Barry", "Andy", "Mikey", "Sally", "Scotty", "Mary", "Eddy", "Stevie", "Woody", "Julie", "Suzie", "Ruby", "Judy"]


@pytest.fixture()
def no_indexes() -> list:
    return []


@pytest.fixture()
def some_indexes() -> list[int]:
    return [0, 1, 2]


@pytest.fixture()
def julie(test_names, no_indexes) -> Player:
    seed = 10
    return Player(no_indexes, test_names, seed)


@pytest.fixture()
def suzie(test_names, no_indexes) -> Player:
    # Julie Suzie Judy Ruby
    seed = 10
    julie = Player(no_indexes, test_names, seed)
    return Player(no_indexes, test_names, seed)


@pytest.fixture()
def judy(test_names, no_indexes) -> Player:
    # Julie Suzie Judy Ruby
    seed = 10
    julie = Player(no_indexes, test_names, seed)
    suzie = Player(no_indexes, test_names, seed)
    return Player(no_indexes, test_names, seed)


@pytest.fixture()
def ruby(test_names, no_indexes) -> Player:
    # Julie Suzie Judy Ruby
    seed = 10
    julie = Player(no_indexes, test_names, seed)
    suzie = Player(no_indexes, test_names, seed)
    judy = Player(no_indexes, test_names, seed)
    return Player(no_indexes, test_names, seed)


@pytest.fixture()
def ladies(test_names, no_indexes) -> list[Player]:
    # Julie Suzie Judy Ruby
    seed = 10
    julie = Player(no_indexes, test_names, seed)
    suzie = Player(no_indexes, test_names, seed)
    judy = Player(no_indexes, test_names, seed)
    ruby = Player(no_indexes, test_names, seed)

    return [julie, suzie, judy, ruby]


@pytest.fixture()
def pocket_aces(ace_of_clubs, ace_of_hearts) -> Pocket:
    return Pocket([ace_of_hearts, ace_of_clubs])


@pytest.fixture()
def basic_flop(ace_of_hearts, seven_of_diamonds, jack_of_spades):
    return Table(
        [ace_of_hearts, seven_of_diamonds, jack_of_spades])


@pytest.fixture()
def basic_turn(ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs):
    return Table(
        [ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs])


def basic_river(ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds):
    return Table(
        [ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds])


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

    """Deal method tests"""

    def test_deal_fresh_deck(self, new_deck, two_of_hearts, three_of_hearts):
        test_card = new_deck.deal()

        first_card_left = new_deck.cards[0]

        assert str(first_card_left) == str(three_of_hearts)
        assert str(test_card) == str(two_of_hearts)
        assert len(new_deck.burnt_cards) == 0

    def test_burn_empty_deck(self, new_deck):
        new_deck.cards = []
        with pytest.raises(IndexError):
            new_deck.deal()

    def test_deal_partial_deck(self, new_deck, two_of_hearts, ace_of_hearts, two_of_diamonds):
        new_deck.burn()
        new_deck.cards = new_deck.cards[11:]

        test_card = new_deck.deal()

        first_card_left = new_deck.cards[0]
        burn_list = new_deck.burnt_cards

        assert str(first_card_left) == str(two_of_diamonds)
        assert str(burn_list[0]) == str(two_of_hearts)
        assert str(test_card) == str(ace_of_hearts)
        assert len(burn_list) == 1


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


class TestPlayer:
    """Player init tests"""

    def test_non_int_index(self, test_names):
        with pytest.raises(TypeError):
            Player(["0"], test_names)

    def test_non_str_name(self):
        with pytest.raises(TypeError):
            Player([0, 1, 2], [0, 1, 2])

    def test_non_list_indices(self, test_names):
        with pytest.raises(TypeError):
            Player(0, test_names)

    def test_non_list_names(self):
        with pytest.raises(TypeError):
            Player([0, 1], "Charlie")

    def test_no_names(self):
        with pytest.raises(ValueError):
            Player([0, 1], [])

    def test_short_name(self, test_names):
        test_names.append("DJ")
        with pytest.raises(ValueError):
            Player([0], test_names)

    def test_long_name(self, test_names):
        test_names.append("Bumbercatch")
        with pytest.raises(ValueError):
            Player([0], test_names)

    def test_neg_index(self, test_names):
        with pytest.raises(ValueError):
            Player([-1, 0], test_names)

    def test_first_player(self, no_indexes, test_names):
        seed = 10

        test_player = Player(no_indexes, test_names, seed)

        assert test_player.name == "Julie"
        assert test_player.index == 0
        assert no_indexes == [0]
        assert "Julie" not in test_names
        assert test_player.out is False

    def test_normal_player(self, some_indexes, test_names):
        seed = 10

        test_player = Player(some_indexes, test_names, seed)

        assert test_player.name == "Julie"
        assert test_player.index == 3
        assert some_indexes == [0, 1, 2, 3]
        assert "Julie" not in test_names
        assert test_player.out is False

    """add_pocket method tests"""

    def test_non_pocket(self, julie, ace_of_clubs, ace_of_hearts):
        with pytest.raises(TypeError):
            julie.add_pocket([ace_of_hearts, ace_of_clubs])

    def test_other_group(self, julie, basic_flop):
        with pytest.raises(TypeError):
            julie.add_pocket(basic_flop)

    def test_aces(self, julie, pocket_aces):
        julie.add_pocket(pocket_aces)
        assert julie.pocket == pocket_aces


class TestHumanPlayer:
    """Human Player init tests"""

    def test_short_input(self, monkeypatch, capsys, some_indexes, test_names):
        player_chooses(['Me', "Charlie"], monkeypatch)
        seed = 10

        human = HumanPlayer(some_indexes, test_names, seed)

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert f"Your must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters" in printed_lines

    def test_long_input(self, monkeypatch, capsys, some_indexes, test_names):
        player_chooses(['Humperdoo', "Charlie"], monkeypatch)
        seed = 10

        test_human = HumanPlayer(some_indexes, test_names, seed)

        captured_output = capsys.readouterr().out
        printed_lines = captured_output.split("\n")

        assert f"Your must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters" in printed_lines

    def test_unique_input(self, monkeypatch, some_indexes, test_names):
        player_chooses(["Charlie"], monkeypatch)
        seed = 10

        test_human = HumanPlayer(some_indexes, test_names, seed)

        assert test_human.name == 'Charlie'

    def test_bot_name(self, monkeypatch, some_indexes, test_names):
        player_chooses(["Andy"], monkeypatch)
        seed = 10

        test_human = HumanPlayer(some_indexes, test_names, seed)

        assert test_human.name == 'Andy'
        assert "Andy" not in test_names


class TestDealer:
    """Dealer init tests"""

    def test_success_ladies(self, ladies, ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs):
        seed = 10

        # act
        dealer_attempt = Dealer(ladies, seed)

        # assert
        assert str(dealer_attempt.deck.cards[26]) == str(ace_of_hearts)
        assert str(dealer_attempt.deck.cards[9]) == str(seven_of_diamonds)
        assert str(dealer_attempt.deck.cards[29]) == str(jack_of_spades)
        assert str(dealer_attempt.deck.cards[3]) == str(ten_of_clubs)
        assert len(dealer_attempt.deck.cards) == 52

        assert dealer_attempt.players == ladies

    def test_a(self):
        pass

    """still in tests"""

    def test_full_ladies(self, ladies):
        test_dealer = Dealer(ladies)

        assert test_dealer.still_in == [0, 1, 2, 3]

    def test_two_outs_ladies(self, ladies):
        test_dealer = Dealer(ladies)

        test_dealer.players[0].out = True
        test_dealer.players[2].out = True

        assert test_dealer.still_in == [1, 3]

    """make pockets tests"""

    def test_full_ladies_make_pockets(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        pockets_dict = test_dealer._make_pockets()

        assert str(pockets_dict[0]) == "King of Spades, Five of Diamonds"
        assert str(pockets_dict[1]) == "Three of Clubs, Three of Hearts"
        assert str(pockets_dict[2]) == "Ten of Clubs, Eight of Spades"
        assert str(pockets_dict[3]) == "Five of Clubs, Five of Hearts"

    def test_two_outs_ladies_make_pockets(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.players[0].out = True
        test_dealer.players[2].out = True

        pockets_dict = test_dealer._make_pockets()

        assert str(pockets_dict[1]) == "King of Spades, Ten of Clubs"
        assert str(pockets_dict[3]) == "Three of Clubs, Five of Clubs"
        assert 0 not in pockets_dict.keys()
        assert 2 not in pockets_dict.keys()

    """deal pockets method"""

    def test_full_ladies_deal_pockets(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.deal_pockets()

        assert str(
            test_dealer.players[0].pocket) == "King of Spades, Five of Diamonds"
        assert str(
            test_dealer.players[1].pocket) == "Three of Clubs, Three of Hearts"
        assert str(
            test_dealer.players[2].pocket) == "Ten of Clubs, Eight of Spades"
        assert str(
            test_dealer.players[3].pocket) == "Five of Clubs, Five of Hearts"

    def test_two_outs_ladies_deal_pockets(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.players[0].out = True
        test_dealer.players[2].out = True

        test_dealer.deal_pockets()

        assert test_dealer.players[0].pocket is None
        assert str(
            test_dealer.players[1].pocket) == "King of Spades, Ten of Clubs"
        assert test_dealer.players[2].pocket is None
        assert str(
            test_dealer.players[3].pocket) == "Three of Clubs, Five of Clubs"


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


# def test_deal_start_of_game():
#     remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]

#     card = deal_card(remaining_deck)

#     assert remaining_deck == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert card == ('J', '♦️')


# def test_deal_mid_game():
#     remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]

#     card = deal_card(remaining_deck)

#     assert remaining_deck == [('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert card == ('3', '❤️')


# def test_deal_empty_deck():
#     remaining_deck = []

#     with pytest.raises(IndexError):
#         deal_card(remaining_deck)


# def test_deal_pockets_all_players():
#     remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = []
#     still_in = [0, 1, 2, 3]

#     pockets = deal_pockets(remaining_deck, burnt_cards, still_in)

#     assert remaining_deck == [('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️')]
#     assert pockets == {0: [('K', '♠️'), ('5', '♦️')],
#                        1: [('3', '♣️'), ('3', '❤️')],
#                        2: [('10', '♣️'), ('8', '♠️')],
#                        3: [('5', '♣️'), ('5', '❤️')]}


# def test_deal_pockets_nobody_still_in():
#     remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = []
#     still_in = []

#     with pytest.raises(IndexError):
#         deal_pockets(remaining_deck, burnt_cards, still_in)


# def test_deal_flop():
#     remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = []

#     flop = deal_flop(remaining_deck, burnt_cards)

#     assert remaining_deck == [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️')]
#     assert flop == [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]


# def test_deal_turn_normal():
#     remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️')]
#     flop = [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]

#     turn = deal_turn(remaining_deck, burnt_cards, flop)

#     assert remaining_deck == [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️'), ('5', '♣️')]
#     assert turn == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]


# def test_deal_turn_no_flop():
#     remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️')]
#     flop = []

#     with pytest.raises(ValueError):
#         deal_turn(remaining_deck, burnt_cards, flop)


# def test_deal_river_normal():
#     remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️'), ('5', '♣️')]
#     turn = [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]

#     river = deal_river(remaining_deck, burnt_cards, turn)

#     assert remaining_deck == [('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️'), ('5', '♣️'), ('3', '❤️')]
#     assert river == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'),
#                      ('5', '♦️'), ('8', '♠️')]


# def test_deal_river_to_flop():
#     remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️')]
#     flop = [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]

#     with pytest.raises(ValueError):
#         deal_river(remaining_deck, burnt_cards, flop)


# def test_deal_to_empty():
#     remaining_deck = [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = []
#     table = []

#     table = deal_to_table(remaining_deck, burnt_cards, table)

#     assert remaining_deck == [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️')]
#     assert table == [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]


# def test_deal_to_3():
#     remaining_deck = [('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️')]
#     table = [('K', '♠️'), ('3', '♣️'), ('10', '♣️')]

#     table = deal_to_table(remaining_deck, burnt_cards, table)

#     assert remaining_deck == [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️'), ('5', '♣️')]
#     assert table == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]


# def test_deal_to_4():
#     remaining_deck = [('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️'), ('5', '♣️')]
#     table = [('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♦️')]

#     table = deal_to_table(remaining_deck, burnt_cards, table)

#     assert remaining_deck == [('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     assert burnt_cards == [('J', '♦️'), ('5', '♣️'), ('3', '❤️')]
#     assert table == [('K', '♠️'), ('3', '♣️'), ('10', '♣️'),
#                      ('5', '♦️'), ('8', '♠️')]


# def test_deal_to_5():
#     remaining_deck = [('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
#         'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]
#     burnt_cards = [('J', '♦️'), ('5', '♣️'), ('3', '❤️')]
#     table = [('K', '♠️'), ('3', '♣️'), ('10', '♣️'),
#              ('5', '♦️'), ('8', '♠️')]

#     with pytest.raises(ValueError):
#         table = deal_to_table(remaining_deck, burnt_cards, table)
