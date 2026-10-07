import pandas as pd
import pytest

from sciviz.plotting import plot_histogram, plot_line_with_error, plot_scatter


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "time_s": [0, 1, 2, 3, 4],
        "measurement": [5.1, 7.2, 9.0, 10.8, 13.1],
        "measurement_err": [0.4, 0.5, 0.3, 0.6, 0.4],
    })


def test_plot_histogram_creates_file(tmp_path, sample_df):
    out = tmp_path / "hist.png"
    result_path = plot_histogram(sample_df, "measurement", str(out))
    assert result_path == str(out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_scatter_creates_file_with_trendline(tmp_path, sample_df):
    out = tmp_path / "scatter.png"
    plot_scatter(sample_df, "time_s", "measurement", str(out), with_trendline=True)
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_scatter_without_trendline(tmp_path, sample_df):
    out = tmp_path / "scatter_no_trend.png"
    plot_scatter(sample_df, "time_s", "measurement", str(out), with_trendline=False)
    assert out.exists()


def test_plot_line_with_error_creates_file(tmp_path, sample_df):
    out = tmp_path / "line.png"
    plot_line_with_error(sample_df, "time_s", "measurement", "measurement_err", str(out))
    assert out.exists()
    assert out.stat().st_size > 0
