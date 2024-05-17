import datetime


def get_next_10_minute_range():
    current_time = datetime.datetime.now().time()
    next_10_minutes = (current_time.minute // 10 + 1) * 10
    if next_10_minutes == 60:
        next_10_minutes = 0
        current_hour = current_time.hour + 1
    else:
        current_hour = current_time.hour
    next_time10 = current_time.replace(hour=current_hour, minute=next_10_minutes, second=0, microsecond=0)

    next_20_minutes = (current_time.minute // 10 + 1) * 10 + 10
    if next_20_minutes > 60:
        next_20_minutes -= 60

    elif next_20_minutes == 60:
        next_20_minutes -= 60
        current_hour += 1
    next_time20 = current_time.replace(hour=current_hour, minute=next_20_minutes, second=0, microsecond=0)

    final_time = next_time10.strftime("%H:%M") + " - " + next_time20.strftime("%H:%M")

    return final_time


def get_current_10_minute_range():
    current_time = datetime.datetime.now().time()
    current_10_minutes = (current_time.minute // 10) * 10
    current_time10 = current_time.replace(minute=current_10_minutes, second=0, microsecond=0)

    # Check if adding 10 minutes would exceed 59 minutes
    if current_10_minutes == 50:
        current_time20 = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
    else:
        current_time20 = current_time.replace(minute=current_10_minutes + 10, second=0, microsecond=0)

    final_time = current_time10.strftime("%H:%M") + " - " + current_time20.strftime("%H:%M")

    return final_time

print('nextone')
print(get_next_10_minute_range())
print('current')
print(get_current_10_minute_range())

