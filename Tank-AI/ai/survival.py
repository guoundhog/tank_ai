from ai.base import AIController, Action
from ai.common import get_candidate


class SurvivalAI(AIController):
    """Mode 1: simple short-horizon dodge and avoidance rules."""
    def get_action(self, obs):
        dx, dy = get_candidate(obs, risky=False)
        return Action(move_x=dx, move_y=dy,
                      aim_x=obs.player_x, aim_y=obs.player_y)
