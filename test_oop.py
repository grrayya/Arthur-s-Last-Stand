import random
import pytest
from oop import Entity, Knight, Dragon


def test_entity_takes_damage_and_floors_at_zero():
    goblin = Entity("Goblin", health=30, min_dmg=1, max_dmg=1)
    goblin.take_damage(50)
    assert goblin.hp == 0
    assert not goblin.is_alive()

def test_entity_roll_attack_stays_in_range():
    goblin = Entity("Goblin", health=30, min_dmg=5, max_dmg=8)
    for _ in range(200):
        assert 5 <= goblin.roll_attack() <= 8


def test_knight_crit_multiplies_damage(monkeypatch):
    knight = Knight("Arthur", health=120, min_dmg=10, max_dmg=10, crit=1.0, flasks=2)
    monkeypatch.setattr(random, "randint", lambda a, b: 10)
    monkeypatch.setattr(random, "random", lambda: 0.0)  # forces the crit branch
    assert knight.roll_attack() == 15


def test_knight_no_crit_returns_base_hit(monkeypatch):
    knight = Knight("Arthur", health=120, min_dmg=10, max_dmg=10, crit=0.0, flasks=2)
    monkeypatch.setattr(random, "randint", lambda a, b: 10)
    assert knight.roll_attack() == 10

def test_flask_heals_but_clamps_at_max_hp():
    knight = Knight("Arthur", health=120, min_dmg=10, max_dmg=20, crit=0.25, flasks=1)
    knight.hp = 100
    knight.drink_flask()
    assert knight.hp == 120  # 100 + 50 would overshoot max_hp


def test_flask_decrements_and_runs_dry():
    knight = Knight("Arthur", health=120, min_dmg=10, max_dmg=20, crit=0.25, flasks=1)
    knight.hp = 50
    assert knight.drink_flask() is True
    assert knight.flasks == 0
    assert knight.drink_flask() is False


def test_dragon_scales_never_reduce_damage_below_one():
    smaug = Dragon("Smaug", health=350, min_dmg=15, max_dmg=25, scales=6)
    mitigated = smaug.take_damage(3) 
    assert mitigated == 1
    assert smaug.hp == 349

def test_dragon_take_damage_applies_scales_normally():
    smaug = Dragon("Smaug", health=350, min_dmg=15, max_dmg=25, scales=6)
    mitigated = smaug.take_damage(20)
    assert mitigated == 14
    assert smaug.hp == 336
