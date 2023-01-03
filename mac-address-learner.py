import argparse
import json
import logging as log
import sys
import pandas as pd
from netmiko import ConnectHandler


# -------------------------------------------------------------------
# Info
# -------------------------------------------------------------------
# Author: Cedric Metzger
# Mail: cmetzger@itris.ch / support.one@itris.ch
# Version: 1.0 / 03.01.2023
# Comment of the author: Your focus determines your reality. — Qui-Gon Jinn

# -------------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# FUNCITONS
# -------------------------------------------------------------------


def learnmacaddress(device):
    sshexception = False
    try:
        with ConnectHandler(ip=device["host"],
                            username=device["user"],
                            password=device["password"],
                            device_type=device["device_type"]) as connection:
            command = "show mac address-table"
            mactable = connection.send_command(command, use_genie=True)

    except Exception as e:
        sshexception = True  # setting to true if there was an exception while connection to the switch
        log.error("failed for " + device["name"] + " with exception ")
        log.error(e)

    if not sshexception:
        for vlan in mactable["mac_table"]["vlans"]:
            for mac in mactable["mac_table"]["vlans"][vlan]["mac_addresses"]:
                for interface in mactable["mac_table"]["vlans"][vlan]["mac_addresses"][mac]["interfaces"]:
                    updatedatabase(mac, interface)

    log.info("learn mac address complete")
    return 0


def updatedatabase(mac, interface):
    macinterface_entry = pd.DataFrame([[mac, interface]], columns=["mac", "interface"])
    log.info("checking for " + macinterface_entry['mac'] + ' ' + macinterface_entry['interface'])
    try:
        # try to open database
        db = pd.read_csv(args.database, sep=";", names=["mac", "interface"])
    except FileNotFoundError:
        # If the file does not exist, create it and write a header line
        with open("db.txt", "w") as file:
            file.write("mac;interface\n")
        # Create an empty dataframe with the correct column names
        db = pd.DataFrame(columns=["mac", "interface"])

    # add first Entry
    log.info("DB has " + str(len(db)) + " entry/entries")
    if db.empty:
        log.info("DB empty, adding frist entry")
        db.loc[0] = [mac, interface]
        # write to the database w/ headers
        db.to_csv(args.database, sep=";", index=False)
    # checking if additionals entries are already in the db
    elif not db.empty:
        log.info("checking for macinterface is in db mac")
        # only adding the entry, if there is no entry for the same mac-interface combo yet
        db = pd.merge(db, macinterface_entry, on=['mac', 'interface'], how='outer').drop_duplicates()
        # write to the database w/o headers
        db.to_csv(args.database, sep=";", index=False, header=False)
    return 0

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Python script to learn mac addresses of connected ports
    Example: mac-address-learner.py -lv
""")
    parser.add_argument('-f', '--file', help='file Containing switches', default='switches.json')
    parser.add_argument('-d', '--database', help='database File', default='db.txt')
    parser.add_argument('-v', '--verbose', action='store_const', const=True, help='active verbosed logs')
    parser.add_argument('-l', '--learn', action='store_const', const=True, help='learn ports')

    args = parser.parse_args()
    # mandatory arguments
    if not args.file:
        log.error("Exiting. Filename is mandatory.")
        sys.exit(1)

    if args.verbose:
        log.basicConfig(level=log.INFO)

    if args.learn:
        with open('switches.json') as f:
            data = json.load(f)

        for switch in data['switches']:
            log.info("learning started for " + switch['host'])
            learnmacaddress(switch)
    #################################