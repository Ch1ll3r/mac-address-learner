# MAC Address Learner
This script reads mac addresses out of the mac address table of Cisco switches. It creates and updates a csv 
containing the mac address and the interface, where the mac address has been seen.

## restrictions
The script is prepared to handle multiple switches, but currently only works with a single switch. If you want to
monitor multiple switches, start the script multiple times.
 
**Warning:** We do not guarantee a correct learning, always verify the output by yourself

## Prerequisites
- [Python requirements installed](#Install-dependencies)
- [Script Confniguration](#Script-Configuration)

## Installation
### Clone the repository
```
$ git clone https://github.com/Ch1ll3r/mac-address-learner
```
**Python version 3** and pip3 is required. Creating a dedicated virtual environment is recommended.

### Creating a virtual environment (optional)

Install the virtualenv package:
```
$ python3 -m pip3 install virtualenv
```
Create and activate a new virtual environment:
```
$ python3 -m venv ./venv
$ source venv/bin/activate
```

### Install dependencies

```
$ python3 -m pip3 install -r requirements.txt
```

### Script Configuration
Edit the script and add your credentials for the switch in switches.json:
```
{
    "switches":[
      {
        "device_type": "cisco_ios",
        "name": "switch1",
        "host": "192.168.1.1",
        "user": "Cisco",
        "password": "Cisco",
        "enablepw": "Cisco"
      }
  ]
}
```
## How to Use
You can use the script with command line arguments.
- -l is for learning and initiates the learning proccess of the script
- -d is to specify a different database-file (default db.txt)
- -f is to specify a different switches-file (default switches.json)
- -v is for Info-level logging

Normal Usage:
```
$ python3 mac-address-learner.py -lv
```
