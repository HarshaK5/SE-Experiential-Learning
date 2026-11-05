import pytest

from bike_share_rental import can_unlock, dock_status, ride_cost


@pytest.mark.parametrize(
    "bike_type, minutes, subscriber, peak, expected",
    [
        ("standard", 30, False, False, 20),
        ("electric", 31, False, True, 85),
        ("cargo", 31, False, True, 100),
        ("standard", 30, True, False, 0),
        ("standard", 31, True, False, 20),
        ("standard", 181, False, False, 240),
    ],
)
def test_ride_cost_branches(bike_type, minutes, subscriber, peak, expected):
    assert ride_cost(bike_type, minutes, subscriber, peak) == expected


@pytest.mark.parametrize(
    "bike_type, minutes",
    [
        ("unicycle", 30),
        ("standard", 0),
        ("standard", -1),
    ],
)
def test_ride_cost_validation_branches(bike_type, minutes):
    with pytest.raises(ValueError):
        ride_cost(bike_type, minutes, False, False)


@pytest.mark.parametrize(
    "bikes_docked, capacity, expected",
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (1, 10, "few bikes"),
        (2, 10, "few bikes"),
        (8, 10, "few slots"),
        (9, 10, "few slots"),
        (5, 10, "available"),
    ],
)
def test_dock_status_branches(bikes_docked, capacity, expected):
    assert dock_status(bikes_docked, capacity) == expected


@pytest.mark.parametrize(
    "bikes_docked, capacity",
    [
        (0, 0),
        (-1, 10),
        (11, 10),
    ],
)
def test_dock_status_validation_branches(bikes_docked, capacity):
    with pytest.raises(ValueError):
        dock_status(bikes_docked, capacity)


@pytest.mark.parametrize(
    "balance, active_ride, age, expected",
    [
        (500, True, 18, False),
        (500, False, 15, False),
        (100, False, 16, True),
        (99, False, 17, False),
        (50, False, 18, True),
        (49, False, 18, False),
    ],
)
def test_can_unlock_branches(balance, active_ride, age, expected):
    assert can_unlock(balance, active_ride, age) is expected
