import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.colorchooser import *
from configparser import ConfigParser
import configurations
import exceptions
import serialcommands
import main_comms
import device_window_advanced
import time
import pickle



class DeviceSetupWindow(object):

    def __init__(self, view, dev_pos):
        #self.setup_window = None
        self.device_position = dev_pos
        self.pos_var = StringVar()
        self.name_var = StringVar()
        self.dev_var = StringVar()
##        print("TYPE")
##        print(type (self.name_var))
        self.ip_var = StringVar()
        self.login_var = StringVar()
        self.password_var = StringVar()
        self.com_var = StringVar()
        
        self.parent = view.parent
        self.view = view
        self.create_device_comms_window(dev_pos)

    def device_setup_preference(self):
        
        #self.port_var.set(configurations.PORT)
        #self.speed_var.set(configurations.SPEED)
        #self.bits_var.set(configurations.BITS)
        #self.stop_var.set(configurations.STOP)
        #self.parity_var.set(configurations.PARITY)
        pass
       
    def create_device_comms_window(self,dev_position):
        #if not self.setup_window:
        device = self.view.controller.get_device_at(dev_position)
        if device:
            position = self.view.controller.get_numeric_notation(dev_position)
            #print ("DEVICE IS (%s) POSITION IS (%s)", % (device,position))
            y = position[0] * 32 
            x = position[1] * 64 + 192
            self.setup_window = Toplevel(self.parent)
            self.setup_window.geometry('%dx%d+%d+%d' % (380, 300, x,y))
            
            self.setup_window.title("Device (%s)" % device.device_name)
            self.setup_window.transient(self.parent)
            self.setup_window.lift()
            self.create_setup_fields(dev_position)
           
            #self.setup_window.focus_set()
            #self.setup_window.transient(self.parent)
            #self.setup_window.grab_set()
            #self.parent.wait_window(self.setup_window)
            

   

    def create_setup_fields(self,dev_pos):

        
        com_list = ("Serial","Telnet","SSH",)

        Label(self.setup_window, text='Position').grid(row=0, column=0, sticky=W, padx=5, pady=5)
        dev = Entry(self.setup_window, state=DISABLED, textvariable=self.pos_var)
        dev.grid(row=0, column=1, columnspan=2, sticky=W, padx=5, pady=5)
                
        Label(self.setup_window, text='Name of Device').grid(row=1, column=0, sticky=W, padx=5, pady=5)
        
        #Entry(self.setup_window, textvariable=self.name_var).grid(row=0,column=1, columnspan=2, sticky=E, padx=5, pady=5)
        nam = Entry(self.setup_window, textvariable=self.name_var)
        nam.grid(row=1, column=1, columnspan=2, sticky=W, padx=5, pady=5)
        nam.focus_set()
        Label(self.setup_window, text='Default IP address').grid(row=2, column=0, sticky=W, padx=5, pady=5)
        Button(self.setup_window, text="Save", command=self.on_save_button_clicked).grid(
            row=1, column=3, sticky=W, padx=35, pady=5)
       
        Entry(self.setup_window, textvariable=self.ip_var).grid(row=2,column=1, columnspan=2, sticky=W, padx=5, pady=5)
        
        Label(self.setup_window, text='Login Name').grid(row=3, column=0, sticky=W, padx=5, pady=5)

        Button(self.setup_window, text="Cancel", command=self.on_cancel_button_clicked).grid(
            row=3, column=3, sticky=W, padx=35, pady=5)

        Entry(self.setup_window, textvariable=self.login_var).grid(row=3,column=1, columnspan=2, sticky=W, padx=5, pady=5)
        
        Label(self.setup_window, text='Password').grid(row=4, column=0, sticky=W, padx=5, pady=5)

                
        Entry(self.setup_window, textvariable=self.password_var, show="*").grid(row=4,column=1, columnspan=2, sticky=W, padx=5, pady=5)
        
        Label(self.setup_window, text='Comms Method').grid(row=5, column=0, sticky=W, padx=5, pady=5)

        Button(self.setup_window, text="Delete", command=self.on_delete_button_clicked).grid(
            row=5, column=3, sticky=W, padx=35, pady=5) 

        Spinbox(self.setup_window, values = com_list, textvariable=self.com_var).grid(row=5,column=1, columnspan=2, sticky=W, padx=5, pady=5)

        
        self.set_fields(dev_pos)
       

        Button(self.setup_window, text="Advanced Config", command=self.on_adv_button_clicked).grid(
            row=6, column=0, sticky=SE, padx=5, pady=5)

             
        Label(self.setup_window, text='============================================').grid(row=7, column=0, columnspan=4, sticky=W, padx=5, pady=5)
        Button(self.setup_window, text="Get from Dev", command=self.on_get_button_clicked).grid(
            row=8, column=3, sticky=W, padx=5, pady=5)
        Button(self.setup_window, text="Put to Dev", command=self.on_put_button_clicked).grid(
            row=8, column=0, sticky=W, padx=5, pady=5)
    def set_fields(self,dev_pos):
        
        device = self.view.controller.get_device_at(dev_pos)
        self.pos_var.set(dev_pos)
        self.name_var.set(device.device_name)
        self.ip_var.set(device.ip_address)
        self.login_var.set(device.login)
        self.password_var.set(device.password)
        self.com_var.set(device.com)
        
    def on_get_button_clicked(self):
        com = self.com_var.get()
        ip = self.ip_var.get()
        login = self.login_var.get()
        password = self.password_var.get()
        if com == "Serial":
            messagebox.showinfo(title="Telnet Required", message="Serial Comms not yet Implemented, please use Telnet")
        if com == "Telnet":
            if ip:
                main_comms.telnet_main(ip,login,password)
                print ("Reading objects from pickle files:")
                with open("Devices/"+ip+".pkl", 'rb') as f:
                        netdev_obj = pickle.load(f)
                        #main_comms.net_device_verification(netdev_obj)
                self.name_var.set(netdev_obj.hostname)
            else:
                 messagebox.showinfo(title="IP Required", message="Please set the IP address,\nLogin name and Password \nas required")
                        
        if com == "SSH":
            messagebox.showinfo(title="Telnet Required", message="SSH Comms not yet Implemented, please use Telnet")

    def on_put_button_clicked(self):
        if com == "Serial":
                                    
            a = serialcommands.Connect()
            a.command("")
            time.sleep(1)
            a.command(password)
            time.sleep(1)
            a.command("enable")
            time.sleep(1)
            a.command("sh ip int br")
        if com == "Telnet":
            pass
        if com == "SSH":
            pass
        

    def on_adv_button_clicked(self):
       
        self.show_advanced_window()
        
    def on_delete_button_clicked(self):

        position = str(self.pos_var.get())
        self.view.controller.delete_device(position)
        self.view.draw_board()
        self.view.draw_all_devices()
        self.setup_window.destroy()
        
    def on_save_button_clicked(self):

        position = str(self.pos_var.get())
        #print ("POSITIOn is ", position)

        device = self.view.controller.get_device_at(position)
        name = self.name_var.get();
        ip = self.ip_var.get();
        login = self.login_var.get();
        password = self.password_var.get();
        com = self.com_var.get();
        self.view.controller.update_device_parameters(device,name,ip,login,password,com)
                             
        
        self.setup_window.destroy()
        

    def set_new_values(self):
        pass
##        config = ConfigParser()
##        config.read('serial.ini')
##        config.set('serial_comms', 'port', self.port_var.get())
##        config.set('serial_comms', 'speed', self.speed_var.get())
##        config.set('serial_comms', 'bits', self.bits_var.get())
##        config.set('serial_comms', 'stop', self.stop_var.get())
##        config.set('serial_comms', 'parity', self.parity_var.get())
##        configurations.PORT = self.port_var.get()
##        configurations.SPEED= self.speed_var.get()
##        configurations.BITS = self.bits_var.get()
##        configurations.PARITY = self.parity_var.get()
##        configurations.STOP = self.stop_var.get()
##        with open('serial.ini', 'w') as config_file:
##            config.write(config_file)

    def on_cancel_button_clicked(self):
        self.setup_window.destroy()


    def show_advanced_window(self):
        
        dev_pos = str(self.pos_var.get())
        name = self.name_var.get()
        ip = self.ip_var.get()
        login = self.login_var.get()
        password = self.password_var.get()
        com = self.com_var.get()
        self.appc=device_window_advanced.AdvancedSetupWindow(self.view,self, dev_pos,name,ip,login,password,com)
