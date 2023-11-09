from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import (
    gen_cards,
    estimate_hole_card_win_rate,
)
import random

nb_simulation = 1000


class AdvancedPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        community_cards = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=nb_simulation,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_cards)
        )
        street = round_state['street']
        current_pot = round_state['pot']['main']['amount']
        to_call = valid_actions[1]['amount']

        # Calculate pot odds
        pot_odds = to_call / (current_pot + to_call)

        # Introduce randomness for "all in" at the very end
        if street == 'showdown' and random.random() < 0.09:
            action = valid_actions[2]  # All in
        else:
            # Advanced strategy for other streets
            if street == 'preflop':
                if win_rate >= 0.5:
                    action = valid_actions[2]  # Raise with very strong hand
                elif win_rate >= 0.4:
                    if pot_odds < 0.2:
                        # Raise with good hand and favorable pot odds
                        action = valid_actions[2]
                    else:
                        action = valid_actions[1]  # Call with good hand
                else:
                    action = valid_actions[1]  # Always Call weak hands
            else:
                aggressive_threshold = 0.6 if street == 'flop' else 0.5
                if win_rate >= aggressive_threshold:
                    action = valid_actions[2]  # Raise with strong hand
                elif win_rate >= 0.4 and pot_odds < 0.3:
                    # Raise with a semi-strong hand and favorable pot odds
                    action = valid_actions[2]
                else:
                    action = valid_actions[1]  # Call or check

        return action['action'], action['amount']

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return AdvancedPlayer()
