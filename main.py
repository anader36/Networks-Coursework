# This project was done by Ahmed Hanafy - TKH ID 202000355 - Year 2 Student
# KH5064 - Networking - School of Computing

# Importing all the libaries required to run the code
from netmiko import ConnectHandler
from scapy.all import *
import netmiko
import schedule
import time
import datetime
import random

# Defining a list which contains all the routers iP address that are available on the network.
routersList = ['192.168.136.30', '192.168.136.31', '192.168.136.32', '192.168.136.33', '192.168.136.34', '192.168.136.35']
switchList = ['192.168.136.29']

# Defining the username and password variable as the credientials used in order to access SSH.
username = 'ahmed'
password = 'CWS911'
# Defining the device type of all routers.
Device_type = 'cisco_ios'

while True:
# A while loop, where each router would connect and retrieve the OSPF Priority Value
    router_priorities = {}
    for router in routersList:
# In able for routers to connect to SSH, the iP address, username, password, and device type are required and retrieved from above.
        connection = netmiko.ConnectHandler(ip=router, username=username, password=password, device_type=Device_type)
# If the connection succeeds and SSH works, a message indicating that the device is connected would print out.
        if isinstance(connection, netmiko.base_connection.BaseConnection):
            print(f'You have successfully connected to router: {router}')
        else:
# If the connection does not succeed and SSH fails to work, a message indicating that the device did not connect will print out.
            print(f'You have failed to connect to the router: {router}')
        connection.secret = password
# Enabling the SSH console.
        connection.enable()
# For designated router, the function will choose a random number to be selected for each router as its priority value.
        priority = random.randint(1,255)
        print(f'Setting OSPF Priority on router {router} to {priority}')
# Accessing the console in order to apply the priority number into each router, then after adding the number, this specific router would be disconnected and the function would apply the priority numbers to the other routers.
        command = f'router ospf 1 priority {priority}'
        output = connection.send_config_set([command])
        router_priorities[router] = priority
        connection.disconnect()
# Checks if the routers list is empty.
    if not router_priorities:
        print("Error: The following dictionary, router_priorities, is empty")
        exit()

# The router with the highest priority would be the designated router, and a message will be printed out indicating the router with the highest value.
    designated_router = max(router_priorities, key=router_priorities.get)
# The designated router will be printed out with the time that the configuration was done on.
    print(f'{datetime.datetime.now()}: The Designated router is {designated_router} with the highest priority {router_priorities[designated_router]}')
# Every 24 hours, a different router will be selected randomly as the designated router.
    time.sleep(86400)

#Connects to the switch
    threat_detected = False
    while True:
        for switch in switchList:
            connection = netmiko.ConnectHandler(ip=switch, username=username, password=password, device_type='cisco_ios')
            #Inputs the command to show the current mac address-table
            command = 'show mac address-table'
            output = connection.send_command(command)
            lines = output.split('\n')
            for line in lines:
                print("Checking the mac address table on the switch")
                # Extract the MAC address from the line
                mac_address = line.split()[1]
                for line in lines:
                    if 'Dynamic' in line:
                        # Extract the MAC address from the line
                        mac_address = line.split()[1]
                        # Set the flag indicating that a threat has been detected
                        threat_detected = True
                        print('Unknown MAC address present')
                        command = f'mac access-list extended BLOCKTHREAT{switch} deny any host {mac_address}'
                        connection.send_config_set([command])
                        print('Unkown mac address successfully blocked')

  # Check if the MAC addresses are in the trusted list and if the PDU is a valid routing PDU from the trusted OSPF domain
if mac_addresses not in trusted_macs or "not a valid OSPF PDU" in mac_addresses:
    # Forward the PDU to the AI application for further inspection
    stdin, stdout, stderr = ssh.exec_command("forward PDU to AI commands here")
    print(stdout.read())
    # Change the operating VLAN connecting the routers to another one and forward a copy to VLAN 88
    stdin, stdout, stderr = ssh.exec_command("change VLAN commands here")
    print(stdout.read())
