import json

import pandas as pd
import pytest

from sciviz.cli import main


@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame({
        "time_s": [0, 1, 2, 3, 4],
        "measurement": [5.1, 7.2, 9.0, 10.8, 13.1],
        "measurement_err": [0.4, 0.5, 0.3, 0.6, 0.4],
    })
    path = tmp_path / "sample.csv"
    df.to_csv(path, index=False)
    return str(path)


def test_cli_stats_prints_json(sample_csv, capsys):
    exit_code = main(["stats", sample_csv, "--column", "measurement"])
    assert exit_code == 0
    output = json.loads(capsys.readouterr().out)
    assert output["n"] == 5
    assert output["mean"] == pytest.approx(9.04)


def test_cli_plot_histogram(sample_csv, tmp_path, capsys):
    out_path = tmp_path / "hist.png"
    exit_code = main([
        "plot", sample_csv, "--kind", "histogram",
        "--column", "measurement", "--output", str(out_path),
    ])
    assert exit_code == 0
    assert out_path.exists()
    assert "Saved plot to" in capsys.readouterr().out


def test_cli_plot_scatter(sample_csv, tmp_path):
    out_path = tmp_path / "scatter.png"
    exit_code = main([
        "plot", sample_csv, "--kind", "scatter",
        "--x", "time_s", "--y", "measurement", "--output", str(out_path),
    ])
    assert exit_code == 0
    assert out_path.exists()


def test_cli_plot_line_requires_yerr(sample_csv, tmp_path):
    out_path = tmp_path / "line.png"
    with pytest.raises(SystemExit):
        main(["plot", sample_csv, "--kind", "line",
              "--x", "time_s", "--y", "measurement", "--output", str(out_path)])


def test_cli_stats_unknown_column_raises(sample_csv):
    with pytest.raises(KeyError):
        main(["stats", sample_csv, "--column", "does_not_exist"])
