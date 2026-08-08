
from texas_hold_em import unique_list, shuffle_deck, fresh_deck, produce_detail_rows, produce_default_rows, print_card_list
import pylint
import pytest


def test_already_unique_ints():
    test_list = [1, 2, 3]

    assert unique_list(test_list) == test_list


def test_not_unique_ints():
    test_list = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 777, 7, 5, 5]

    assert unique_list(test_list) == [1, 2, 3, 4, 777, 7, 5]


def test_unique_mixed_data():
    test_list = [1, "1", "a", "A", 1.0]

    assert unique_list(test_list) == test_list


def test_empty_shuffle():
    seed = 10
    deck = []

    assert shuffle_deck(deck, seed) == []


def test_fresh_deck_shuffle():
    seed = 10
    deck = [('2', '❤️'), ('3', '❤️'), ('4', '❤️'), ('5', '❤️'), ('6', '❤️'), ('7', '❤️'), ('8', '❤️'), ('9', '❤️'), ('10', '❤️'), ('J', '❤️'), ('Q', '❤️'), ('K', '❤️'), ('A', '❤️'), ('2', '♦️'), ('3', '♦️'), ('4', '♦️'), ('5', '♦️'), ('6', '♦️'), ('7', '♦️'), ('8', '♦️'), ('9', '♦️'), ('10', '♦️'), ('J', '♦️'), ('Q', '♦️'), ('K', '♦️'), ('A', '♦️'),
            ('2', '♠️'), ('3', '♠️'), ('4', '♠️'), ('5', '♠️'), ('6', '♠️'), ('7', '♠️'), ('8', '♠️'), ('9', '♠️'), ('10', '♠️'), ('J', '♠️'), ('Q', '♠️'), ('K', '♠️'), ('A', '♠️'), ('2', '♣️'), ('3', '♣️'), ('4', '♣️'), ('5', '♣️'), ('6', '♣️'), ('7', '♣️'), ('8', '♣️'), ('9', '♣️'), ('10', '♣️'), ('J', '♣️'), ('Q', '♣️'), ('K', '♣️'), ('A', '♣️')]

    assert shuffle_deck(deck, seed) == [('J', '♦️'), ('K', '♠️'), ('3', '♣️'), ('10', '♣️'), ('5', '♣️'), ('5', '♦️'), ('3', '❤️'), ('8', '♠️'), ('5', '❤️'), ('7', '♦️'), ('A', '♦️'), ('9', '♣️'), ('8', '❤️'), ('4', '♠️'), ('10', '♠️'), ('9', '❤️'), ('A', '♠️'), ('7', '♣️'), ('J', '♣️'), ('K', '♦️'), ('7', '❤️'), ('3', '♦️'), ('10', '❤️'), ('10', '♦️'), (
        'J', '❤️'), ('8', '♣️'), ('A', '❤️'), ('K', '❤️'), ('8', '♦️'), ('J', '♠️'), ('Q', '♣️'), ('2', '♠️'), ('2', '♣️'), ('Q', '♦️'), ('4', '♦️'), ('6', '❤️'), ('9', '♦️'), ('6', '♣️'), ('9', '♠️'), ('K', '♣️'), ('Q', '❤️'), ('4', '♣️'), ('6', '♦️'), ('7', '♠️'), ('5', '♠️'), ('2', '♦️'), ('2', '❤️'), ('A', '♣️'), ('6', '♠️'), ('3', '♠️'), ('4', '❤️'), ('Q', '♠️')]


def test_one_item_shuffle():
    seed = 10
    deck = [11]

    assert shuffle_deck(deck, seed) == [11]


def test_new_deck():
    assert fresh_deck() == [('2', '❤️'), ('3', '❤️'), ('4', '❤️'), ('5', '❤️'), ('6', '❤️'), ('7', '❤️'), ('8', '❤️'), ('9', '❤️'), ('10', '❤️'), ('J', '❤️'), ('Q', '❤️'), ('K', '❤️'), ('A', '❤️'), ('2', '♦️'), ('3', '♦️'), ('4', '♦️'), ('5', '♦️'), ('6', '♦️'), ('7', '♦️'), ('8', '♦️'), ('9', '♦️'), ('10', '♦️'), ('J', '♦️'), ('Q', '♦️'), ('K', '♦️'), ('A', '♦️'),
                            ('2', '♠️'), ('3', '♠️'), ('4', '♠️'), ('5', '♠️'), ('6', '♠️'), ('7', '♠️'), ('8', '♠️'), ('9', '♠️'), ('10', '♠️'), ('J', '♠️'), ('Q', '♠️'), ('K', '♠️'), ('A', '♠️'), ('2', '♣️'), ('3', '♣️'), ('4', '♣️'), ('5', '♣️'), ('6', '♣️'), ('7', '♣️'), ('8', '♣️'), ('9', '♣️'), ('10', '♣️'), ('J', '♣️'), ('Q', '♣️'), ('K', '♣️'), ('A', '♣️')]


