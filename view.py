################  THIS IS VIEW
################
##################
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
import controller
from configurations import *
import preferences_window
import serial_comms_window
#import device_initial_setup_window
import device_window_advanced
import exceptions




class View():
    selected_device_position = None
    all_squares_to_be_highlighted = []
    images = {}
    board_color_1 = BOARD_COLOR_1
    board_color_2 = BOARD_COLOR_2
    highlight_color = HIGHLIGHT_COLOR
    
    # Functioms   
    
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.create_app_window()
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.start_new_network()

    def start_new_network(self):
        self.controller.reset_network_data()
        self.controller.reset_to_initial_locations()

        # router=self.controller.load_router()
        # self.draw_single_device("B3",router)





        
        self.draw_all_devices()
        self.info_label.config(text="   White to Start the Game  ")    

##################################################PICLE STUFF FROM 3.12
    def load_project(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Explosion Beat File', '*.ebt')], title='Load Project')
        if not file_path:
            return
        pickled_file_object = open(file_path, "rb")
        try:
            self.all_patterns = pickle.load(pickled_file_object)
        except EOFError:
            messagebox.showerror("Error",
                                 "Explosion Beat file seems corrupted or invalid !")
        pickled_file_object.close()
        try:
            self.reconstruct_first_pattern()
            self.root.title(os.path.basename(file_path) + PROGRAM_NAME)
        except:
            messagebox.showerror("Error",
                                 "An unexpected error occurred trying to process the beat file")

    def save_project(self):
        saveas_file_name = filedialog.asksaveasfilename(
            filetypes=[('Explosion Beat File', '*.ebt')], title="Save project as...")
        if saveas_file_name is None:
            return
        pickle.dump(self.all_patterns, open(saveas_file_name, "wb"))
        self.root.title(os.path.basename(saveas_file_name) + PROGRAM_NAME)    
##################################################################################
    def reload_colors(self, color_1, color_2, highlight_color):
        self.board_color_1 = color_1
        self.board_color_2 = color_2
        self.highlight_color = highlight_color
        self.draw_board()
        self.draw_all_devices()

    def on_serial_menu_clicked(self):
        self.show_serial_comms_window()

    def on_exit_clicked(self):
        self.parent.destroy()
        
            

    def show_serial_comms_window(self):
        serial_comms_window.SerialCommsWindow(self)    

    def on_preference_menu_clicked(self):
        self.show_preferences_window()

    def show_preferences_window(self):
        preferences_window.PreferencesWindow(self)    

    def create_app_window(self):
        self.create_top_menu()
        self.create_icon_bar()
        self.create_left_frame()
        self.create_canvas()
        self.draw_board()
        self.create_bottom_frame()

    def create_top_menu(self):
        self.menu_bar = Menu(self.parent)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_config_menu()
        self.create_about_menu()

    
         

##    def create_edit_menu(self):
##        self.edit_menu = Menu(self.menu_bar, tearoff=0)
##        self.edit_menu.add_command(
##            label="Preferences", command=self.on_preference_menu_clicked)
##        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
##        self.parent.config(menu=self.menu_bar)
    

           
    def create_icon_bar(self):
        def new_file(event=None):
                
            self.title("Untitled")
            global file_name
            file_name = None
            content_text.delete(1.0, END)
            on_content_changed()
        self.shortcut_bar = Frame(self.parent,  height=25)
        def open_file(event=None):
            input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                                 filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if input_file_name:
                global file_name
                file_name = input_file_name
                root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
                content_text.delete(1.0, END)
                with open(file_name) as _file:
                    content_text.insert(1.0, _file.read())
            on_content_changed()

        def save(event=None):
            global file_name
            if not file_name:
                save_as()
            else:
                write_to_file(file_name)
            return "break"

        def cut():
            content_text.event_generate("<<Cut>>")
            on_content_changed()
            return "break"


        def copy():
            content_text.event_generate("<<Copy>>")
            return "break"


        def paste():
            content_text.event_generate("<<Paste>>")
            on_content_changed()
            return "break"


        def undo():
            content_text.event_generate("<<Undo>>")
            on_content_changed()
            return "break"


        def redo(event=None):
            content_text.event_generate("<<Redo>>")
            on_content_changed()
            return 'break'


        def find_text(event=None):
            search_toplevel = Toplevel(self)
            search_toplevel.title('Find Text')
            search_toplevel.transient(self)
            search_toplevel.resizable(False, False)
            Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
            search_entry_widget = Entry(
                search_toplevel, width=25)
            search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
            search_entry_widget.focus_set()
            ignore_case_value = IntVar()
            Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(
                row=1, column=1, sticky='e', padx=2, pady=2)
            Button(search_toplevel, text="Find All", underline=0,
                   command=lambda: search_output(
                       search_entry_widget.get(), ignore_case_value.get(),
                       content_text, search_toplevel, search_entry_widget)
                   ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

            def close_search_window():
                content_text.tag_remove('match', '1.0', END)
                search_toplevel.destroy()
            search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
            return "break"

        self.new_file_icon = PhotoImage(file='icons/new_file.gif')
        self.open_file_icon = PhotoImage(file='icons/open_file.gif')
        self.save_file_icon = PhotoImage(file='icons/save.gif')
        self.cut_icon = PhotoImage(file='icons/cut.gif')
        self.copy_icon = PhotoImage(file='icons/copy.gif')
        self.paste_icon = PhotoImage(file='icons/paste.gif')
        self.undo_icon = PhotoImage(file='icons/undo.gif')
        self.redo_icon = PhotoImage(file='icons/redo.gif')

        # adding shortcut icons
        self.icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
         'undo', 'redo', 'find_text')
        for self.i, self.icon in enumerate(self.icons):
            self.tool_bar_icon = PhotoImage(file='icons/{}.gif'.format(self.icon))
        
            #print(self.icon)
            self.cmd = eval(self.icon)
            
            self.tool_bar = Button(self.shortcut_bar, image=self.tool_bar_icon,command=self.cmd )
            self.tool_bar.image = self.tool_bar_icon
            self.tool_bar.pack(side='left')
        self.shortcut_bar.pack(expand='no', fill='x')   

    def create_bottom_frame(self):
        self.bottom_frame = Frame(self.parent, height=64)
        self.info_label = Label(
            self.bottom_frame, text="   White to Start the Game  ", fg=BOARD_COLOR_2)
        self.info_label.pack(side=TOP, padx=8, pady=5)
        self.bottom_frame.pack(fill="x", side="bottom")

    def create_left_frame(self):
        
        self.left_frame = Frame(self.parent, bd=2, relief=GROOVE)
        #self.info_label = Label(self.left_frame, text="   whatever  ", fg=BOARD_COLOR_2)
        #self.info_label.pack(side=LEFT, padx=8, pady=5)
        self.left_frame.pack(side=LEFT, fill="y")
        self.router_image = PhotoImage(file='images/router_button.png')
        self.switch_image = PhotoImage(file='images/switch_button.png')
        

        self.router_b_button = Button(self.left_frame, image=self.router_image,  command=self.router_button_pressed)

        self.switch_b_button = Button(self.left_frame, image=self.switch_image,  command=self.switch_button_pressed)
    
        self.router_b_button.pack()
        self.switch_b_button.pack()
        self.left_frame.pack()


    def router_button_pressed(self):
        
            #self.controller.pre_move_validation("Z1", "A1")need to check to make sure A1 is free(needs some work)
            self.controller.create_new_device("A1","R")
            self.draw_all_devices()
        
    def switch_button_pressed(self):
        
        
            #self.controller.pre_move_validation("Z1", "A1")need to check to make sure A1 is free(needs some work)
            self.controller.create_new_device("A2","S")
            self.draw_all_devices()


    def show_setup_window(self, device_position):
        dev_pos = device_position
        device_window_advanced.AdvancedSetupWindow(self, dev_pos)
        
        
                
    def on_about_menu_clicked(self):
        messagebox.showinfo("Paul McCherry's",
                            "Network Configurator Nessa BSC Hons\n Development 2017")
    def on_sshtelnet_menu_clicked(self):
        pass

    
        

    def on_new_game_menu_clicked(self):
        self.start_new_game()

   
    def create_file_menu(self):
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(
            label="New Config", command=self.on_new_game_menu_clicked)
        self.file_menu.add_command(
            label="Discover Network", command=self.on_discover_network_clicked)
        
        self.file_menu.add_command(
            label="Exit App", command=self.on_exit_clicked)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.parent.config(menu=self.menu_bar)

    def create_edit_menu(self):
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(
            label="Preferences", command=self.on_preference_menu_clicked)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.parent.config(menu=self.menu_bar)

    def create_config_menu(self):
        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(
            label="Serial Comms", command=self.on_serial_menu_clicked)
        self.config_menu.add_command(
            label="Telnet/SSH Comms", command=self.on_sshtelnet_menu_clicked)
        self.menu_bar.add_cascade(label="Config", menu=self.config_menu)
        
        self.parent.config(menu=self.menu_bar)    

    def create_about_menu(self):
        
        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(
            label="About", command=self.on_about_menu_clicked)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.parent.config(menu=self.menu_bar)

    def create_canvas(self):
        
        canvas_width = NUMBER_OF_COLUMNS * DIMENSION_OF_EACH_SQUARE
        canvas_height = NUMBER_OF_ROWS * DIMENSION_OF_EACH_SQUARE
        self.canvas = Canvas(
           self.parent, borderwidth=0, background="#ffffff")
        self.canvas_frame = Frame(self.canvas, bd=2, relief=SUNKEN)              
        canvas_scrollbar = Scrollbar(self.parent, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=canvas_scrollbar.set)
        canvas_scrollbar.pack(side="right", fill="y")
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=2,)
        self.canvas.create_window((NUMBER_OF_ROWS,NUMBER_OF_COLUMNS), window=self.canvas_frame, anchor="nw", 
                                  tags="self.canvas_frame")
        

        self.canvas_frame.pack()
        
    def draw_board(self):
        current_color = BOARD_COLOR_2
        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
                if(self.all_squares_to_be_highlighted and (row, col) in self.all_squares_to_be_highlighted):
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,  fill=HIGHLIGHT_COLOR)
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,  fill=current_color)
                current_color = self.get_alternate_color (current_color)
                
        
        ########PRACTICE DRAWINg LINES
               
        adf=self.controller.get_numeric_notation("B1")
        #print("AAAAAAAAAAAAAAAAA")
        #print(type(adf))
        #print(adf[0],adf[1])
        self.canvas.create_line(224,192,288,192, tags="line", fill="red")        
        self.canvas.create_line(608,192,672,192, tags="line", fill="red")
        self.canvas.create_line(352,192,544,192, tags="line", fill="blue", width=4.0)

    def get_alternate_color(self, current_color):
        if current_color == self.board_color_2:
            next_color = self.board_color_1
        else:
            next_color = self.board_color_2
        return next_color

    def on_square_clicked(self, event):
        clicked_row, clicked_column = self.get_clicked_row_column(event)
        position_of_click = self.controller.get_alphanumeric_position((clicked_row, clicked_column))
        print("****************************Position of Click is (%s)and selected device position is (%s) " % (position_of_click,self.selected_device_position))
        if self.selected_device_position: # on second click if a device has been clicked
            # if position of second click is same as first open setup window
            if position_of_click == self.selected_device_position:   
                self.show_setup_window(self.selected_device_position)
                self.selected_device_position = None
               
            else:
             # if position of second click is an empty square then move the device    
                self.shift(self.selected_device_position, position_of_click)
                self.selected_device_position = None
        else:    
            self.selected_device_position = position_of_click    
        #self.update_highlight_list(position_of_click)
        
        self.draw_board()
        self.draw_all_devices()
          
    def shift(self, start_pos, end_pos):
        selected_device = self.controller.get_device_at(start_pos)
        if selected_device: 
            device_at_destination = self.controller.get_device_at(end_pos)
            if not device_at_destination :
                try:
                    self.controller.pre_move_validation(start_pos, end_pos)
                except exceptions.NetConfError as error:
                    self.info_label["text"] = error.__class__.__name__
            else:
                self.update_label(selected_device, start_pos, end_pos)

    

