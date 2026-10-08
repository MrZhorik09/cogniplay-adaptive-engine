import json

import pytest

from adaptive_engine.cli import main


@pytest.fixture
def item_bank_csv(tmp_path):
    rows = ["item_id,domain,a,b"]
    b_values = [-3.0 + 0.3 * i for i in range(21)]
    for i, b in enumerate(b_values):
        rows.append(f"item_{i},reasoning,1.3,{round(b, 2)}")
    path = tmp_path / "bank.csv"
    path.write_text("\n".join(rows))
    return str(path)


def test_cli_simulate_prints_valid_json(item_bank_csv, capsys):
    exit_code = main([
        "simulate", "--items", item_bank_csv, "--true-theta", "1.0",
        "--rounds", "10", "--seed", "42",
    ])
    assert exit_code == 0
    captured = capsys.readouterr().out
    summary = json.loads(captured)
    assert summary["rounds"] == 10
    assert summary["true_theta"] == 1.0
    assert "final_theta_estimate" in summary
    assert "total_xp" in summary


def test_cli_simulate_with_plot(item_bank_csv, tmp_path):
    out_path = tmp_path / "convergence.png"
    exit_code = main([
        "simulate", "--items", item_bank_csv, "--true-theta", "0.5",
        "--rounds", "8", "--seed", "1", "--plot", str(out_path),
    ])
    assert exit_code == 0
    assert out_path.exists()


def test_cli_item_bank_plot(item_bank_csv, tmp_path):
    out_path = tmp_path / "bank.png"
    exit_code = main(["item-bank-plot", "--items", item_bank_csv, "--output", str(out_path)])
    assert exit_code == 0
    assert out_path.exists()


def test_cli_simulate_rejects_too_many_rounds(item_bank_csv):
    with pytest.raises(ValueError):
        main(["simulate", "--items", item_bank_csv, "--true-theta", "0.0", "--rounds", "9999"])
