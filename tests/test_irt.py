import pytest

from adaptive_engine.irt import fisher_information, probability_correct, update_ability


def test_probability_at_theta_equals_b_is_one_half():
    assert probability_correct(theta=0.5, a=1.3, b=0.5) == pytest.approx(0.5)


def test_probability_increases_with_theta():
    low = probability_correct(theta=-2.0, a=1.0, b=0.0)
    high = probability_correct(theta=2.0, a=1.0, b=0.0)
    assert 0.0 < low < 0.5 < high < 1.0


def test_probability_is_numerically_stable_for_extreme_theta():
    # Should not raise OverflowError and should stay within [0, 1].
    assert 0.0 <= probability_correct(theta=1000, a=2.0, b=0.0) <= 1.0
    assert 0.0 <= probability_correct(theta=-1000, a=2.0, b=0.0) <= 1.0


def test_fisher_information_peaks_at_item_difficulty():
    a, b = 1.5, 0.0
    info_at_b = fisher_information(theta=b, a=a, b=b)
    info_away = fisher_information(theta=b + 2.0, a=a, b=b)
    assert info_at_b > info_away


def test_fisher_information_nonnegative():
    assert fisher_information(theta=3.0, a=1.2, b=-1.0) >= 0.0


def test_update_ability_moves_toward_correct_answer():
    theta = 0.0
    new_theta = update_ability(theta, a=1.0, b=0.0, correct=True, n_attempts=1)
    assert new_theta > theta


def test_update_ability_moves_away_for_incorrect_answer():
    theta = 0.0
    new_theta = update_ability(theta, a=1.0, b=0.0, correct=False, n_attempts=1)
    assert new_theta < theta


def test_update_ability_step_shrinks_with_more_attempts():
    step_early = update_ability(0.0, a=1.0, b=0.0, correct=True, n_attempts=1) - 0.0
    step_late = update_ability(0.0, a=1.0, b=0.0, correct=True, n_attempts=50) - 0.0
    assert step_late < step_early


def test_update_ability_rejects_invalid_attempt_count():
    with pytest.raises(ValueError):
        update_ability(0.0, a=1.0, b=0.0, correct=True, n_attempts=0)
