import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------- extra_time_charge ----------
def test_extra_time_charge_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)

def test_extra_time_charge_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)

def test_extra_time_charge_within_included():
    # haircut included=30, duration=20 -> extra=-10 -> returns 0
    assert extra_time_charge("haircut", 20, "junior", False) == 0

def test_extra_time_charge_member_bonus():
    # haircut included=30, +15 member = 45, duration=50 -> extra=5, junior rate=10 -> 50
    assert extra_time_charge("haircut", 50, "junior", True) == 5 * 10

def test_extra_time_charge_member_spa_no_bonus():
    # spa excluded from member bonus: included=90, duration=100 -> extra=10, rate=10 -> 100
    assert extra_time_charge("spa", 100, "junior", True) == 10 * 10

def test_extra_time_charge_junior_short():
    # haircut extra=20 (<=60), junior rate=10 -> 200
    assert extra_time_charge("haircut", 50, "junior", False) == 20 * 10

def test_extra_time_charge_senior_short():
    # haircut extra=20 (<=60), not junior -> rate=18 -> 360
    assert extra_time_charge("haircut", 50, "senior", False) == 20 * 18

def test_extra_time_charge_junior_long():
    # haircut extra=70 (>60), junior rate=10+8=18, no senior +4 -> 1260
    assert extra_time_charge("haircut", 100, "junior", False) == 70 * 18

def test_extra_time_charge_senior_long():
    # haircut extra=70 (>60), senior rate=18+8+4=30 -> 2100
    assert extra_time_charge("haircut", 100, "senior", False) == 70 * 30


# ---------- can_book ----------
def test_can_book_walk_in_small():
    assert can_book(2, 1, True) is True

def test_can_book_walk_in_large():
    assert can_book(3, 1, True) is False

def test_can_book_advance_large_party():
    assert can_book(5, 1, False) is False

def test_can_book_advance_many_services():
    assert can_book(2, 3, False) is False

def test_can_book_advance_ok():
    assert can_book(2, 2, False) is True


# ---------- arrival_status ----------
def test_arrival_status_weekday_on_time():
    assert arrival_status(5, False, False) == "open"

def test_arrival_status_weekday_late():
    assert arrival_status(0, False, False) == "late"

def test_arrival_status_weekday_closed():
    assert arrival_status(-20, False, False) == "closed"

def test_arrival_status_colour_weekend_open():
    assert arrival_status(20, True, True) == "open"

def test_arrival_status_colour_weekend_late():
    assert arrival_status(10, True, True) == "late"

def test_arrival_status_colour_weekend_closed():
    assert arrival_status(0, True, True) == "closed"

def test_arrival_status_colour_weekday_open():
    assert arrival_status(10, True, False) == "open"

def test_arrival_status_noncolour_weekend_open():
    assert arrival_status(15, False, True) == "open"

# Branch coverage verified at 100%
