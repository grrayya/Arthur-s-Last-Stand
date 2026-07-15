import random
import procedural


def setup_function(_):

    procedural.arthur_hp = 120
    procedural.smaug_hp = 300

def test_roll_swing_stays_within_range_when_no_crit(monkeypatch):
    monkeypatch.setattr(random, "random", lambda: 1.0) 
    for _ in range(200):
        dmg, is_crit = procedural.roll_swing(12, 22)
        assert 12 <= dmg <= 22
        assert is_crit is False


def test_roll_swing_applies_crit_multiplier(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 20)
    monkeypatch.setattr(random, "random", lambda: 0.0)
    dmg, is_crit = procedural.roll_swing(15, 25, crit=0.25)
    assert dmg == 30
    assert is_crit is True

def test_start_brawl_ends_with_smaug_defeated(monkeypatch, capsys):
    procedural.smaug_hp = 10  # one hit finishes him off
    monkeypatch.setattr(random, "randint", lambda a, b: 15)
    monkeypatch.setattr(random, "random", lambda: 1.0)
    procedural.start_brawl()
    assert procedural.smaug_hp <= 0
    assert procedural.arthur_hp == 120  # boss turn is skipped once smaug falls
    assert "Smaug falls" in capsys.readouterr().out


def test_start_brawl_ends_with_arthur_defeated(monkeypatch, capsys):
    procedural.arthur_hp = 10
    monkeypatch.setattr(random, "randint", lambda a, b: 15)
    monkeypatch.setattr(random, "random", lambda: 1.0)
    procedural.start_brawl()
    assert procedural.arthur_hp <= 0
    assert "Arthur died" in capsys.readouterr().out
