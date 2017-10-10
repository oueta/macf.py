#!/usr/bin/env python3
import os
import sys
import re
import urllib.request
import csv
path = os.path.dirname(os.path.realpath(__file__))
def search_csv(csv_path, search):
    with open(csv_path, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            if row and len(row) > 3:
                if row[1].upper() == search.upper():
                    return row
def bit_reverse(x):
    x = int(x, 16)
    reverse = 0
    position = 7;
    for position in range(7,0,-1):
        reverse += (x & 1) << position
        x >>= 1
    return hex(reverse + x)[2:].zfill(2)
iab_url = 'https://standards.ieee.org/develop/regauth/iab/iab.csv'
iab_file = path + '/iab.csv'
mas_url = 'https://standards.ieee.org/develop/regauth/oui36/oui36.csv'
mas_file = path + '/mas.csv'
mam_url = 'https://standards.ieee.org/develop/regauth/oui28/mam.csv'
mam_file = path + '/mam.csv'
mal_url = 'https://standards.ieee.org/develop/regauth/oui/oui.csv'
mal_file = path + '/mal.csv'
if len(sys.argv) > 1:
    if sys.argv[1] == '-d':
        try:
            print("Downloading IAB..")
            urllib.request.urlretrieve(iab_url, iab_file)
            print("Downloading small block..")
            urllib.request.urlretrieve(mas_url, mas_file)
            print("Downloading medium block..")
            urllib.request.urlretrieve(mam_url, mam_file)
            print("Downloading large block..")
            urllib.request.urlretrieve(mal_url, mal_file)
            print("Done!")
        except:
            if os.path.isfile(iab_file): os.remove(iab_file)
            if os.path.isfile(mas_file): os.remove(mas_file)
            if os.path.isfile(mam_file): os.remove(mam_file)
            if os.path.isfile(mal_file): os.remove(mal_file)
            print("Incomplete download, files deleted")
    else:
        mac_pattern = re.compile("^[0-9a-f.,:-]+$", re.IGNORECASE)
        char_pattern = re.compile("^[0-9a-f]$", re.IGNORECASE)
        if mac_pattern.search(sys.argv[1]) is not None:
            input_mac = sys.argv[1].lower()
            trim_mac = ""
            for i in range(len(input_mac)):
                if char_pattern.search(input_mac[i]) is not None:
                    trim_mac += input_mac[i]
            if len(trim_mac) != 12:
                print("It's too short" if len(trim_mac) < 12 else "It's too long")
            else:
                if os.path.isfile(mal_file) and os.path.isfile(mam_file) and os.path.isfile(mas_file):
                    found_row = search_csv(iab_file, trim_mac[0:9])
                    if found_row is None:
                        found_row = search_csv(mas_file, trim_mac[0:9])
                        if found_row is None:
                            found_row = search_csv(mam_file, trim_mac[0:7])
                            if found_row is None:
                                found_row = search_csv(mal_file, trim_mac[0:6])
                    print(found_row[2] if found_row is not None else "Unknown Vendor")
                # globally/locally = 0/1
                locally = (int(trim_mac[0:2], 16) & 2) >> 1
                print("Globally unique" if locally == 0 else "Locally administered")
                # unicast/multicast = 0/1
                multicast = int(trim_mac[0:2], 16) & 1
                print("Unicast" if multicast == 0 else "Multicast")
                # bit-reversed notation
                if len(sys.argv) > 2 and sys.argv[2] == "-r":
                    tmp_mac = ""
                    for i in range(0,12,+2): tmp_mac += bit_reverse(trim_mac[i:i+2])
                    trim_mac = tmp_mac
                # trimmed
                print(trim_mac)
                # colon
                print("{}{}:{}{}:{}{}:{}{}:{}{}:{}{}".format(*trim_mac))
                # dash
                print("{}{}-{}{}-{}{}-{}{}-{}{}-{}{}".format(*trim_mac))
                # cisco
                print("{}{}{}{}.{}{}{}{}.{}{}{}{}".format(*trim_mac))
                # huawei
                print("{}{}{}{}-{}{}{}{}-{}{}{}{}".format(*trim_mac))
        else:
            print("Illegal characters")
else:
    print("Usage: ./macf.py 1A:2B:3C:4D:5E:6F")
    print("-d Download IEEE Public database")
    print("-r Print bit-reversed notation")
