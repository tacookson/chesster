import pytest

from chesster import cli, config, fetch, render
from conftest import FakeEngine, game_dict

CONFIG = 'username = "Me4tbegZ0r"\n'


@pytest.fixture
def repo(tmp_path, monkeypatch):
    (tmp_path / "chesster.toml").write_text(CONFIG)
    games = [game_dict(), game_dict(url="https://www.chess.com/game/live/987654321")]
    monkeypatch.setattr(fetch, "games", lambda username, time_classes: iter(games))
    engines = []

    def open_engine(path):
        engines.append(FakeEngine())
        return engines[-1]
    monkeypatch.setattr(cli, "_open_engine", open_engine)
    return tmp_path, engines


def _run(tmp_path, *args):
    cli.main(["--config", str(tmp_path / "chesster.toml"), *args])


def _files(tmp_path):
    return sorted((tmp_path / "games").glob("*/*.md"))


def test_existing_ignores_files_that_arent_games(tmp_path):
    month = tmp_path / "2026-10"
    month.mkdir()
    (month / "notes.md").write_text("my notes")
    (month / "week-notes.md").write_text("more notes")
    (month / "2026-10-24-vs-opp-123.md").write_text("analysed")
    (month / "2026-10-25-vs-opp-456.md").write_text(render.NOT_ANALYSED)
    assert cli._existing(tmp_path) == {"123": True, "456": False}


def test_second_run_writes_nothing(repo, capsys):
    tmp_path, engines = repo
    _run(tmp_path)
    assert len(_files(tmp_path)) == 2 and len(engines) == 1
    _run(tmp_path)
    assert "No new games." in capsys.readouterr().out
    assert len(engines) == 1


def test_no_engine_games_are_analysed_by_a_later_run(repo, capsys):
    tmp_path, engines = repo
    _run(tmp_path, "--no-engine")
    assert all(render.NOT_ANALYSED in p.read_text() for p in _files(tmp_path))
    _run(tmp_path, "--no-engine")
    assert "No new games." in capsys.readouterr().out
    _run(tmp_path)
    assert len(engines) == 1
    assert len(_files(tmp_path)) == 2
    assert not any(render.NOT_ANALYSED in p.read_text() for p in _files(tmp_path))


def test_stray_file_in_games_does_not_crash(repo):
    tmp_path, _ = repo
    (tmp_path / "games" / "2026-10").mkdir(parents=True)
    (tmp_path / "games" / "2026-10" / "notes.md").write_text("mine")
    _run(tmp_path)
    assert (tmp_path / "games" / "2026-10" / "notes.md").read_text() == "mine"


def test_bad_config_exits_with_a_message(tmp_path):
    (tmp_path / "chesster.toml").write_text('username = "Me"\ntime_classes = "rapid"\n')
    with pytest.raises(SystemExit, match="Problem in .*time_classes must be a list"):
        _run(tmp_path)


def test_fetch_errors_exit_with_a_message(tmp_path, monkeypatch):
    (tmp_path / "chesster.toml").write_text(CONFIG)

    def fail(username, time_classes):
        raise fetch.FetchError("Couldn't reach Chess.com (offline). Check your connection.")
        yield
    monkeypatch.setattr(fetch, "games", fail)
    with pytest.raises(SystemExit, match="Couldn't reach Chess.com"):
        _run(tmp_path)


def test_missing_stockfish_exits_with_a_message(tmp_path):
    with pytest.raises(SystemExit, match="Stockfish not found"):
        cli._open_engine(str(tmp_path))  # a directory, not an engine
