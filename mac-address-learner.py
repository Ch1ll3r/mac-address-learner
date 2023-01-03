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
    df2 = pd.DataFrame(columns=["mac", "interface"])

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
                    df3 = pd.DataFrame(columns=["mac", "interface"])
                    df3 = pd.DataFrame([[mac, interface]], columns=["mac", "interface"])
                    df3 = pd.DataFrame([["0100.0ccc.cccc", "CPU"]], columns=["mac", "interface"])
                    # check if mac is already in DF
                    if df3.isin(df2).any():
                        print("found df3 in df2")

                    df2.loc[len(df2)] = [mac, interface]


    print("completed df")
    print(df2)
    return 0


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
