from hypothesis import given, strategies as st
from bike_share_rental_parser import parse_ride_duration, format_station_code, parse_ride_log

@given(st.text() | st.none())
def test_parse_ride_duration_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_format_station_code_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_ride_log_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass
