import chess
import chess.engine
import pytest

PGN = """[Event "Live Chess"]
[Site "Chess.com"]
[White "Me4tbegZ0r"]
[Black "opp_1"]
[Result "0-1"]
[ECO "C50"]
[ECOUrl "https://www.chess.com/openings/Italian-Game-Two-Knights-Defense-4.d3"]

1. e4 {[%clk 0:15:05]} 1... e5 {[%clk 0:15:08]} 2. Nf3 {[%clk 0:14:50]} 2... Nc6 {[%clk 0:14:59]}
3. Bc4 {[%clk 0:14:30]} 3... Nf6 {[%clk 0:14:40]} 0-1
"""


def game_dict(**kw) -> dict:
    """A Chess.com archive entry, as the API returns it."""
    game = {
        "url": "https://www.chess.com/game/live/123456789",
        "pgn": PGN,
        "time_control": "900+10",
        "end_time": 1792857600,  # 2026-10-24 16:00 UTC
        "rated": True,
        "time_class": "rapid",
        "rules": "chess",
        "white": {"username": "Me4tbegZ0r", "rating": 797, "result": "resigned"},
        "black": {"username": "opp_1", "rating": 932, "result": "win"},
    }
    game.update(kw)
    return game


class FakeEngine:
    """Stands in for Stockfish: scores come from `score(board)`, in White's view."""

    def __init__(self, score=lambda board: 0, pv=lambda board: []):
        self.score, self.pv, self.calls = score, pv, []

    def analyse(self, board, limit, multipv=None, game=None):
        self.calls.append({"fen": board.fen(), "multipv": multipv, "game": game})
        if multipv is None:
            return self._info(board, self.score(board), self.pv(board))
        infos = []
        for move in board.legal_moves:
            board.push(move)
            infos.append(self._info(board, self.score(board), [move]))
            board.pop()
        return sorted(infos, key=lambda i: -i["score"].white().score(mate_score=100_000))

    @staticmethod
    def _info(board, white_cp, pv):
        # Real engines report from the side to move.
        return {"score": chess.engine.PovScore(chess.engine.Cp(white_cp), chess.WHITE)
                if board.turn == chess.WHITE else
                chess.engine.PovScore(chess.engine.Cp(-white_cp), chess.BLACK), "pv": pv}

    def quit(self):
        pass


@pytest.fixture
def fake_engine():
    return FakeEngine
