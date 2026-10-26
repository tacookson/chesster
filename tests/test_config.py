import pytest

from chesster import config


def _load(tmp_path, text):
    path = tmp_path / "chesster.toml"
    path.write_text(text)
    return config.load(path)


def test_defaults(tmp_path):
    cfg = _load(tmp_path, 'username = "Me"\n')
    assert cfg.time_classes == ("rapid",)
    assert (cfg.depth, cfg.safe_depth, cfg.mistake, cfg.blunder, cfg.decided) == (16, 12, 20, 30, 200)
    assert cfg.games_dir == tmp_path / "games"


def test_repo_config_loads():
    cfg = config.load(config.Path(__file__).parent.parent / "chesster.toml")
    assert cfg.username == "Me4tbegZ0r" and cfg.decided == 200


def test_time_classes_are_lowercased(tmp_path):
    assert _load(tmp_path, 'username = "Me"\ntime_classes = ["Rapid", "blitz"]\n').time_classes == ("rapid", "blitz")


@pytest.mark.parametrize("text, message", [
    ('timezone = "America/Toronto"\n', "username is missing"),
    ('username = "Me"\ntime_classes = "rapid"\n', "must be a list"),
    ('username = "Me"\ntime_classes = ["rapidd"]\n', "must be from"),
    ('username = "Me"\ntimezone = "Toronto"\n', "not an IANA name"),
    ('username = "Me"\n[engine]\ndepth = "16"\n', "[engine] depth must be a positive number"),
    ('username = "Me"\n[engine]\ndepth = 16.5\n', "[engine] depth must be a whole number"),
    ('username = "Me"\n[thresholds]\nmistake = 30\nblunder = 20\n', "blunder must be at least mistake"),
    ('username = "Me\n', "not valid TOML"),
])
def test_bad_settings_fail_with_a_message(tmp_path, text, message):
    with pytest.raises(config.ConfigError, match=message.replace("[", r"\[").replace("]", r"\]")):
        _load(tmp_path, text)
