from adaptive_engine.gamification import SessionScorer, compute_xp
from adaptive_engine.item_bank import Item


def test_compute_xp_incorrect_answer_gives_consolation_xp():
    item = Item(item_id="i1", domain="memory", a=1.0, b=1.0)
    assert compute_xp(item, correct=False, streak_after=0) == 2


def test_compute_xp_harder_item_worth_more():
    easy = Item(item_id="e", domain="memory", a=1.0, b=0.0)
    hard = Item(item_id="h", domain="memory", a=1.0, b=2.0)
    xp_easy = compute_xp(easy, correct=True, streak_after=1)
    xp_hard = compute_xp(hard, correct=True, streak_after=1)
    assert xp_hard > xp_easy


def test_compute_xp_streak_bonus_applies_after_threshold():
    item = Item(item_id="i1", domain="memory", a=1.0, b=0.0)
    xp_no_streak = compute_xp(item, correct=True, streak_after=1)
    xp_with_streak = compute_xp(item, correct=True, streak_after=5)
    assert xp_with_streak > xp_no_streak


def test_session_scorer_tracks_streak_and_resets_on_miss():
    item = Item(item_id="i1", domain="memory", a=1.0, b=0.0)
    scorer = SessionScorer()

    scorer.record(item, True)
    scorer.record(item, True)
    assert scorer.streak == 2

    scorer.record(item, False)
    assert scorer.streak == 0
    assert scorer.best_streak == 2


def test_session_scorer_accumulates_total_xp():
    item = Item(item_id="i1", domain="memory", a=1.0, b=0.0)
    scorer = SessionScorer()
    xp1 = scorer.record(item, True)
    xp2 = scorer.record(item, False)
    assert scorer.total_xp == xp1 + xp2
    assert len(scorer.history) == 2
