from chesster import cli


def test_rename_files_adds_match_prefix(tmp_path, capsys):
    month = tmp_path / "2026-10"
    month.mkdir()
    (month / "2026-10-23-vs-suresh_0705-9.md").write_text("x")
    (month / "2026-10-23-vs-opp-8.md").write_text("y")  # blitz: no match ID, left alone
    cli._rename_files(tmp_path, {"9": "261023-1"})
    assert sorted(p.name for p in month.iterdir()) == ["2026-10-23-vs-opp-8.md",
                                                       "261023-1_2026-10-23-vs-suresh_0705-9.md"]
    assert "Renamed" in capsys.readouterr().out
    assert cli._existing_ids(tmp_path) == {"8", "9"}
