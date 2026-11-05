def parse_ride_duration(text):
    """
    Converts a ride duration written as HH:MM into minutes.
    Assumes text always has exactly one colon with digits on both sides.
    """
    hours, minutes = text.strip().split(':')
    return int(hours) * 60 + int(minutes)

def format_station_code(code):
    """
    Formats a station code as ZONE-NUMBER, e.g. 'a12' -> 'A-12'.
    Assumes code is a non-empty string.
    """
    code = code.strip().upper()
    return code[0] + '-' + code[1:]

def parse_ride_log(line):
    """
    Parses 'bike_type,minutes,subscriber' into a tuple.
    Assumes all three fields are present and minutes is an integer.
    """
    parts = line.split(',')
    return parts[0].strip(), int(parts[1]), parts[2].strip() == 'yes'

def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    print("Duration in minutes:", parse_ride_duration(value))

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    print("Formatted station code:", format_station_code(value))

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    print("Parsed ride log:", parse_ride_log(value))

if __name__ == "__main__":
    main()
