from datetime import datetime, timedelta

# Sample start and end dates (naive datetimes)
start_date = datetime(2024, 7, 12, 12, 0, 0)
end_date = datetime(2024, 7, 12, 18, 0, 0)

# Define the UTC+05:30 offset
utc_offset = timedelta(hours=5, minutes=30)

# Subtract the offset to convert to UTC
start_date_utc = start_date - utc_offset
end_date_utc = end_date - utc_offset

# Print the results
print(start_date_utc)
print(type(start_date))
print(end_date_utc)