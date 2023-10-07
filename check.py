"""
Checks if a selected server is full.
"""

import time
import winsound
from win10toast import ToastNotifier

import check_server
import DebugLogs

if __name__ == '__main__':

    delay = 30

    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second

    print("\nPlease input the server you want to check (Ex: Delphnius).\nMust be formatted correctly! (Press Enter to "
          "use default): ")

    server_name = input()
    if server_name == "":
        server_name = "Delphnius"

    DebugLogs.debug.log(f"Server Name selected: {server_name}")

    toast = ToastNotifier()

    while True:

        extra_delay = [0]

        result = check_server.check_status(server_name, extra_delay)
        if result:
            DebugLogs.debug.log("Found the server!")
            winsound.Beep(frequency, duration)
            toast.show_toast(
                "New World Server",
                f"The server now allows character transfer!",
                duration=20,
                icon_path="data/icon.ico",
                threaded=True,
            )
            break

        time.sleep(delay + extra_delay[0])

    winsound.Beep(frequency, duration*2)
    DebugLogs.debug.log("Found the requested server, stopping now.")
