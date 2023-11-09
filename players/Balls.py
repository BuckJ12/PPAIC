# flake8: noqa
from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.card import Card


class Balls(BasePokerPlayer):
    def __init__(self):
        super().__init__()
        self.round_count = 0

    def declare_action(self, valid_actions, hole_card, round_state):
        # Always play
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]

        if round_state['round_count'] > self.round_count:
            self.round_count = round_state['round_count']
            raise_action_info = valid_actions[2]
            action, amount = raise_action_info["action"], raise_action_info["amount"]["min"]

        # Check if the hand is good (pair or higher)
        if self.is_good_hand(hole_card, round_state['community_card']):
            # Raise when the hand is good
            raise_action_info = valid_actions[2]
            action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]

        return action, amount

    def receive_game_start_message(self, game_info):
        print("Fuck")
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

    def is_good_hand(self, hole_card, community_card):
        # Combine hole cards and community cards to evaluate the hand
        all_cards = hole_card + community_card

        # Check if the hand is a pair or higher
        ranks = [Card.from_str(card).rank for card in all_cards]
        return len(set(ranks)) == 1


def setup_ai():
    return Balls()
