# L6_L7_53 — Bike Share Rental

Lab 6: Code and Branch Coverage

## About

A small Python module that prices bike-share rides by bike type, duration and subscription, reports dock status and decides whether a rider may unlock a bike.

## Files

| File | Description |
|------|-------------|
| `bike_share_rental.py` | The module under test |
| `test_bike_share_rental.py` | Starter examples |
| `CodeCoverageTest_53_bike_share_rental.py` | Tests for line/code coverage |
| `BranchCoverageTest_53_bike_share_rental.py` | Tests for branch coverage |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.

## Running the tests and coverage

From this directory, install the test dependencies if needed:

```bash
python -m pip install pytest coverage
```

Run the tests and measure line coverage:

```bash
python -m coverage run -m pytest CodeCoverageTest_53_bike_share_rental.py
python -m coverage report -m
```

Run the tests and measure branch coverage:

```bash
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_53_bike_share_rental.py
python -m coverage report -m
```

The test suites are designed to cover the valid, boundary, and invalid-input
paths of all three public functions.
