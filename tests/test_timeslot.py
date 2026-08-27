from timeslot import TimeSlot
from datetime import datetime
import pytest



def test_create_valid_slot():
    slot = TimeSlot(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 11, 0))
    assert slot.start_time == datetime(2026, 1, 1, 10, 0)


def test_raises_when_end_before_start():
    with pytest.raises(ValueError):
        TimeSlot(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 9, 0))


def test_raises_when_invalid_type():
    with pytest.raises(TypeError):
        TimeSlot("2025, 01, 01", "2026, 01, 01")


def test_overlaps_return_true():
    slot1 = TimeSlot(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 11, 0))
    slot2 = TimeSlot(datetime(2026, 1, 1, 10,30, 0), datetime(2026, 1, 1, 12, 0))
    assert TimeSlot.overlaps_with(slot1, slot2) == True


def test_without_overlaps_return_false():
    slot1 = TimeSlot(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 11, 0))
    slot2 = TimeSlot(datetime(2026, 1, 1, 11,30, 0), datetime(2026, 1, 1, 12, 0))
    assert TimeSlot.overlaps_with(slot1, slot2) == False


def test_touching_slots_return_false():
    slot1 = TimeSlot(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 11, 0))
    slot2 = TimeSlot(datetime(2026, 1, 1, 11,0), datetime(2026, 1, 1, 12, 0))
    assert TimeSlot.overlaps_with(slot1, slot2) == False