def test_default_rows():
    assert produce_default_rows() == (' ------ ', '|      |')


def test_picture_rows():
    top, bot = produce_detail_rows(("K", "❤️"))

    assert top.count(" ") == 4 and bot.count(" ") == 4


def test_ten_rows():
    top, bot = produce_detail_rows(('10', '♣️'))

    assert top.count(" ") == 3 and bot.count(" ") == 3


def test_normal_rows():
    top, bot = produce_detail_rows(('5', '♦️'))

    assert top.count(" ") == 4 and bot.count(" ") == 4


def test_print_no_cards(capsys):
    card_list = []

    print_card_list(card_list, False)

    captured_output = capsys.readouterr().out
    printed_lines = captured_output.split("\n")

    assert "Error: No cards to print" in printed_lines


def test_print_one_card(capsys):
    card_list = [('5', '♦️')]

    print_card_list(card_list, False)

    captured_output = capsys.readouterr().out
    printed_lines = captured_output.split("\n")

    assert ' ------ ' in printed_lines
    assert printed_lines.count(' ------ ') == 2
    assert '|      |' in printed_lines
    assert printed_lines.count('|      |') == 3
    assert '|    5♦️|' in printed_lines
    assert '|5♦️    |' in printed_lines


def test_print_pocket(capsys):
    card_list = [('5', '♦️'), ('3', '♠️')]

    print_card_list(card_list, False)

    captured_output = capsys.readouterr().out
    printed_lines = captured_output.split("\n")

    assert ' ------   ------ ' in printed_lines
    assert printed_lines.count(' ------   ------ ') == 2
    assert '|      | |      |' in printed_lines
    assert printed_lines.count('|      | |      |') == 3
    assert '|    5♦️| |    3♠️|' in printed_lines
    assert '|5♦️    | |3♠️    |' in printed_lines


def test_print_flop(capsys):
    card_list = [('5', '♦️'), ('3', '♠️'), ('J', '♦️')]

    print_card_list(card_list, True)

    captured_output = capsys.readouterr().out
    printed_lines = captured_output.split("\n")

    assert '      ------   ------   ------ ' in printed_lines
    assert printed_lines.count('      ------   ------   ------ ') == 2
    assert '     |      | |      | |      |' in printed_lines
    assert printed_lines.count('     |      | |      | |      |') == 3
    assert '     |    5♦️| |    3♠️| |    J♦️|' in printed_lines
    assert '     |5♦️    | |3♠️    | |J♦️    |' in printed_lines


def test_print_turn(capsys):
    card_list = [('5', '♦️'), ('3', '♠️'), ('J', '♦️'), ('Q', '❤️')]

    print_card_list(card_list, True)

    captured_output = capsys.readouterr().out
    printed_lines = captured_output.split("\n")

    assert '      ------   ------   ------   ------ ' in printed_lines
    assert printed_lines.count('      ------   ------   ------   ------ ') == 2
    assert '     |      | |      | |      | |      |' in printed_lines
    assert printed_lines.count('     |      | |      | |      | |      |') == 3
    assert '     |    5♦️| |    3♠️| |    J♦️| |    Q❤️|' in printed_lines
    assert '     |5♦️    | |3♠️    | |J♦️    | |Q❤️    |' in printed_lines


def test_print_river(capsys):
    card_list = [('5', '♦️'), ('3', '♠️'), ('J', '♦️'),
                 ('Q', '❤️'), ('4', '❤️')]

    print_card_list(card_list, True)

    captured_output = capsys.readouterr().out
    printed_lines = captured_output.split("\n")

    assert '      ------   ------   ------   ------   ------ ' in printed_lines
    assert printed_lines.count(
        '      ------   ------   ------   ------   ------ ') == 2
    assert '     |      | |      | |      | |      | |      |' in printed_lines
    assert printed_lines.count(
        '     |      | |      | |      | |      | |      |') == 3
    assert '     |    5♦️| |    3♠️| |    J♦️| |    Q❤️| |    4❤️|' in printed_lines
    assert '     |5♦️    | |3♠️    | |J♦️    | |Q❤️    | |4❤️    |' in printed_lines
