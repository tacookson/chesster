import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    username: str
    timezone: str
    games_dir: Path
    time_classes: tuple[str, ...]
    engine_path: str
    depth: int
    safe_depth: int
    mistake: float
    blunder: float
    gave_back: float


def load(path: Path) -> Config:
    data = tomllib.loads(path.read_text())
    engine = data.get("engine", {})
    thresholds = data.get("thresholds", {})
    return Config(
        username=data["username"],
        timezone=data.get("timezone", "America/Toronto"),
        games_dir=path.parent / data.get("games_dir", "games"),
        time_classes=tuple(data.get("time_classes", ["rapid"])),
        engine_path=engine.get("path", "stockfish"),
        depth=engine.get("depth", 16),
        safe_depth=engine.get("safe_depth", 12),
        mistake=thresholds.get("mistake", 15),
        blunder=thresholds.get("blunder", 30),
        gave_back=thresholds.get("gave_back", 0.5),
    )
