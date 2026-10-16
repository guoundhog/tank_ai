from math import hypot
from ai.base import AIController, Action
from ai.common import get_candidate


class BattleAI(AIController):
    """Mode 3: simple aim + shoot + evade. Neural-network training is future work."""
    def get_action(self, obs):
        distance = hypot(obs.player_x - obs.ai_x, obs.player_y - obs.ai_y)
        # Candidate search evaluates walls, unlike direct steering through walls.
        dx, dy = get_candidate(obs, seek=(distance > 290))
        return Action(move_x=dx, move_y=dy, shoot=True,
                      aim_x=obs.player_x, aim_y=obs.player_y)
