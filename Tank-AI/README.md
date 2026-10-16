# Tank Dodge Lab (v0.1)

A small **top-down tank game** built with Python and **pygame-ce**. This is a playable first prototype with bouncing bullets and three **rule-based** AI opponents. The final goal is to compare classical prediction and reinforcement-learning controllers.

> The AI in this version uses simple heuristics. It is **not** deep reinforcement learning, and the near-miss AI does **not** guarantee zero hits.

## Quick start — Windows (Python required for development)

1. Install Python 3.11+ (preferably Python 3.12 or 3.13) with the Windows Python Launcher (`py`).
2. Unzip the project.
3. Double-click **`setup_windows.bat`** (creates `.venv` and installs `pygame-ce`).
4. Double-click **`play_windows.bat`**.

If you prefer VS Code / PowerShell, run in the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

### Controls

| Key | Effect |
| --- | --- |
| `1`, `2`, `3` (main menu) | Choose survival / near miss / duel |
| `W A S D` | Move player tank |
| Mouse | Aim turret |
| Hold left click or `Space` | Fire |
| `P` | Pause/unpause |
| `R` | Restart current mode |
| `Esc` | Main menu |
| `F3` | Toggle FPS and bullet count |

## Game modes (v0.1)

1. **SURVIVAL:** AI attempts to evade your projectiles and keep distance.
2. **NEAR MISS:** AI tries to stay close to bullets without touching them (approximate local straight-line prediction only).
3. **DUEL:** AI can fire at the player, maintain distance, and try to dodge.

In all modes, bullets bounce off field boundaries and solid walls, then expire after a short lifetime. A shot damages only the opposing team; player shots never harm the player after ricocheting. One hit ends the round.

## File layout

```text
Tank-AI/
├── main.py                   # Pygame window, input, fixed-step loop
├── game/
│   ├── config.py             # Resolution, balance constants
│   ├── world.py              # Map / obstacle geometry, collision checks
│   ├── tank.py               # Tank movement / aiming
│   ├── bullet.py             # Bullets / bounce / lifetime
│   ├── game.py               # Game state + AI integration (headless ready)
│   └── renderer.py           # Pygame drawing only
├── ai/
│   ├── base.py               # Observation -> Action interface
│   ├── common.py             # Tiny shared heuristic helpers
│   ├── survival.py           # Mode 1
│   ├── risky_dodge.py        # Mode 2
│   └── battle.py             # Mode 3
├── assets/                   # Space for future sprites and sound
├── tests/                    # Pure-Python physics and logic tests
├── setup_windows.bat         # Development dependency installer
├── play_windows.bat          # Start from a venv
├── build_windows.bat         # Create Windows distributable
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Build Windows EXE

**Run the build on Windows.** Double-click `build_windows.bat` after installing dependencies via `setup_windows.bat`.

It uses PyInstaller `--onedir --windowed` and creates:

```text
dist/
└── TankAI/
    ├── TankAI.exe
    └── _internal/   # Dependencies: DO NOT DELETE
```

Zip the **whole `dist/TankAI` directory** and attach the ZIP to a GitHub Release. The recipient does **not** need Python installed. A release EXE has not been built or tested in this source ZIP.

If you later add `assets/` files or ML model weights, remember to include them as data and resolve resource paths correctly in a bundled build.

## Tests / performance

Core mechanics have no pygame dependency; you can test or simulate them even without opening a window:

```powershell
py -m unittest discover -s tests -v
```

- Physics is updated at a **fixed 120 Hz**.
- Rendering is capped at **60 FPS**.
- AI decisions happen every **0.1 s**.
- Bullets are expired and capped, avoiding runaway collections.
- The camera is fixed and the only currently supported arena fits on screen.

## GitHub plan

1. Start in a private repository and commit `v0.1`.
2. Add richer ricochet trajectory prediction and tune the three modes.
3. Implement a separate headless training/evaluation workflow (e.g. Gymnasium + PyTorch).
4. Save trained models and run inference locally inside the game.
5. Make repository public and upload tested Windows artifacts in **Releases**.

## License

MIT. Replace the default copyright line with the correct legal name(s) before public release if appropriate.
