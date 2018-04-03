import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.colorchooser import *
from configparser import ConfigParser
import configurations
import serialcomms
import miniterm


class SerialCommsWindow():

    def __init__(self, view):
        
        self.port_var = StringVar()
        self.speed_var = StringVar()
        self.bits_var = StringVar()
        self.stop_var = StringVar()
        self.parity_var = StringVar()
        
        self.parent = view.parent
        self.serial_comms_preference()
        self.view = view
        self.create_serial_comms_window()

    def serial_comms_preference(self):
        
        
        #self.port_var.set(configurations.PORT)
        #self.speed_var.set(configurations.SPEED)
        #self.bits_var.set(configurations.BITS)
        #self.stop_var.set(configurations.STOP)
        #self.parity_var.set(configurations.PARITY)
        pass
       
    def create_serial_comms_window(self):
        self.serial_window = Toplevel(self.parent)
        self.serial_window.geometry('300x200')
        self.serial_window.title("Serial Comms Paramters")
        self.create_serial_list()
        self.serial_window.transient(self.parent)

    def create_serial_list(self):

        comlist = ("com1","com2","com3","com4")
        speedlist =("1200","2400","4800","9600","19200","38400")
        
        bitslist =("7","8")
        stoplist = ("0","1","2")
        paritylist = ("none","odd","even")
        Label(self.serial_window, text='Com Port').grid(row=0, column=0, sticky=W, padx=5, pady=5)
        
        
        Spinbox(self.serial_window, values=comlist, textvariable=self.port_var).grid(row=0,column=1, columnspan=2, sticky=E, padx=5, pady=5)
        self.port_var.set(configurations.PORT)
        Label(self.serial_window, text='Speed').grid(row=1, column=0, sticky=W, padx=5, pady=5)
        
        Spinbox(self.serial_window, values=speedlist, textvariable=self.speed_var).grid(row=1,column=1, columnspan=2, sticky=E, padx=5, pady=5)
        self.speed_var.set(configurations.SPEED)
        Label(self.serial_window, text='Data Bits').grid(row=2, column=0, sticky=W, padx=5, pady=5)
        
        Spinbox(self.serial_window, values = bitslist, textvariable=self.bits_var).grid(row=2,column=1, columnspan=2, sticky=E, padx=5, pady=5)
        self.bits_var.set(configurations.BITS)
        Label(self.serial_window, text='Stop Bits').grid(row=3, column=0, sticky=W, padx=5, pady=5)
        
        Spinbox(self.serial_window, values= stoplist, textvariable=self.stop_var).grid(row=3,column=1, columnspan=2, sticky=E, padx=5, pady=5)
        self.stop_var.set(configurations.STOP)
        Label(self.serial_window, text='Parity').grid(row=4, column=0, sticky=W, padx=5, pady=5)
        
        Spinbox(self.serial_window, values = paritylist, textvariable=self.parity_var).grid(row=4,column=1, columnspan=2, sticky=E, padx=5, pady=5)
        self.parity_var.set(configurations.PARITY)
        
        Button(self.serial_window, text="Save", command=self.on_save_button_clicked).grid(
            row=1, column=3, sticky=W, padx=5, pady=5)
        Button(self.serial_window, text="Cancel", command=self.on_cancel_button_clicked).grid(
            row=3, column=3, sticky=E, padx=5, pady=5)
        
        Button(self.serial_window, text="Initial Config", command=self.on_configure_button_clicked).grid(
            row=5, column=3, sticky=E, padx=5, pady=5)
        
    def on_configure_button_clicked(self):
        serialcomms.connect(self.port_var.get(),self.speed_var.get(),self.bits_var.get(),self.stop_var.get(),self.parity_var.get())
        #miniterm.Miniterm(self,self.port_var.get(),self.speed_var.get())
        
        

    def set_new_values(self):
        config = ConfigParser()
        config.read('serial.ini')
        config.set('serial_comms', 'port', self.port_var.get())
        config.set('serial_comms', 'speed', self.speed_var.get())
        config.set('serial_comms', 'bits', self.bits_var.get())
        config.set('serial_comms', 'stop', self.stop_var.get())
        config.set('serial_comms', 'parity', self.parity_var.get())
        configurations.PORT = self.port_var.get()
        configurations.SPEED= self.speed_var.get()
        configurations.BITS = self.bits_var.get()
        configurations.PARITY = self.parity_var.get()
        configurations.STOP = self.stop_var.get()
        with open('serial.ini', 'w') as config_file:
            config.write(config_file)

    def on_cancel_button_clicked(self):
        self.serial_window.destroy()

    def on_save_button_clicked(self):
        self.set_new_values()
        self.serial_window.destroy()

