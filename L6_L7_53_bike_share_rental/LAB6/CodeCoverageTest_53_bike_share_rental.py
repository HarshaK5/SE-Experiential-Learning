import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


def test_ride_cost_examples_and_surcharges():
    assert ride_cost("standard", 45, False, False) == 40
    assert ride_cost("electric", 30, True, False) == 0
    assert ride_cost("cargo", 31, True, True) == 50
    assert ride_cost("standard", 181, False, True) == 255


def test_dock_status_examples():
    assert dock_status(0, 10) == "empty"
    assert dock_status(10, 10) == "full"
    assert dock_status(2, 10) == "few bikes"
    assert dock_status(8, 10) == "few slots"
    assert dock_status(5, 10) == "available"


def test_unlock_decisions():
    assert can_unlock(500, False, 18) is True
    assert can_unlock(100, False, 16) is True
    assert can_unlock(99, False, 16) is False
    assert can_unlock(500, False, 15) is False
    assert can_unlock(500, True, 18) is False


@pytest.mark.parametrize(
    "call",
    [
        lambda: ride_cost("unknown", 30, False, False),
        lambda: ride_cost("standard", 0, False, False),
        lambda: dock_status(0, 0),
        lambda: dock_status(-1, 10),
        lambda: dock_status(11, 10),
    ],
)
def test_invalid_inputs_raise_value_error(call):
    with pytest.raises(ValueError):
        call()
