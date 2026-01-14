from datetime import datetime, timedelta, timezone

# generates UNIX timestamps for each day of the year
def GenerateUnixTimestamps(year):
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)

    timestamps = []
    current = start

    while current < end:
        timestamps.append(int(current.timestamp()))
        current += timedelta(days=1)

    # print(timestamps)
    return timestamps

def NormalizeYear(hourly_data, year):
    """
    Ensure exactly 8760 hours for a non-leap year.
    """
    start_ts = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
    end_ts = int(datetime(year + 1, 1, 1, tzinfo=timezone.utc).timestamp())

    hourly_data = [
        h for h in hourly_data
        if start_ts <= h["ts"] < end_ts
    ]

    return hourly_data[:8760]

