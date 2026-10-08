import pytest

from adaptive_engine.item_bank import Item, item_bank_to_dataframe, load_item_bank


def test_item_rejects_unknown_domain():
    with pytest.raises(ValueError):
        Item(item_id="x1", domain="trivia", a=1.0, b=0.0)


def test_item_rejects_nonpositive_discrimination():
    with pytest.raises(ValueError):
        Item(item_id="x1", domain="memory", a=0.0, b=0.0)


def test_load_item_bank_from_csv(tmp_path):
    csv_path = tmp_path / "bank.csv"
    csv_path.write_text("item_id,domain,a,b\ni1,memory,1.2,0.5\ni2,attention,0.8,-1.0\n")
    items = load_item_bank(str(csv_path))
    assert len(items) == 2
    assert items[0].item_id == "i1"
    assert items[0].domain == "memory"
    assert items[1].b == -1.0


def test_load_item_bank_missing_column_raises(tmp_path):
    csv_path = tmp_path / "bank.csv"
    csv_path.write_text("item_id,domain,a\ni1,memory,1.2\n")
    with pytest.raises(KeyError):
        load_item_bank(str(csv_path))


def test_item_bank_to_dataframe_round_trip():
    items = [Item(item_id="i1", domain="memory", a=1.2, b=0.5)]
    df = item_bank_to_dataframe(items)
    assert list(df.columns) == ["item_id", "domain", "a", "b"]
    assert df.iloc[0]["item_id"] == "i1"
