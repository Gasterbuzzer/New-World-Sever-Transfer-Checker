"""
Single Module to check the status of a requested server.
"""

import requests
import DebugLogs.debug
from bs4 import BeautifulSoup


def check_status(server_name: str, request_delay: list, url: str = "https://www.newworld.com/en-us/support/server"
                                                                   "-status"):
    """
    Checks the status of a server.
    :param request_delay: List of one element containing an integer which can be used to delay a request if met with
    api limit.
    :param server_name: Server Name must be typed correctly.
    :param url: (Leave default if you do not know)
    """
    response = requests.get(url)

    if response.status_code != 200:
        DebugLogs.debug.log_e("Request failed with status code: " + str(response.status_code))
        request_delay[0] += 30
        return False

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the <div> element with the specified class
    server_divs = soup.find_all("div", class_="ags-ServerStatus-content-responses-response-server")

    # Check if the element was found
    for server_div in server_divs:
        # Find the nested <div> element with class "ags-ServerStatus-content-responses-response-server-name"
        server_name_div = server_div.find("div", class_="ags-ServerStatus-content-responses-response-server-name")

        # Extract the text content if the nested <div> element is found
        if server_name_div:
            _server_name = server_name_div.get_text(strip=True)  # Extract text and remove leading/trailing spaces

            if server_name == _server_name:

                # Find the status <div> element within the same parent <div>
                status_div = server_div.find("div",
                                             class_="ags-ServerStatus-content-responses-response-server-status"
                                                    "--noTransfer")
                status_up_div = server_div.find("div",
                                                class_="ags-ServerStatus-content-responses-response-server-status--up")

                # Check if the status <div> element with the specific title exists
                if status_div and status_up_div and status_div.get("title") == "Character transfer is unavailable":
                    print("Server Status:", status_up_div.get("title"))
                    print("Server Name:", server_name)
                    print("Transfer Status: Character transfer is unavailable")

                    status_full_div = server_div.find("div",
                                                      class_="ags-ServerStatus-content-responses-response-server"
                                                             "-status--full")

                    if status_full_div:
                        status_full = status_full_div.get("title")
                        print("Status: Is it Full?:", status_full, "\n")

                    return False
                else:
                    print("Server Name:", server_name)
                    print("Transfer Status: Character transfer is available!!!\n")
                    return True

        else:
            DebugLogs.debug.log_e(
                "Element with class 'ags-ServerStatus-content-responses-response-server-name' not found inside the "
                "parent <div>. Wrong url?")

            return True

    DebugLogs.debug.log_e("Could not find server name.")
    return True


if __name__ == '__main__':
    delay = [0]
    print(check_status("Delphnius", delay))
