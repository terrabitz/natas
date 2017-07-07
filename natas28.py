import requests
from requests.auth import HTTPBasicAuth
import logging
import string
import base64
from urllib.parse import urlparse, parse_qs
import shutil
import random
from termcolor import colored, cprint
import sys

logging.basicConfig(level=logging.INFO)

url = "http://natas28.natas.labs.overthewire.org/index.php"
level_username = "natas28"
level_password = "JWwR438wkgTsNKBbcJoowyysdM82YjeF"
block_size = 16
offset = 10

auth = HTTPBasicAuth(level_username, level_password)

# Utilities #############################################################
def bytes_to_hex_array(bytes):
    return ['{0:0{1}x}'.format(c, 2) for c in bytes]


def print_blocks(bytes_arr, block_size=16):
    hex_arr = bytes_to_hex_array(bytes_arr)
    i = 0
    while len(hex_arr) > 0:
        i += 1
        print(hex_arr.pop(0), end=" ")
        if i == block_size:
            i = 0
            print()


def print_start(input):
    print("#" * shutil.get_terminal_size().columns)
    print("Input: " + input)
    print()


def send_encrypted_query(bytes_arr):
    query = bytes(bytes_arr)
    encoded_query = base64.b64encode(query)
    res = requests.get(url, auth=auth, params={'query': encoded_query})
    # logging.debug(res.text)
    return res


def has_valid_padding_size(bytes_arr):
    res = send_encrypted_query(bytes_arr)
    if 'Incorrect amount of PKCS#7 padding for blocksize' in res.text:
        return False
    else:
        return True


def has_valid_padding(bytes_arr):
    res = send_encrypted_query(bytes_arr)
    if "Invalid PKCS#7 padding encountered" in res.text:
        return False
    else:
        return True


def modify_array(bytes_arr):
    print("Modifying array...")
    for idx in range(16):
        current = bytes_arr[idx]
        bytes_arr[idx] = (current + random.randint(1, 30)) % 256
    return bytes_arr


def get_encrypted_query_from_plaintext(input):
    res = requests.post(url, auth=auth, data={'query': input})
    query_param = parse_qs(urlparse(res.url).query)['query'][0]
    decoded_query = base64.b64decode(query_param)
    query_array = bytearray(decoded_query)
    return query_array


def has_repeating_blocks(bytes_arr, block_size=16):
    logging.debug(bytes_arr)
    for i in range(0, len(bytes_arr) - block_size, block_size):
        block_1 = bytes_arr[i:i + block_size]
        block_2 = bytes_arr[i + block_size:i + block_size * 2]

        logging.debug(block_1)
        logging.debug(block_2)

        if block_1 == block_2:
            return i

    return False


def get_offset():
    iterator = ["b" * i + "a" * block_size * 2 for i in range(block_size)]
    for idx, i in enumerate(iterator):
        print_start(i)
        query_array = get_encrypted_query_from_plaintext(i)
        repeating_blocks_start_index = has_repeating_blocks(query_array)
        text_output = "Has repeating blocks: " + str(bool(repeating_blocks_start_index))
        if repeating_blocks_start_index:
            print_blocks(query_array)
            cprint(text_output, 'green')
            cprint('Offset: ' + str(offset), 'green')
            cprint('Start Index: ' + str(repeating_blocks_start_index), 'green')
            return offset, repeating_blocks_start_index
        print(text_output)


if __name__ == "__main__":
    offset, start_index = get_offset()
    size_to_find = block_size * 2
    match_index_start = start_index
    match_index_end = start_index + size_to_find

    found = ""
    for current_char in range(size_to_find):
        plaintext_to_match = 'b' * offset + 'a' * (size_to_find - len(found) - 1)
        query_to_match = get_encrypted_query_from_plaintext(plaintext_to_match)
        query_slice_to_match = query_to_match[match_index_start:match_index_end]

        cprint("Encrypted slice to match: ", 'blue')
        print_blocks(query_slice_to_match)

        for char in string.printable:
            query_input = plaintext_to_match + found + char
            print_start(query_input)
            query_output = get_encrypted_query_from_plaintext(query_input)
            query_array_slice = query_output[match_index_start:match_index_end]

            print('Checking: ')
            print_blocks(query_array_slice)

            if query_array_slice == query_slice_to_match:
                print()
                cprint("Matching slice: ", 'blue')
                print_blocks(query_array_slice)
                print()

                found += char
                cprint('Found matching char: ' + char, 'green')
                cprint('Current string: ' + found, 'green')
                break
        else:
            cprint("Byte not found. Exiting...", 'red')
            sys.exit(1)
