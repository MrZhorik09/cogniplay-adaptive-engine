import math

import pandas as pd
import pytest

from sciviz.stats import confidence_interval_95, descriptive_stats, load_dataset


def test_load_dataset(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("a,b\n1,2\n3,4\n")
    df = load_dataset(str(csv_path))
    assert list(df.columns) == ["a", "b"]
    assert len(df) == 2


def test_descriptive_stats_basic_values():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5]})
    result = descriptive_stats(df, "x")
    assert result.n == 5
    assert result.mean == pytest.approx(3.0)
    assert result.minimum == 1.0
    assert result.maximum == 5.0
    assert result.median == 3.0
    assert result.std == pytest.approx(1.5811, rel=1e-3)


def test_descriptive_stats_ignores_nan_and_non_numeric():
    df = pd.DataFrame({"x": [1, 2, "not_a_number", None, 5]})
    result = descriptive_stats(df, "x")
    assert result.n == 3
    assert result.mean == pytest.approx((1 + 2 + 5) / 3)


def test_descriptive_stats_missing_column_raises_keyerror():
    df = pd.DataFrame({"x": [1, 2, 3]})
    with pytest.raises(KeyError):
        descriptive_stats(df, "does_not_exist")


def test_descriptive_stats_all_nan_raises_valueerror():
    df = pd.DataFrame({"x": ["a", "b", "c"]})
    with pytest.raises(ValueError):
        descriptive_stats(df, "x")


def test_confidence_interval_single_sample_returns_point():
    low, high = confidence_interval_95(mean=10.0, std=2.0, n=1)
    assert low == high == 10.0


def test_confidence_interval_symmetric_around_mean():
    low, high = confidence_interval_95(mean=10.0, std=2.0, n=100)
    assert low < 10.0 < high
    assert math.isclose((low + high) / 2, 10.0, rel_tol=1e-9)
