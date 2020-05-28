#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
from functools import reduce
from itertools import combinations, chain

def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = list(map(rank_of_card, hand))
    ranks.sort(reverse=True)
    return ranks


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    suits = {card[-1] for card in hand}
    if len(suits) == 1:
        return True
    return False


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют 
    последовательность 5ти, где у 5ти карт ранги идут по порядку (стрит)"""
    div_ranks = {x - y for x, y in zip(ranks[0::], ranks[1::])}
    if div_ranks == {1}:
        return True
    return False


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank
    return None


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    first_rank = kind(2, ranks)
    if first_rank:
        pairs = []
        pairs.append(first_rank)
        ranks = [x for x in ranks if x != first_rank]
        second_rank = kind(2, ranks)
        if second_rank:
            pairs.append(second_rank)
            return pairs
    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    all_hands = combinations(hand, 5)
    max_hand = next(all_hands)
    max_hand_value = hand_rank(max_hand)
    for five_hand in all_hands:
        if hand_rank(five_hand) > max_hand_value:
            max_hand_value = hand_rank(five_hand)
            max_hand = five_hand

    return list(max_hand)


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    if '?B' in hand and '?R' in hand:
        hand.remove('?B')
        hand.remove('?R')
        current_hand = hand.copy()
        wild_hand_B = gen_variants('C', hand) + gen_variants('S', hand)
        wild_hand_R = gen_variants('H', hand) + gen_variants('D', hand)
        current_hand += [wild_hand_B[0], wild_hand_R[0]]
        max_hand = best_hand(current_hand)
        max_hand_value = hand_rank(max_hand)
        for add_card_B in wild_hand_B[1::]:
            for add_card_R in wild_hand_R[1::]:
                current_hand = hand.copy()
                current_hand += [add_card_B, add_card_R]
                local_best_hand = best_hand(current_hand)
                if hand_rank(local_best_hand) > max_hand_value:
                    max_hand_value = hand_rank(local_best_hand)
                    max_hand = local_best_hand
    elif '?B' in hand:
        hand.remove('?B')
        current_hand = hand.copy()
        wild_hand_B = gen_variants('C', hand) + gen_variants('S', hand)
        current_hand.append(wild_hand_B[0])
        max_hand = best_hand(current_hand)
        max_hand_value = hand_rank(max_hand)
        for add_card_B in wild_hand_B[1::]:
            current_hand = hand.copy()
            current_hand.append(add_card_B)
            local_best_hand = best_hand(current_hand)
            if hand_rank(local_best_hand) > max_hand_value:
                max_hand_value = hand_rank(local_best_hand)
                max_hand = local_best_hand
    elif '?R' in hand:
        hand.remove('?R')
        current_hand = hand.copy()
        wild_hand_R = gen_variants('H', hand) + gen_variants('D', hand)
        current_hand.append(wild_hand_R[0])
        max_hand = best_hand(current_hand)
        max_hand_value = hand_rank(max_hand)
        for add_card_R in wild_hand_R[1::]:
            current_hand = hand.copy()
            current_hand.append(add_card_R)
            local_best_hand = best_hand(current_hand)
            if hand_rank(local_best_hand) > max_hand_value:
                max_hand_value = hand_rank(local_best_hand)
                max_hand = local_best_hand
    else:
        max_hand = best_hand(hand)

    return max_hand


def rank_of_card(card):
    rank = card[0]
    if rank.isdigit():
        return int(rank)
    word_ranks = ['T', 'J', 'Q', 'K', 'A']
    rank_dict = {word: word_ranks.index(word) + 10 for word in ['T', 'J', 'Q', 'K', 'A']}
    return rank_dict[rank]


def gen_variants(suit, hand):
    ranks = [str(i) for i in range(2,10)] + ['T', 'J', 'Q', 'K', 'A']
    return [rank + suit for rank in ranks if rank + suit not in hand]


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split())) == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split())) == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split())) == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
