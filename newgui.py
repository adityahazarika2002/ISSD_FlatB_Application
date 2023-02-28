import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import * # type:ignore
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from integrator import trapezoidal_csv
from PIL import ImageTk
import PIL.Image as Image
import customtkinter as ctk
import mplcyberpunk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

PATH = os.path.dirname(os.path.realpath(__file__))


class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("FlatB: Flatband Voltage Calculator")
        self.iconbitmap(r"icon\calculator.ico")
        self.geometry("950x800")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        #configure grid layout
        
        
        self.main_frame = ctk.CTkCanvas(master=self)

        self.main_canvas = ctk.CTkCanvas(master=self.main_frame, bg="#2a2d2e", highlightthickness=0)


        self.main_canvas.grid_columnconfigure(1, weight=1)
        self.main_canvas.grid_rowconfigure(2, weight=1)

        self.sub_frame = ctk.CTkFrame(master=self.main_canvas)

        self.scrollbar = ctk.CTkScrollbar(master=self.main_frame, orientation='vertical', command=self.main_canvas.yview)

        self.sub_frame.bind("<Configure>",
                            lambda e: self.main_canvas.configure(
                            scrollregion=self.main_canvas.bbox("all")))
        
        self.main_canvas.create_window((0, 0), window=self.sub_frame, anchor=CENTER)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_frame.pack(fill="both", expand=True, anchor=NE)
        self.main_canvas.pack(side="left", fill="both", expand=True, anchor=NE)
        self.scrollbar.pack(side="right", fill="y")
        
        #=================FRAME=================

        self.author = ctk.CTkFrame(master= self.sub_frame, corner_radius=10) # type:ignore
        self.author.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.upper = ctk.CTkFrame(master= self.sub_frame,
                                    corner_radius=10) # type:ignore
        self.upper.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.upper.grid_rowconfigure(1, weight = 1)
        self.upper.grid_columnconfigure(1, weight=1) 

        self.lower = ctk.CTkFrame(master=self.sub_frame,
                                    corner_radius=10) # type:ignore
        self.lower.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.lower.grid_columnconfigure(2, weight=1)


        self.name = ctk.CTkLabel(master= self.author, text= "FlatB: Flatband Voltage Calculator",
                                    text_font=("Soegoe UI", 30, "bold"),# type:ignore
                                    text_color="#c8c8c8")
        self.name.grid(row=0, column=0, padx=20, pady=(20, 10)) 

        #=====Upper Frame=====
        logoimage = Image.open(PATH + r"\image\tulogo.png").resize((150, 150)) # type:ignore
        self.logo_image = ImageTk.PhotoImage(logoimage)
        
        self.logo_label = ctk.CTkLabel(master= self.upper, image=self.logo_image, corner_radius=6) # type:ignore
        self.logo_label.grid(row=0, column=0, padx=20, pady=25)

        self.parameters = ctk.CTkFrame(master= self.upper,
                                        width= 180,
                                        corner_radius=6) # type:ignore
        self.parameters.grid(row=1, column=0, padx=(20,13), pady=(10, 20))

        self.information = ctk.CTkFrame(master= self.upper)
        self.information.grid(row=0, column=1, padx=(13, 20), pady=20, rowspan=2)


        #=====Parameters=====

        #configure grid layout

        self.parameters.grid_rowconfigure(0)
        self.parameters.grid_rowconfigure(5)
        self.parameters.grid_rowconfigure(7)
        self.parameters.grid_rowconfigure(11)

        self.label_params = ctk.CTkLabel(master= self.parameters,
                                    text= "PARAMETERS",
                                    text_font=("Segoe UI", 16, "bold")) # type:ignore
        self.label_params.grid(row=1, column=0, padx=10, pady=10)

        self.tox_entry = ctk.CTkEntry(master= self.parameters,
                                    width= 120,
                                    placeholder_text= "T_ox (in μm)",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.tox_entry.grid(row=2, column=0, padx=10, pady=10)

        self.phi_m = ctk.CTkEntry(master= self.parameters,
                                    width= 120,
                                    placeholder_text= "Phi_m (in eV)",
                                    text_font=("Segoe UI", 10,)) # type:ignore
        self.phi_m.grid(row=3, column=0, padx=10, pady=10)

        self.epselonx_entry = ctk.CTkEntry(master= self.parameters,
                                    width= 120,
                                    placeholder_text= "Epsilon_x (in F/cm)",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.epselonx_entry.grid(row=4, column=0, padx=10, pady=10)

        self.label_option = ctk.CTkLabel(master= self.parameters, text= "Select Option:",
                                        text_font=("Segoe UI", 10, "bold")) # type:ignore
        self.label_option.grid(row=8, column=0, padx=20, pady=0)

        self.option = ctk.CTkOptionMenu(master= self.parameters,
                                        values= ["Phi_s (in eV)", "Na (in cm^-3)"],
                                        text_font=("Segoe UI", 10, "bold")) # type:ignore
        self.option.grid(row=9, column=0, padx=20, pady=10)

        self.option_entry = ctk.CTkEntry(master= self.parameters,
                                    width= 120,
                                    placeholder_text= "Enter Value",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.option_entry.grid(row=10, column=0, padx=10, pady=5)


        self.parametererror_label = ctk.CTkLabel(master= self.parameters,
                                    text= " ",
                                    text_font=("Segoe UI", 8), # type:ignore
                                    text_color="#FF5260") 
        self.parametererror_label.grid(row=11, column=0, padx=10, pady=0)
        self.parametererror_label.configure(text=" ")
        

        #=====information=====

        #configure grid layout

        self.information.grid_rowconfigure(1, weight=1)

        image = Image.open(PATH + r"\image\reference.jpg").resize((700, 500)) # type:ignore
        self.bg_image = ImageTk.PhotoImage(image)
        
        self.img_info = ctk.CTkLabel(master= self.information, image=self.bg_image, corner_radius=6) # type:ignore
        self.img_info.grid(row=0, column=0, padx=20, pady=25)


        #=====Divide Lower Frame=====

        self.radio_var = tk.IntVar(value=2)

        self.csv_input = ctk.CTkFrame(master= self.lower,
                                    width= 280,
                                    corner_radius=6) # type:ignore
        self.csv_input.grid(row=0, column=0, padx=(20, 10), pady=(10, 20))


        self.function = ctk.CTkFrame(master= self.lower,
                                    corner_radius=6) # type:ignore
        self.function.grid(row=0, column=1, padx=(10, 10), pady=(10, 20))

        self.calculate = ctk.CTkFrame(master= self.lower,
                                    corner_radius=6) # type:ignore
        self.calculate.grid(row=0, column=2, padx=(10, 20), pady=(10, 20))


        #=====CSV Input=====

        #configure grid layout
        
        self.radio_button1 = ctk.CTkRadioButton(master= self.csv_input,
                                            text= "Use CSV Input      ",
                                            text_font=("Segoe UI", 10, "bold"), # type:ignore
                                            variable= self.radio_var,
                                            value= 0)
        self.radio_button1.grid(row=0, column=0, padx=20, pady=20)

        self.upload_button = ctk.CTkButton(master=self.csv_input,
                                            text="Upload CSV",
                                            text_font=("Segoe UI", 10, "bold"), # type:ignore
                                            command= self.browse_copyFiles)
        self.upload_button.grid(row=1, column=0, padx=20, pady=0)

        self.csvinfo_label = ctk.CTkLabel(master= self.csv_input,
                                                text= "[Tox (cm), ρ(x) (C*cm^-3)]",
                                                text_font=("Segoe UI", 8), # type:ignore
                                                text_color="grey") 
        self.csvinfo_label.grid(row=2, column=0, padx=10, pady=0)

        self.csverror_label = ctk.CTkLabel(master= self.csv_input,
                                                text= " ",
                                                text_font=("Segoe UI", 8), # type:ignore
                                                text_color="#FF5260") 
        self.csverror_label.grid(row=3, column=0, padx=10, pady=0)
        self.csverror_label.configure(text=" ")




        #=====Function=====
        
        #configure grid layout

        self.radio_button2 = ctk.CTkRadioButton(master= self.function,
                                            text= "Use Function",
                                            text_font=("Segoe UI", 10, "bold"), # type:ignore
                                            variable= self.radio_var,
                                            value= 1)
        self.radio_button2.grid(row=0, column=0, padx=(20, 10), pady=(20,10))

        self.function_entry = ctk.CTkEntry(master= self.function,
                                    width= 120,
                                    placeholder_text= "Function",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.function_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        self.lower_limit = ctk.CTkEntry(master= self.function,
                                    width= 130,
                                    placeholder_text= "Lower Limit (in μm)",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.lower_limit.grid(row=0, column=1, padx=10, pady=(20, 10))

        self.upper_limit = ctk.CTkEntry(master= self.function,
                                    width= 130,
                                    placeholder_text= "Upper Limit (in μm)",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.upper_limit.grid(row=1, column=1, padx=10, pady=(0, 10))

        self.pts_num = ctk.CTkEntry(master= self.function,
                                    width= 130,
                                    placeholder_text= "Number of Points",
                                    text_font=("Segoe UI", 10)) # type:ignore
        self.pts_num.grid(row=0, column=2, padx=(10, 20), pady=(20, 10))

        self.function_label = ctk.CTkLabel(master= self.function,
                                            text= " ",
                                            text_font=("Segoe UI", 8), # type:ignore
                                            text_color="#FF5260") 
        self.function_label.grid(row=1, column=2, padx=10, pady=0)
        self.function_label.configure(text=" ")

        self.info_button = ctk.CTkButton(master=self.function,
                                            width=5,
                                            text="info",
                                            text_font=("Segoe UI", 10, "bold"), # type:ignore
                                            command= self.info_window)
        self.info_button.grid(row=2, column=1, padx=20, pady=(10, 10), sticky="nswe")


        #=====Calculate=====

        #configure grid layout

        self.calculate_button = ctk.CTkButton(master=self.calculate,
                                            width=40,
                                            height=50,
                                            text="Calculate",
                                            text_font=("Segoe UI", 10, "bold"), # type:ignore
                                            command= self.error,
                                            fg_color="Green")
        self.calculate_button.grid(row=0, column=0, padx=40, pady=40)


        #=====Lowest Frame=====
        
    #=================Event Handler=================
    
    def button_event(self):
        print("Button Clicked")

    def info_window(self):

        window = ctk.CTkToplevel(self)
        window.title("How to Input Data?")
        window.iconbitmap("icon/graph.ico")
        window.minsize(250, 150)

        self.info_label = ctk.CTkLabel(master= window,
                                            text= '''1. The function should be in the form of "x".\n2. The function should be input as a python expression (Numpy as np can be used).    \na. Example: The input for function y = sin(x) would look like {np.sin(x)}.\nb. Example: The input for function y = x^2 would look like {x**2}.\nc. Example: The input for function y = e^-(x^2 + 2x + 1) would look like {np.exp(-(x**2 + 2*x + 1))}.''',

                                            text_font=("Segoe UI", 10)) # type:ignore
        self.info_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.okay_button = ctk.CTkButton(master=window,
                                            width=10,
                                            text="Okay!",
                                            text_font=("Segoe UI", 10, "bold"), # type:ignore
                                            command= window.destroy)
        self.okay_button.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")



    def browse_copyFiles(self):
        global source
        source = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("csv files", "*.csv*"), ("all files", "*.*")))
        self.csverror_label.configure(text_color="#A5FF9F", text="File Uploaded")

    def phi_dipole(self):
        if self.option.get() == "Phi_s (in eV)":
            phi_di = float(self.option_entry.get())
        else: #self.option.get() == "Na (in cm^-3)"
            phi_di = 4.05 + (1.12/2) + 0.026*(np.log(float(self.option_entry.get())/np.power(10, 10)))
        return phi_di

    def input_function(self, x):
        y = x*eval(self.function_entry.get())
        return y

    def trapezoidal_fun(self, a, b, n):
        h = (b - a) / n
        sum = 0.5 * (self.input_function(a) + self.input_function(b))
        for i in range(1, n):
            sum += 2*self.input_function(a + i * h)
        return sum * h/2

    def voltage_output(self):
        self.eps_knot = 8.854*(10**-14)

        if self.radio_var.get() == 0:
            volts = float(self.phi_m.get()) - float(self.phi_dipole()) - ((10**-4)*float(self.tox_entry.get()))*(1/(self.eps_knot*float(self.epselonx_entry.get())))*trapezoidal_csv(source)
        else:
            volts = float(self.phi_m.get()) - float(self.phi_dipole()) - ((10**-4)*float(self.tox_entry.get()))*(1/(self.eps_knot*float(self.epselonx_entry.get())))*self.trapezoidal_fun((10**-4)*float(self.lower_limit.get()), (10**-4)*float(self.upper_limit.get()), int(self.pts_num.get()))


        return volts

    def graph_plot(self):
        if self.radio_var.get() == 0:

            data_csv = open(f'{source}')
            array = np.loadtxt(data_csv, delimiter=',')

            arrx = np.zeros(len(array))
            arry = np.zeros(len(array))
            for i in range(len(array)):
                arrx[i] = array[i][0]
                arry[i] = array[i][1]
            
            plt.style.use('cyberpunk')
            
            fig0 = plt.figure(figsize=(8, 5))
            plt.plot(arrx, arry, label='Experimental Data')
            plot_graph1 = FigureCanvasTkAgg(fig0, self.output_frame)
            plot_graph1.draw()
            plot_graph1.get_tk_widget().pack(expand=TRUE, fill=BOTH)

            self.output_label.configure(text= f"The Flatband Volatage is: {self.voltage_output()}")


        elif self.radio_var.get() == 1:
            
            plt.style.use('cyberpunk')
            
            x = np.linspace(float(self.lower_limit.get()), float(self.upper_limit.get()), int(self.pts_num.get()))
            fig1 = plt.figure(figsize=(8, 5))
            plt.plot(x, self.input_function(x), label='Input Function')
            plot_graph = FigureCanvasTkAgg(fig1, self.output_frame)
            plot_graph.draw()
            plot_graph.get_tk_widget().pack(expand=TRUE, fill=BOTH)

            self.output_label.configure(text= f"The Flatband Volatage is: {self.voltage_output()}")
            

    def output(self):
        self.voltage_output()

        window = ctk.CTkToplevel(self)
        window.title("Output")
        window.iconbitmap("icon/graph.ico")
        window.minsize(450, 350)

        self.output_frame = ctk.CTkFrame(master= window,
                                    corner_radius=6) # type:ignore
        self.output_frame.pack(expand=TRUE, fill=BOTH, padx=20, pady=20)

        self.output_label = ctk.CTkLabel(master= window,
                                        text= f"Flatband Voltage is: {self.voltage_output()}",
                                    text_font=("Segoe UI", 10, "bold")) # type:ignore
        self.output_label.pack(expand=TRUE, fill=BOTH, padx=10, pady=10)

        self.graph_plot()

    
    def error(self):
        param = "invalid literal for int() with base 10: ''"
        func_param = "could not convert string to float: ''"
        self.parametererror_label.configure(text=" ")
        self.csverror_label.configure(text=" ")
        self.function_label.configure(text=" ")
        #self.output()
        try:
            self.output()
            self.parametererror_label.configure(text=" ")
            self.csverror_label.configure(text=" ")
            self.function_label.configure(text=" ")
        except NameError:
            if self.radio_var.get() == 1:
                self.function_label.configure(text="Invalid Function")
            else:
                self.csverror_label.configure(text="CSV not found", text_color="#FF5260")
        except TypeError:
            self.function_label.configure(text="Invalid Function")
        except SyntaxError:         
            self.function_label.configure(text="Invalid Function")   
        except ValueError as e:
            error_statement = str(e)
            if error_statement == param:
                self.function_label.configure(text="Invalid Parameters")
            elif error_statement == func_param:
                self.parametererror_label.configure(text="Invalid Parameters")
        except FileNotFoundError:
            self.csverror_label.configure(text="CSV not found", text_color="#FF5260")

    def on_closing(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()