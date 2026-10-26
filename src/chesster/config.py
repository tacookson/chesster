import tomllib
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

TIME_CLASSES = {"bullet", "blitz", "rapid", "daily"}


class ConfigError(ValueError):
    """A setting in chesster.toml is missing or invalid."""


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
    decided: int


def _number(table: dict, key: str, default, kind: type, where: str):
    value = table.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ConfigError(f"{where}{key} must be a positive number, not {value!r}")
    if kind is int and not isinstance(value, int):
        raise ConfigError(f"{where}{key} must be a whole number, not {value!r}")
    return value


def load(path: Path) -> Config:
    try:
        data = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"not valid TOML: {e}") from e
    engine = data.get("engine", {})
    thresholds = data.get("thresholds", {})

    username = data.get("username")
    if not isinstance(username, str) or not username.strip():
        raise ConfigError("username is missing")

    timezone = data.get("timezone", "America/Toronto")
    try:
        ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as e:
        raise ConfigError(f"timezone {timezone!r} is not an IANA name like 'America/Toronto'") from e

    time_classes = data.get("time_classes", ["rapid"])
    if not isinstance(time_classes, list) or not all(isinstance(t, str) for t in time_classes):
        raise ConfigError(f"time_classes must be a list, e.g. [\"rapid\"], not {time_classes!r}")
    time_classes = [t.lower() for t in time_classes]
    if not time_classes or not set(time_classes) <= TIME_CLASSES:
        raise ConfigError(f"time_classes must be from {sorted(TIME_CLASSES)}, not {time_classes!r}")

    mistake = _number(thresholds, "mistake", 15, float, "[thresholds] ")
    blunder = _number(thresholds, "blunder", 30, float, "[thresholds] ")
    if blunder < mistake:
        raise ConfigError("[thresholds] blunder must be at least mistake")

    return Config(
        username=username,
        timezone=timezone,
        games_dir=path.parent / data.get("games_dir", "games"),
        time_classes=tuple(time_classes),
        engine_path=engine.get("path", "stockfish"),
        depth=_number(engine, "depth", 16, int, "[engine] "),
        safe_depth=_number(engine, "safe_depth", 12, int, "[engine] "),
        mistake=mistake,
        blunder=blunder,
        decided=_number(thresholds, "decided", 200, int, "[thresholds] "),
    )
