from ai.base import AIController, Action
from ai.common import get_candidate


class RiskyDodgeAI(AIController):
    """Mode 2: rule-based near-miss preference. NOT a no-hit guarantee."""
    def get_action(self, obs):
        dx, dy = get_candidate(obs, risky=True)
        return Action(move_x=dx, move_y=dy,
                      aim_x=obs.player_x, aim_y=obs.player_y)
