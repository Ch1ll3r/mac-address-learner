import argparse
import json
import sys
import logging as log


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
# Main
# -------------------------------------------------------------------

#################################
###Begin Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Python script to change passwords
    Example: changePassword -f hostname.txt -vcd
""")
    parser.add_argument('-f', '--file', help='File containing hierarchy', default='switches.json')
    parser.add_argument('-g', '--jsonFilePath', action='store_const', const=True, help='json output file',
                        default="json.json")
    parser.add_argument('-l', '--learn', action='store_const', const=True, help='learn ports')
    parser.add_argument('-k', '--csv', action='store_const', const=True, help='the hierarchy is csv')
    parser.add_argument('-v', '--verbose', action='store_const', const=True, help='verbose mode')
    parser.add_argument('-c', '--create', action='store_const', const=True, help='create hierarchy')
    parser.add_argument('-t', '--test', action='store_const', const=True, help='test')

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
            log.info("learning started for " + switch['name'])

    #################################
