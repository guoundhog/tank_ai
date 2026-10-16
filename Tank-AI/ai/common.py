"""Small rule-based local-planning helpers; later AI work can replace these."""
from math import hypot, cos, sin, pi
from ai.base import Action

DIRECTIONS = [(0.0, 0.0)] + [(cos(i*pi/4), sin(i*pi/4)) for i in range(8)]


def wall_clearance(x, y, obs):
    left, top, right, bottom = obs.arena
    best = min(x-left, right-x, y-top, bottom-y)
    for wx, wy, ww, wh in obs.walls:
        near_x = max(wx, min(x, wx+ww))
        near_y = max(wy, min(y, wy+wh))
        best = min(best, hypot(x-near_x, y-near_y))
    return best


def bullet_distances(x, y, obs, time_ahead):
    for b in obs.bullets:
        if b.owner == 'player':
            # Straight-line local estimate: bounce prediction comes in a later version.
            yield hypot(x - (b.x + b.vx*time_ahead),
                        y - (b.y + b.vy*time_ahead))


def get_candidate(obs, *, risky=False, seek=False):
    """Evaluate simple future positions with a cheap heuristic (not RL)."""
    current = (obs.ai_x, obs.ai_y)
    target_t = 0.28
    speed = 180.0
    best_direction = (0, 0)
    best_score = -float('inf')
    incoming = any(b.owner == 'player' for b in obs.bullets)
    for dx, dy in DIRECTIONS:
        xx = current[0] + dx * speed * target_t
        yy = current[1] + dy * speed * target_t
        clearance = wall_clearance(xx, yy, obs)
        if clearance < 21.0:  # Avoid tank-sized intersections.
            continue
        player_distance = hypot(xx - obs.player_x, yy - obs.player_y)
        score = min(clearance, 75.0) * 0.16
        if risky and incoming:
            near = 1000.0
            for t in (0.0, 0.16, 0.32, 0.50):
                ds = list(bullet_distances(xx, yy, obs, t))
                if ds:
                    near = min(near, min(ds))
                    for d in ds:
                        if d < 38:
                            score -= (38-d)*5.8
            # Stay ~55-80 pixels from a projectile, without touching it.
            score -= abs(min(near, 550) - 66) * 0.09
            score += min(player_distance, 350) * 0.006
        else:
            score += (-player_distance * 0.075 if seek
                      else min(player_distance, 430) * 0.04)
            for t in (0.0, 0.15, 0.35, 0.60):
                for distance in bullet_distances(xx, yy, obs, t):
                    if distance < 115:
                        score -= (115-distance) * (1.3 if t < .4 else .6)
        # Moving opponents are more interesting than a frozen optimum.
        if dx == 0 and dy == 0:
            score -= 11.0
        if score > best_score:
            best_score = score
            best_direction = (dx, dy)
    return best_direction
