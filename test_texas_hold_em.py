import pylint
import pytest

from support.testing_util import player_chooses

from texas_hold_em import unique_list, default_rows, MIN_NAME_LENGTH, MAX_NAME_LENGTH, DRAW_PLACEHOLDER, Card, Deck, CardGroup, Pocket, Table, Player, HumanPlayer, Dealer, Hand, compare_hands


"""Standard function tests"""


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


"""instituting fixtures"""


@pytest.fixture()
def ace_of_hearts() -> Card:
    return Card("A", "H")


@pytest.fixture()
def king_of_hearts() -> Card:
    return Card("K", "H")


@pytest.fixture()
def queen_of_hearts() -> Card:
    return Card("Q", "H")


@pytest.fixture()
def jack_of_hearts() -> Card:
    return Card("J", "H")


@pytest.fixture()
def ten_of_hearts() -> Card:
    return Card("10", "H")


@pytest.fixture()
def nine_of_hearts() -> Card:
    return Card("9", "H")


@pytest.fixture()
def two_of_hearts() -> Card:
    return Card("2", "H")


@pytest.fixture()
def three_of_hearts() -> Card:
    return Card("3", "H")


@pytest.fixture()
def three_of_spades() -> Card:
    return Card("3", "S")


@pytest.fixture()
def three_of_diamonds() -> Card:
    return Card("3", "D")


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
def jack_of_clubs() -> Card:
    return Card("J", "C")


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


@pytest.fixture()
def basic_river(ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds):
    return Table(
        [ace_of_hearts, seven_of_diamonds, jack_of_spades, ten_of_clubs, jack_of_diamonds])


@pytest.fixture()
def ex_royal_flush(ten_of_hearts, jack_of_hearts, queen_of_hearts, king_of_hearts, ace_of_hearts):
    return Hand([ten_of_hearts, jack_of_hearts, queen_of_hearts, ace_of_hearts, king_of_hearts])


@pytest.fixture()
def ex_straight_flush(ten_of_hearts, jack_of_hearts, queen_of_hearts, king_of_hearts, nine_of_hearts):
    return Hand([ten_of_hearts, jack_of_hearts, queen_of_hearts, nine_of_hearts, king_of_hearts])


@pytest.fixture()
def ex_flush(ten_of_hearts, two_of_hearts, queen_of_hearts, king_of_hearts, nine_of_hearts):
    return Hand([ten_of_hearts, two_of_hearts, queen_of_hearts, nine_of_hearts, king_of_hearts])


@pytest.fixture()
def ex_straight(ten_of_hearts, jack_of_diamonds, queen_of_hearts, king_of_hearts, ace_of_clubs):
    return Hand([ten_of_hearts, jack_of_diamonds, queen_of_hearts, ace_of_clubs, king_of_hearts])


@pytest.fixture()
def ex_foak(jack_of_clubs, jack_of_diamonds, jack_of_hearts, jack_of_spades, three_of_hearts):
    return Hand([jack_of_clubs, jack_of_diamonds, jack_of_hearts, jack_of_spades, three_of_hearts])


@pytest.fixture()
def ex_full_house(jack_of_clubs, three_of_spades, jack_of_hearts, jack_of_spades, three_of_hearts):
    return Hand([jack_of_clubs, three_of_spades, jack_of_hearts, jack_of_spades, three_of_hearts])


@pytest.fixture()
def ex_toak(jack_of_clubs, seven_of_diamonds, jack_of_hearts, jack_of_spades, three_of_hearts):
    return Hand([jack_of_clubs, seven_of_diamonds, jack_of_hearts, jack_of_spades, three_of_hearts])


@pytest.fixture()
def ex_two_pair(jack_of_clubs, three_of_spades, seven_of_diamonds, jack_of_spades, three_of_hearts):
    return Hand([jack_of_clubs, three_of_spades, seven_of_diamonds, jack_of_spades, three_of_hearts])


@pytest.fixture()
def ex_pair(jack_of_clubs, three_of_spades, seven_of_diamonds, queen_of_hearts, three_of_hearts):
    return Hand([jack_of_clubs, three_of_spades, seven_of_diamonds, queen_of_hearts, three_of_hearts])


@pytest.fixture()
def ex_high_card(jack_of_clubs, three_of_spades, seven_of_diamonds, queen_of_hearts, ten_of_clubs):
    return Hand([jack_of_clubs, three_of_spades, seven_of_diamonds, queen_of_hearts, ten_of_clubs])


