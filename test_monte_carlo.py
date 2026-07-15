import pytest
from monte_carlo import simulate_battles


def test_simulate_battles_returns_percentage_in_valid_range():
    rate = simulate_battles(trials=200)
    assert 0 <= rate <= 100

def test_zero_trials_raises_zero_division():
    with pytest.raises(ZeroDivisionError):
        simulate_battles(trials=0)


def test_win_rate_is_roughly_stable_across_runs():
    rate_a = simulate_battles(trials=3000)
    rate_b = simulate_battles(trials=3000)
    assert abs(rate_a - rate_b) < 15
