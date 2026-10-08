import pytest

from adaptive_engine.item_bank import Item
from adaptive_engine.selector import select_next_item


@pytest.fixture
def items():
    return [
        Item(item_id="easy", domain="memory", a=1.0, b=-2.0),
        Item(item_id="matched", domain="memory", a=1.0, b=0.0),
        Item(item_id="hard", domain="memory", a=1.0, b=2.0),
    ]


def test_select_next_item_picks_item_matching_current_theta(items):
    chosen = select_next_item(theta=0.0, items=items, administered_ids=set())
    assert chosen.item_id == "matched"


def test_select_next_item_excludes_administered(items):
    chosen = select_next_item(theta=0.0, items=items, administered_ids={"matched"})
    # With "matched" excluded, the next-best (closest difficulty) item should be picked.
    assert chosen.item_id in {"easy", "hard"}


def test_select_next_item_raises_when_bank_exhausted(items):
    all_ids = {item.item_id for item in items}
    with pytest.raises(ValueError):
        select_next_item(theta=0.0, items=items, administered_ids=all_ids)


def test_select_next_item_tracks_theta_shift(items):
    low_choice = select_next_item(theta=-2.0, items=items, administered_ids=set())
    high_choice = select_next_item(theta=2.0, items=items, administered_ids=set())
    assert low_choice.item_id == "easy"
    assert high_choice.item_id == "hard"
