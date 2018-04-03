#was piece

from configurations import *
import exceptions


def create_device (device, color='white'):  # pretend color is manufacturer and white is cisco
    if isinstance(device, str):
        if device.upper() in SHORT_NAME.keys():
            color = "white"
            device = SHORT_NAME[device.upper()]
        device = device.capitalize()
        if device in SHORT_NAME.values():
            return eval("{classname}(color)".format(classname=device))
    raise exceptions.NetConfError("invalid device name: '{}'".format(device))

def get_numeric_notation(rowcol):
    row, col = rowcol
    return int(col)-1, X_AXIS_LABELS.index(row)

class Device():

    def __init__(self, color):
        self.name = self.__class__.__name__.lower()
        if color == 'black':
            self.name = self.name.lower()
        elif color == 'white':
            self.name = self.name.upper()
        self.color = color
        self.device_name = ""
        self.ip_address = ""
        self.login = ""
        self.password = ""
        self.com = "Telnet"
        self.vendor = ""
        self.model = ""
        self.serial_number = ""
        self.os_version = ""
        self.uptime = ""
        self.type = ""
   
    def keep_reference(self, model):
        self.model = model

class Router(Device):
    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
    max_distance = 20
    def moves_available(self,current_position):
        return super(Router, self).moves_available (current_position, self.directions, self.max_distance)

class Switch(Device):
    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
    max_distance = 20
    def moves_available(self,current_position):
        return super(Switch, self).moves_available (current_position, self.directions, self.max_distance)

def update_device_parameters(dev,name,ip,login,password,com,vendor,model,serial_no,os,uptime,type):
        print("NAME IS (%s) device is (%s)" % (name,dev))
        dev.device_name = name
        dev.ip_address = ip
        dev.login = login
        dev.password = password
        dev.com = com
#,vendor,model,serial_no,os,uptime,type
        dev.vendor = vendor
        dev.model = model
        dev.serial_number = serial_no
        dev.os_version = os
        dev.uptime = uptime
        dev.type = type
        
