from datetime import datetime, timedelta
import sys

window_size = 5 

if len(sys.argv) != 3:
    print("script.py <start-time> <end-time>")
    sys.exit()

def generate_windows(start_str, end_str):
    
    start_time = datetime.strptime(start_str, "%H:%M:%S")
    end_time = datetime.strptime(end_str, "%H:%M:%S")

    total_seconds = int((end_time - start_time).total_seconds())
    total_windows = total_seconds // window_size

    print(f"Total windows: {total_windows}\n")

    for window_number in range(total_windows):
        window_start = start_time + timedelta(seconds=window_number * window_size)
        window_end = window_start + timedelta(seconds=window_size)

        print(
            f"Window {window_number:03d}: "
            f"{window_start.strftime('%H:%M:%S')} - "
            f"{window_end.strftime('%H:%M:%S')}"
        )

start = sys.argv[1]
end = sys.argv[2]
generate_windows(start, end)