@pytest.fixture()
def ex_worse_full_house(jack_of_clubs, three_of_spades, jack_of_hearts, three_of_diamonds, three_of_hearts):
    return Hand([jack_of_clubs, three_of_spades, jack_of_hearts, three_of_diamonds, three_of_hearts])


@pytest.fixture()
def ex_better_flush(ten_of_hearts, three_of_hearts, queen_of_hearts, king_of_hearts, nine_of_hearts):
    return Hand([ten_of_hearts, three_of_hearts, queen_of_hearts, nine_of_hearts, king_of_hearts])


@pytest.fixture()
def ex_drawing_straight(ten_of_clubs, jack_of_diamonds, queen_of_hearts, king_of_hearts, ace_of_clubs):
    return Hand([ten_of_clubs, jack_of_diamonds, queen_of_hearts, ace_of_clubs, king_of_hearts])


"""Testing Classes"""


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

    def test_deal_empty_deck(self, new_deck):
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

    """deal pockets tests"""

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

    def test_deal_pockets_no_active_players(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.players[0].out = True
        test_dealer.players[1].out = True
        test_dealer.players[2].out = True
        test_dealer.players[3].out = True

        with pytest.raises(IndexError):
            test_dealer.deal_pockets()

    """deal flop tests"""

    def test_already_has_flop(self, ladies, basic_flop):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.table = basic_flop

        with pytest.raises(ValueError):
            test_dealer._deal_flop()

    def test_fresh_flop(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer._deal_flop()

        assert str(
            test_dealer.table) == "King of Spades, Three of Clubs, Ten of Clubs"
        assert isinstance(test_dealer.table, Table) is True

    """deal turn tests"""

    def test_no_flop(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        with pytest.raises(TypeError):
            test_dealer._deal_turn()

    def test_already_turn(self, ladies, basic_turn):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.table = basic_turn

        with pytest.raises(ValueError):
            test_dealer._deal_turn()

    def test_standard_turn(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer._deal_flop()
        test_dealer._deal_turn()

        assert str(
            test_dealer.table) == "King of Spades, Three of Clubs, Ten of Clubs, Five of Diamonds"
        assert isinstance(test_dealer.table, Table) is True

    """deal river tests"""

    def test_no_turn(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        with pytest.raises(TypeError):
            test_dealer._deal_river()

    def test_already_river(self, ladies, basic_river):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.table = basic_river

        with pytest.raises(ValueError):
            test_dealer._deal_river()

    def test_standard_river(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer._deal_flop()
        test_dealer._deal_turn()
        test_dealer._deal_river()

        assert str(
            test_dealer.table) == "King of Spades, Three of Clubs, Ten of Clubs, Five of Diamonds, Eight of Spades"
        assert isinstance(test_dealer.table, Table) is True

    """deal_to_table tests"""

    def test_deal_to_empty(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.deal_to_table()

        assert str(
            test_dealer.table) == "King of Spades, Three of Clubs, Ten of Clubs"
        assert isinstance(test_dealer.table, Table) is True

    def test_deal_to_flop(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.deal_to_table()
        test_dealer.deal_to_table()

        assert str(
            test_dealer.table) == "King of Spades, Three of Clubs, Ten of Clubs, Five of Diamonds"
        assert isinstance(test_dealer.table, Table) is True

    def test_deal_to_turn(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.deal_to_table()
        test_dealer.deal_to_table()
        test_dealer.deal_to_table()

        assert str(
            test_dealer.table) == "King of Spades, Three of Clubs, Ten of Clubs, Five of Diamonds, Eight of Spades"
        assert isinstance(test_dealer.table, Table) is True

    def test_deal_to_river(self, ladies):
        seed = 10
        test_dealer = Dealer(ladies, seed)

        test_dealer.deal_to_table()
        test_dealer.deal_to_table()
        test_dealer.deal_to_table()

        with pytest.raises(ValueError):
            test_dealer.deal_to_table()


class TestHand:
    """Testing flush"""

    def test_flush_attribute(self, ex_flush, ex_foak, ex_full_house, ex_high_card, ex_pair, ex_royal_flush, ex_straight, ex_straight_flush, ex_toak, ex_two_pair):
        assert ex_flush._flush is True
        assert ex_foak._flush is False
        assert ex_full_house._flush is False
        assert ex_high_card._flush is False
        assert ex_pair._flush is False
        assert ex_royal_flush._flush is True
        assert ex_straight._flush is False
        assert ex_straight_flush._flush is True
        assert ex_toak._flush is False
        assert ex_two_pair._flush is False

    """testing unique values"""

    def test_unique_values(self, ex_flush, ex_foak, ex_full_house, ex_high_card, ex_pair, ex_royal_flush, ex_straight, ex_straight_flush, ex_toak, ex_two_pair):
        assert ex_flush._unique_count == 5
        assert ex_foak._unique_count == 2
        assert ex_full_house._unique_count == 2
        assert ex_high_card._unique_count == 5
        assert ex_pair._unique_count == 4
        assert ex_royal_flush._unique_count == 5
        assert ex_straight._unique_count == 5
        assert ex_straight_flush._unique_count == 5
        assert ex_toak._unique_count == 3
        assert ex_two_pair._unique_count == 3

    """testing straight status"""

    def test_straight_attribute(self, ex_flush, ex_foak, ex_full_house, ex_high_card, ex_pair, ex_royal_flush, ex_straight, ex_straight_flush, ex_toak, ex_two_pair):
        assert ex_flush._straight is False
        assert ex_foak._straight is False
        assert ex_full_house._straight is False
        assert ex_high_card._straight is False
        assert ex_pair._straight is False
        assert ex_royal_flush._straight is True
        assert ex_straight._straight is True
        assert ex_straight_flush._straight is True
        assert ex_toak._straight is False
        assert ex_two_pair._straight is False

    """testing hand type and kickers"""

    def test_type_and_kickers(self, ex_flush, ex_foak, ex_full_house, ex_high_card, ex_pair, ex_royal_flush, ex_straight, ex_straight_flush, ex_toak, ex_two_pair):
        assert ex_flush.hand_type == "Flush"
        assert ex_flush.kickers == (2, 3, 5, 6, 13)

        assert ex_foak.hand_type == "Four of a Kind"
        assert ex_foak.kickers == (4, 12)

        assert ex_full_house.hand_type == "Full House"
        assert ex_full_house.kickers == (4, 12)

        assert ex_high_card.hand_type == "High Card"
        assert ex_high_card.kickers == (3, 4, 5, 8, 12)

        assert ex_pair.hand_type == "Pair"
        assert ex_pair.kickers == (12, 3, 4, 8)

        assert ex_royal_flush.hand_type == "Royal Flush"
        assert ex_royal_flush.kickers == None

        assert ex_straight.hand_type == "Straight"
        assert ex_straight.kickers == 1

        assert ex_straight_flush.hand_type == "Straight Flush"
        assert ex_straight_flush.kickers == 2

        assert ex_toak.hand_type == "Three of a Kind"
        assert ex_toak.kickers == (4, 8, 12)

        assert ex_two_pair.hand_type == "Two Pair"
        assert ex_two_pair.kickers == (4, 12, 8)


"""Testing compare_hands()"""


def test_compare_not_hands(ten_of_hearts, jack_of_diamonds, queen_of_hearts, king_of_hearts, ace_of_clubs, ex_straight):
    with pytest.raises(TypeError):
        compare_hands((ten_of_hearts, jack_of_diamonds, queen_of_hearts,
                      king_of_hearts, ace_of_clubs), ex_straight)


def test_compare_adjacent_hands(ex_straight, ex_flush):
    assert compare_hands(ex_straight, ex_flush) == 1


def test_compare_gap_hands(ex_foak, ex_two_pair):
    assert compare_hands(ex_foak, ex_two_pair) == 0


def test_compare_first_kicker(ex_full_house, ex_worse_full_house):
    assert compare_hands(ex_worse_full_house, ex_full_house) == 1


def test_compare_last_kicker(ex_better_flush, ex_flush):
    assert compare_hands(ex_better_flush, ex_flush) == 0


def test_compare_drawing_hands(ex_straight, ex_drawing_straight):
    assert compare_hands(ex_drawing_straight, ex_straight) == DRAW_PLACEHOLDER


def test_compare_identical_hands(ex_straight):
    assert compare_hands(ex_straight, ex_straight) == DRAW_PLACEHOLDER
