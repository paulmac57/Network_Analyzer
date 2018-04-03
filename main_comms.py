#telnet-example from https://docs.python.org/3/library/telnetlib.html
import time
import pickle
from getpass import getpass

import ssh_connection as ssh
import telnet_connection as telnet
from show_version_parser import process_show_version
import show_cdp_neighbors_parser as cdp

class NetworkDevice(object):
    """Container for network device attributes."""
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.show_version = ""
       
##        self.show_version = """Cisco Internetwork Operating System Software 
##
##        IOS (tm) C2600 Software (C2600-I-M), Version 12.3(5), RELEASE SOFTWARE (fc1)
##
##        Copyright (c) 1986-2003 by cisco Systems, Inc.
##
##        Compiled Tue 28-Oct-03 05:07 by kellythw
##
##        Image text-base: 0x80008098, data-base: 0x80CA4288
##
##        
##
##        ROM: System Bootstrap, Version 11.3(2)XA4, RELEASE SOFTWARE (fc1)
##Preston uptime is 48 minutes
##
##        System returned to ROM by power-on
##
##        System image file is "flash:c2600-i-mz.123-5.bin"
##
##        
##
##        cisco 2610 (MPC860) processor (revision 0x203) with 45056K/4096K bytes of memory.
##
##        Processor board ID JAD05060SLY (1836265265)
##
##        M860 processor: part number 0, mask 49
##
##        Bridging software.
##
##        X.25 software, Version 3.0.0.
##
##        1 Ethernet/IEEE 802.3 interface(s)
##
##        1 Serial network interface(s)
##
##        32K bytes of non-volatile configuration memory.
##
##        16384K bytes of processor board System flash (Read/Write)
##
##        
##
##        Configuration register is 0x2102
##
##        Preston>"""


def ssh_main():
    """Process show version using SSH."""
    ip = input("Enter IP Address: ")
    username = ''
    password = getpass()

    test_device = NetworkDevice(ip, username, password)

    (remote_conn_pre, remote_conn, _) = ssh.establish_connection(ip, username, password)
    ssh.disable_paging(remote_conn)
    remote_conn.send(b"\n")
    remote_conn.send(b"show version\n")

    # Read the output from the 'show version' command
    test_device.show_version = ssh.read_ssh_data(remote_conn)
    remote_conn_pre.close()
    process_show_version(test_device)

    # Print to stdout for verification
    net_device_verification(test_device)

    # Write object to a file
    with open('ssh_file.pkl', 'wb') as f:
        pickle.dump(test_device, f)

def show_version(remote_connection,device):
    
    device.ip_address = remote_connection.ip
    device.show_version = telnet.show_version(remote_connection.remote_conn)
    time.sleep(1)
    remote_connection.remote_conn.close()
    process_show_version(device)
    write_pickle(device)

def show_cdp_neighbors(remote_connection,device):
    device.ip_address = remote_connection.ip
    device.show_cdp_neighbors = telnet.show_cdp_neighbors(remote_connection.remote_conn)
    time.sleep(1)
##    print ("NEIGBOURS ARE ")
##    print(device.show_cdp_neighbors)
    cdp.process_show_cdp_neighbors(remote_connection,device)
    cdp.show_cdp_detail(remote_connection,device)
   
    
    remote_connection.remote_conn.close()
  

def set_hostname(new_name,remote_connection, device):
    time.sleep(1)
    command="\nhostname "+new_name
    print (command)
    device.ip_address = remote_connection.ip
    telnet.set_hostname(remote_connection.remote_conn,command)
    time.sleep(1)
    remote_connection.remote_conn.close()
    write_pickle(device)

    
def write_pickle(the_device):
    ip = the_device.ip_address
    # Print to stdout for verification
    #net_device_verification(the_device)
    #Write object to a file
    with open("Devices/"+ip+".pkl", 'wb') as f:
       pickle.dump(the_device, f)    


def telnet_main(ip_address,login,passw):
    """Process show version using telnet."""
    ##  ALLOWS ME TO SWITCH OFF RoUTERS and switches for nOW
    #ip = input("Enter IP Address: ")
    ip = "192.168.0.118"
    #ip = ip_address
    #password = passw
    username = login
    password= "cisco"
    #password = getpass()
    

    tmp_device2 = NetworkDevice(ip, username, password)

    tmp_device2.remote_conn = telnet.establish_connection(ip, username, password)
    t = telnet.disable_paging(tmp_device2.remote_conn)
    print ("disable paging = "+t) 
    #print(test_device2.show_version)
##    remote_conn.write(b"\n")
##    remote_conn.write(b"show version\n")
##
##    time.sleep(1)
##    test_device2.show_version = remote_conn.read_very_eager().decode()
    return tmp_device2


def net_device_verification(net_device):
    """Prints out a set of attributes for a NetworkDevice object."""
    print_attr = [
        'hostname',
        'ip',
        'username',
        'password',
        'device_type',
        'vendor',
        'model',
        'os_version',
        'uptime',
        'serial_number',
    ]

    # Uses getattr to get the right attribute
    for field in print_attr:
        val = getattr(net_device, field)
        print ("%15s: %-40s" % (field, val))
    print()


def main():
    """
    Login to a network device (using either telnet or SSH) and retrieve 'show version'
    from the device.
    """
    print()
    print ("Using SSH:")
    #ssh_main()

    print ("Using telnet:")
    telnet_main()

    print ("\n")
    print ("Reading objects from pickle files:")
    my_files = ['ssh_file.pkl', 'telnet_file.pkl']
    for a_file in my_files:
        with open(a_file, 'rb') as f:
            netdev_obj = pickle.load(f)
            net_device_verification(netdev_obj)


if __name__ == "__main__":
    main()
