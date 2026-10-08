import pytest

from adaptive_engine.item_bank import Item
from adaptive_engine.simulate import simulate_session


@pytest.fixture
def large_item_bank():
    # Enough items, spanning a wide difficulty range, for a session to have
    # room to adapt and for the ability estimate to have a chance to converge.
    items = []
    b_values = [-3.0 + 0.3 * i for i in range(21)]  # -3.0 .. 3.0
    for i, b in enumerate(b_values):
        items.append(Item(item_id=f"item_{i}", domain="reasoning", a=1.3, b=round(b, 2)))
    return items


def test_simulate_session_returns_expected_history_length(large_item_bank):
    result = simulate_session(large_item_bank, true_theta=1.0, rounds=15, seed=42)
    assert len(result.theta_history) == 16  # initial + 15 rounds
    assert len(result.records) == 15


def test_simulate_session_is_deterministic_given_seed(large_item_bank):
    r1 = simulate_session(large_item_bank, true_theta=1.0, rounds=15, seed=42)
    r2 = simulate_session(large_item_bank, true_theta=1.0, rounds=15, seed=42)
    assert r1.theta_history == r2.theta_history
    assert r1.total_xp == r2.total_xp


def test_simulate_session_converges_toward_true_theta(large_item_bank):
    result = simulate_session(
        large_item_bank, true_theta=1.5, initial_theta=0.0, rounds=20, seed=123)
    # The estimate should end up meaningfully closer to the true ability
    # than the (deliberately mismatched) starting point.
    initial_error = abs(0.0 - 1.5)
    assert result.final_error < initial_error


def test_simulate_session_rejects_rounds_exceeding_bank_size(large_item_bank):
    with pytest.raises(ValueError):
        simulate_session(large_item_bank, true_theta=0.0, rounds=1000, seed=1)


def test_simulate_session_rejects_nonpositive_rounds(large_item_bank):
    with pytest.raises(ValueError):
        simulate_session(large_item_bank, true_theta=0.0, rounds=0, seed=1)
