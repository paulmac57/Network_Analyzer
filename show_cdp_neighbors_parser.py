import re
from uptime import Uptime
from ciscoconfparse import CiscoConfParse
import io
import time



def process_show_cdp_neighbors(remote_conn,net_device):
    '''
    
    '''

    show_cdp_neighbors = net_device.show_cdp_neighbors
    

    target = open("Devices/showcdp.txt", 'w')
    target.write(show_cdp_neighbors)
    target.close()
 
    
    #parse = CiscoConfParse("Devices/showcdp.txt")
    #interfaces = parse.find_objects("*Ser" or "*Eth")
    #print ("Interafcaes")
    #print (interfaces)

    # Process show_version output
##    net_device.vendor, net_device.model = obtain_vendor_model(show_ver)
##    net_device.os_version = obtain_os_version(show_ver)
##    net_device.uptime = obtain_uptime(show_ver)
##    net_device.hostname = obtain_hostname(show_ver)
##    net_device.serial_number = obtain_serial_number(show_ver)
##    net_device.device_type = obtain_device_type(net_device.model)



def show_cdp_detail(remote_conn,device):
    
    '''
    Process the show_cdp neigbors output for device
    Assign the following attributes to the device object
    hostname
    interface type
    interface port
    '''
    
       
    
    for ln in io.open('Devices/showcdp.txt', newline='\r\n'):
     
        b = re.search(r"(.+?) (Ser|Eth) (.+?) (.+?) .*",ln)

        if b:
            print ("gp1= "+b.group(1),
                  "gp2= "+b.group(2),
                  "gp3= "+b.group(3))
            command ="show cdp entry "+b.group(1)+"\n"
            remote_conn.remote_conn.write(command.encode())
            time.sleep(1)
            show_detail = remote_conn.remote_conn.read_very_eager().decode()
            print (show_detail)
    
           
        
    
    # Process show_version output
##    net_device.vendor, net_device.model = obtain_vendor_model(show_ver)
##    net_device.os_version = obtain_os_version(show_ver)
##    net_device.uptime = obtain_uptime(show_ver)
##    net_device.hostname = obtain_hostname(show_ver)
##    net_device.serial_number = obtain_serial_number(show_ver)
##    net_device.device_type = obtain_device_type(net_device.model)