##    def update_highlight_list(self, position):
##        self.all_squares_to_be_highlighted = None
##        try:
##            piece = self.controller.get_piece_at(position)
##        except:
##            piece = None
##        if piece and (piece.color == self.controller.player_turn()):
##            self.selected_piece_position = position
##            self.all_squares_to_be_highlighted = list(map(
##                self.controller.get_numeric_notation,
##                self.controller.get_piece_at (position).moves_available(position)))                
##
    def get_clicked_row_column(self, event):
        col_size = row_size = DIMENSION_OF_EACH_SQUARE
        clicked_column = event.x // col_size
        clicked_row = (event.y // row_size)
        return (clicked_row, clicked_column)

    def get_x_y_coordinate(self, row, col):
        x = (col * DIMENSION_OF_EACH_SQUARE)
        y = (row * DIMENSION_OF_EACH_SQUARE)
        return (x, y)

    def calculate_device_coordinate(self, row, col):
        x0 = (col * DIMENSION_OF_EACH_SQUARE) + \
            int(DIMENSION_OF_EACH_SQUARE / 2)
        y0 = ((row) * DIMENSION_OF_EACH_SQUARE) + \
            int(DIMENSION_OF_EACH_SQUARE / 2)
        return (x0, y0)

    def draw_single_device(self, position, device):
        x, y = self.controller.get_numeric_notation(position)
        
        if device:
            #filename = "images/{}_{}.png".format(device.name.lower(), device.color)
            
            filename = "images/{}.png".format(device.name.lower())
            if filename not in self.images:
                self.images[filename] = PhotoImage(file=filename)
            x0, y0 = self.calculate_device_coordinate(x, y)
            self.canvas.create_image(x0, y0, image=self.images[
                                     filename], tags=("occupied"), anchor="c")
    def draw_all_devices(self):
        self.canvas.delete("occupied")
        print("items follow")
        self.controller.get_all_devices_on_board()
        for position, device in self.controller.get_all_devices_on_board():
            print ("position is (%s) device is (%s) " % (position,device))
            self.draw_single_device(position, device)

    def update_label(self, piece, start_pos, end_pos):
        turn = ('white')
        self.info_label["text"] = '' + piece.color.capitalize() + "  :  " + \
            start_pos + end_pos + '    ' + turn.capitalize() + '\'s turn'

    def on_discover_network_clicked(self):
        messagebox.showinfo(title="Network Discovery", message="Discover Network")      
        self.controller.show_cdp_neighbors()
    
def main(controller):
    root = Tk()
    w = 1276 # width for the Tk root
    h = 400 # height for the Tk root
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window and places it in middle
    # not needed
    #x = (ws/2) - (w/2)
    #y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed at top left for this app
    root.geometry('%dx%d+%d+%d' % (w, h, 0, -1))
    #Label(root, text='Network Configurator',bg="black").pack()
    root.title("Network Configurator")
    root.resizable(False,False)
    #root.overrideredirect(1)
    View(root, controller)
    
    
    root.mainloop()


##    no_window_decoration = Toplevel(root, bg='black')
##Label(no_window_decoration, text='I am a top-level with no window manager\n I cannot be resized or moved',
##      bg='black', fg='white').pack()
##no_window_decoration.overrideredirect(1)


def init_new_app():
    app_controller = controller.Controller()
    main(app_controller)

if __name__ == "__main__":
    init_new_app()
