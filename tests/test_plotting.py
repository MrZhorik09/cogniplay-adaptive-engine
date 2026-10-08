import pytest

from adaptive_engine.item_bank import Item, item_bank_to_dataframe
from adaptive_engine.plotting import plot_convergence, plot_item_bank
from adaptive_engine.simulate import simulate_session


@pytest.fixture
def small_item_bank():
    return [Item(item_id=f"item_{i}", domain=d, a=1.2, b=b)
            for i, (d, b) in enumerate([
                ("memory", -1.0), ("memory", 0.0), ("attention", 1.0),
                ("speed", -2.0), ("reasoning", 2.0),
            ])]


def test_plot_convergence_creates_file(tmp_path, small_item_bank):
    result = simulate_session(small_item_bank, true_theta=0.5, rounds=5, seed=1)
    out = tmp_path / "convergence.png"
    plot_convergence(result, str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_item_bank_creates_file(tmp_path, small_item_bank):
    df = item_bank_to_dataframe(small_item_bank)
    out = tmp_path / "item_bank.png"
    plot_item_bank(df, str(out))
    assert out.exists()
    assert out.stat().st_size > 0
