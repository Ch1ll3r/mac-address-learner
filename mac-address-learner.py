import argparse
import json
import logging as log
import sys
import genie
import pyats
import re
import netmiko
import numpy as np
import pandas as pd
from netmiko import ConnectHandler


# -------------------------------------------------------------------
# Info
# -------------------------------------------------------------------
# Author: Cedric Metzger
# Mail: cmetzger@itris.ch / support.one@itris.ch
# Version: 0.1 / 21.12.2022
# Comment of the author: Your focus determines your reality. — Qui-Gon Jinn

# -------------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# FUNCITONS
# -------------------------------------------------------------------


def learnmacaddress(device):
    sshex = False
    db = pd.DataFrame(columns=["mac", "interface"])

    try:
        with ConnectHandler(ip=device["host"],
                            username=device["user"],
                            password=device["password"],
                            device_type=device["device_type"]) as connection:
            command = "show mac address-table"
            mactable = connection.send_command(command, use_genie=True)

    except Exception as e:
        sshex = True
        log.error("failed for " + device["name"] + " with exception ")
        log.error(e)

    if not sshex:
        for vlan in mactable["mac_table"]["vlans"]:
            for mac in mactable["mac_table"]["vlans"][vlan]["mac_addresses"]:
                for interface in mactable["mac_table"]["vlans"][vlan]["mac_addresses"][mac]["interfaces"]:
                    macinterface_entry = pd.DataFrame([[mac, interface]], columns=["mac", "interface"])
                    log.info("checking for " + macinterface_entry)
                    # add first Entry
                    log.info("DB has " + str(len(db)) + " entry/entries")
                    if db.empty:
                        log.info("DB empty, adding frist entry")
                        db.loc[len(db)] = [mac, interface]
                    # checking if additionals entries are already in the db
                    elif not db.empty:
                        log.info("checking for macinterface is in db mac")
                        # only adding the entry, if there is no entry for the same mac-interface combo yet

                        mask = macinterface_entry[['mac', 'interface']].isin(db[['mac', 'interface']]).all(axis=1)
                        # Check if any rows are duplicates
                        if mask.any():
                            log.info('already found, not adding it')
                        else:
                            log.info(macinterface_entry + "is not yet in DB, adding it")
                            db.loc[len(db)] = [mac, interface]
    log.info("learn mac address complete, return db")
    return db


def updatedatabase(db):
    return 0


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Python script to learn mac addresses of connected ports
    Example: mac-address-learner.py -lv
""")
    parser.add_argument('-f', '--file', help='file Containing switches', default='switches.json')
    parser.add_argument('-d', '--database', help='database File', default='db.json')
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
            # connect to switch
            # learn mac address table
            # Update db.json

    #################################
