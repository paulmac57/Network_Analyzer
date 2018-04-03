
from configurations import *
import model
import device
import main_comms

class Controller():
    
    def __init__(self):
        self.init_network_model()

    def create_new_device(self,position,network_device):
        self.model[position] = device.create_device(network_device)
        
        return 


##    def load_router(self):
##           
##        self.model["A1"] = device.create_device("R","white")
##        return 
##
##    def load_switch(self):
##        switch = device.create_device(Switch,"white")
##        #switch = device.Switch("White")
##        return 

##    def update_game_statistics(self,device, device_at_destination, initial_pos, final_pos):
        self.model.update_game_statistics(device, device_at_destination, initial_pos, final_pos)
        return

    def update_device_parameters(self,dev, name,ip,login,password,com,vendor,model,serial_no,os,uptime,type):
        device.update_device_parameters(dev, name,ip,login,password,com,vendor,model,serial_no,os,uptime,type)

    def init_network_model(self):
        self.model = model.Model()
        
        
    def get_all_devices_on_board(self):
        #print (self.model())
        return self.model.items()

    def reset_network_data(self):
        self.model.reset_network_data()

    def reset_to_initial_locations(self):
        self.model.reset_to_initial_locations()

    def get_alphanumeric_position(self, rowcolumntuple):
        return self.model.get_alphanumeric_position(rowcolumntuple)
    
    def get_numeric_notation(self, position):
        return device.get_numeric_notation(position)

    def get_device_at(self, position_of_click):
        return self.model.get_device_at(position_of_click)

    def pre_move_validation(self, start_pos, end_pos):
        return self.model.pre_move_validation(start_pos, end_pos)

    def delete_device(self,position):
        self.model.delete_device_at(position)
        
#    def player_turn(self):
#        return self.model.player_turn

    def moves_available(self, position):
        return self.model.moves_available(position)

    def telnet_main(self,ip,login,password):
        this_device = main_comms.telnet_main(ip,login,password)
        return this_device
    
    def show_version(self,remote_connection,device):
        main_comms.show_version(remote_connection,device)
        return 

    def show_cdp_neighbors(self,remote_connection,device):
        main_comms.show_cdp_neighbors(remote_connection,device)
        return 

    def set_hostname(self,new_name,remote_connection,device):
        main_comms.set_hostname(new_name,remote_connection,device)
        return
    
    def write_pickle(self,device):
        main_comms.write_pickle(device)
        return
