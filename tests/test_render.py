from chesster import analyse, render
from chesster.analyse import Flag


def test_eval_words_are_from_my_side():
    assert render.eval_words(30) == "about equal"
    assert render.eval_words(-120) == "slightly worse"
    assert render.eval_words(300) == "clearly better"
    assert render.eval_words(-460) == "losing"
    assert render.eval_words(100_000) == "forced mate for you"


def test_material_words():
    assert render.material_words(3) == "a piece"
    assert render.material_words(7) == "7 points of material"


def _flag(**kw):
    base = dict(ply=28, move_label="15. Bd3", severity="blunder", kind=analyse.LOST_MATERIAL, drop=38,
                before="+0.3", after="−4.6", best="Bxc6", punished_by="15... Nxe5", best_uci="b5c6",
                punished_uci="c6e5", before_cp=25, after_cp=-460,
                best_line="15. Bxc6 Qxc6 16. Qxc6 bxc6", punish_line="15... Nxe5 16. Qxd7 Nxd7",
                material=3, best_takes="knight", punish_takes="bishop", safe=(1, 37))
    base.update(kw)
    return Flag(**base)


def test_moment_reads_as_sentences():
    text = render._moment(_flag(first_material_loss=True), "White")
    assert "### Move 15 as White: you played Bd3" in text
    assert "**Blunder: you lost a piece.** This was the first material you lost in the game." in text
    assert "- **Better:** 15. Bxc6, taking the knight." in text
    assert "- **What your move allowed:** 15... Nxe5, taking your bishop." in text
    assert "about equal (+0.3) → losing (−4.6), from your side." in text
    assert "Only 1 of your 37 legal moves kept your position. This was a hard spot." in text


def test_merged_moment_lists_every_move():
    flag = _flag(move_label="15... Rab8", merged=["16... a5", "17... Rb5"], kind=analyse.DEEPER,
                 material=0, safe=None)
    text = render._moment(flag, "Black")
    assert "### Moves 15–17 as Black: you played Rab8, a5, Rb5" in text
    assert "The same idea was missed on 3 moves in a row." in text


def test_missed_chance_headline():
    text = render._moment(_flag(kind=analyse.MISSED_CHANCE, material=0, safe=None, severity="mistake"),
                          "White")
    assert "**Mistake: your opponent's last move gave you a big chance and you didn't take it.**" in text
