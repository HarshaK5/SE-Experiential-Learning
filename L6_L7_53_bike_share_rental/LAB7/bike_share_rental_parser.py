def parse_ride_duration(text):
    """
    Converts a ride duration written as HH:MM into minutes.
    Returns 0 when the input is missing or malformed.
    """
    if not isinstance(text, str):
        return 0

    parts = text.strip().split(':')
    if len(parts) != 2:
        return 0

    try:
        hours, minutes = (int(part) for part in parts)
    except ValueError:
        return 0

    if hours < 0 or not 0 <= minutes < 60:
        return 0
    return hours * 60 + minutes

def format_station_code(code):
    """
    Formats a station code as ZONE-NUMBER, e.g. 'a12' -> 'A-12'.
    Returns an empty string when the input is missing or empty.
    """
    if not isinstance(code, str):
        return ''

    code = code.strip().upper()
    if not code:
        return ''
    return code[0] + '-' + code[1:]

def parse_ride_log(line):
    """
    Parses 'bike_type,minutes,subscriber' into a tuple.
    Returns a neutral tuple when the input is missing or malformed.
    """
    if not isinstance(line, str):
        return '', 0, False

    parts = line.split(',')
    if len(parts) < 3:
        return '', 0, False

    try:
        minutes = int(parts[1].strip())
    except ValueError:
        return '', 0, False

    return parts[0].strip(), minutes, parts[2].strip() == 'yes'

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
