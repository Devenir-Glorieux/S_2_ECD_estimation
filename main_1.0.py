from tkinter import *
from tkinter import ttk
import csv
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import math
import os

window = Tk()
window.title ('ECD estimation for well constraction')
window.geometry ('1415x360+30+30')
window.resizable(False, False)
#window.grid_propagate(1)
bg1='gainsboro' 
bg2='rosybrown'
bg3='darkgray' 
GRAVITY = 9.8066

# Создаю фреймы и вкладки
estimation = ttk.Notebook()
estimation.grid()

ecd_frame = Frame(estimation)
ecd_frame.grid()
trip_frame = Frame(estimation)
trip_frame.grid()

up_frame  =  Frame(ecd_frame,  width=1880,  height=  400,  bg=bg1)
up_frame.grid(row=0,  column=0,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

down_frame  =  Frame(ecd_frame,  width=500,  height= 420,  bg=bg2)
down_frame.grid(row=1,  column=0,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

estimation.add(ecd_frame, text='ECD estimation')
estimation.add(trip_frame, text='trip/up&down operations')
#estimation.hide(1)

bit_id_list=[]
casing_id_list=[]
pipe_outer_diameter_list=[]
total_md_list=[]
total_tvd_list=[]
injr_list=[]
mud_density_list=[]
pv_list=[]
yp_list=[]
interval_num_list = []

row_counter = 4
interval_num=1

interval_num_list.append(interval_num)

def row_add():
    global row_counter
    global interval_num

    label_text = str(row_counter-2) + '.'
    Label(up_frame, text=label_text, background=bg1, font='Arial 8 bold').grid(row=row_counter, column=0, padx=0,  pady=0, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Drill Bit Diameter', background=bg1).grid(row=row_counter,  column=1,  padx=0,  pady=0, sticky='w')
    bit_id_entry = ttk.Entry(up_frame, width=10) 
    bit_id_entry.grid(row=row_counter, column=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Pipe Outer Diametr', background=bg1).grid(row=row_counter,  column=3,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')
    pipe_outer_diameter_entry = ttk.Entry(up_frame, width=10) 
    pipe_outer_diameter_entry.grid(row=row_counter, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Total MD', background=bg1).grid(row=row_counter,  column=5,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
    total_md_entry = ttk.Entry(up_frame, width=10) 
    total_md_entry.grid(row=row_counter, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='TVD', background=bg1).grid(row=row_counter,  column=7,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
    total_tvd_entry = ttk.Entry(up_frame, width=10) 
    total_tvd_entry.grid(row=row_counter, column=8, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Flow Rate', background=bg1).grid(row=row_counter,  column=9,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
    injr_entry = ttk.Entry(up_frame, width=10) 
    injr_entry.grid(row=row_counter, column=10, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Mud Density', background=bg1).grid(row=row_counter,  column=11,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
    mud_density_entry = ttk.Entry(up_frame, width=10) 
    mud_density_entry.grid(row=row_counter, column=12, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Plastic Viscosity', background=bg1).grid(row=row_counter,  column=13,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
    pv_entry = ttk.Entry(up_frame, width=10) 
    pv_entry.grid(row=row_counter, column=14, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    label = Label(up_frame, text='Yield Point', background=bg1)
    label.grid(row=row_counter,  column=15,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
    yp_entry = ttk.Entry(up_frame, width=10) 
    yp_entry.grid(row=row_counter, column=16, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    Label(up_frame, text='Casing ID', background=bg1).grid(row=row_counter,  column=17,  padx=0,  pady=0, sticky='w')
    casing_id_entry = ttk.Entry(up_frame, width=10) 
    casing_id_entry.grid(row=row_counter, column=18, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    row_counter += 1
    interval_num +=1

    bit_id_list.append(bit_id_entry)
    pipe_outer_diameter_list.append(pipe_outer_diameter_entry)
    total_md_list.append(total_md_entry)
    total_tvd_list.append(total_tvd_entry)
    injr_list.append(injr_entry)
    mud_density_list.append(mud_density_entry)
    pv_list.append(pv_entry)
    yp_list.append(yp_entry)
    casing_id_list.append(casing_id_entry)

    interval_num_list.append(interval_num)
    window.update_idletasks()
    window.geometry(f'1415x{240+(row_counter * 30)}')
    print(len(bit_id_list))
    return

def calc():
    global interval_num
    global unit
    interval_number = 1 #определяю порядковый номер расчета
    big = []
    bit_id_values=[]
    pipe_outer_diameter_values=[]
    total_md_values=[]
    total_tvd_values=[]
    injr_values=[]
    mud_density_values=[]
    pv_values=[]
    yp_values=[]
    casing_id_values=[]

    def data_get():
        global unit
        
        if unit.get() == 1:                                                 
            for bit_id_entry in bit_id_list:
                bit_id_values.append(float(bit_id_entry.get())/25.4)

            for casing_id_entry in casing_id_list:
                casing_id_values.append(float(casing_id_entry.get())/25.4)    
                
            for pipe_outer_diameter_entry in pipe_outer_diameter_list:
                pipe_outer_diameter_values.append(float(pipe_outer_diameter_entry.get())/25.4)
                
            for total_md_entry in total_md_list:
                total_md_values.append(float(total_md_entry.get())*3.281)

            for total_tvd_entry in total_tvd_list:
                total_tvd_values.append(float(total_tvd_entry.get())*3.281)

            for injr_entry in injr_list:
                injr_values.append(float(injr_entry.get())*15.85032)

            for mud_density_entry in mud_density_list:
                mud_density_values.append(float(mud_density_entry.get())/119.8264273004)

            for pv_entry in pv_list:
                pv_values.append(pv_entry.get())

            for yp_entry in yp_list:
                yp_values.append(yp_entry.get())
        else:
            for bit_id_entry in bit_id_list:
                bit_id_values.append(float(bit_id_entry.get()))

            for casing_id_entry in casing_id_list:
                casing_id_values.append(float(casing_id_entry.get()))     
                
            for pipe_outer_diameter_entry in pipe_outer_diameter_list:
                pipe_outer_diameter_values.append(float(pipe_outer_diameter_entry.get()))
                
            for total_md_entry in total_md_list:
                total_md_values.append(float(total_md_entry.get()))

            for total_tvd_entry in total_tvd_list:
                total_tvd_values.append(float(total_tvd_entry.get()))

            for injr_entry in injr_list:
                injr_values.append(float(injr_entry.get()))

            for mud_density_entry in mud_density_list:
                mud_density_values.append(float(mud_density_entry.get()))

            for pv_entry in pv_list:
                pv_values.append(pv_entry.get())

            for yp_entry in yp_list:
                yp_values.append(yp_entry.get())

         
        return (bit_id_values, pipe_outer_diameter_values, total_md_values, total_tvd_values, injr_values, mud_density_values, pv_values, yp_values, casing_id_values)
    
    bit_id_values, pipe_outer_diameter_values, total_md_values, total_tvd_values, injr_values, mud_density_values, pv_values, yp_values, casing_id_values = data_get()
      
    for i in range(len(bit_id_values)):
        big.append([bit_id_values[i], pipe_outer_diameter_values[i], total_md_values[i], total_tvd_values[i], injr_values[i], mud_density_values[i], pv_values[i], yp_values[i], casing_id_values[i], interval_num_list[i]])
        
    for j in big:
        bit_id_values_a = j[0]
        pipe_outer_diameter_values_a = j[1]
        total_md_values_a = j[2]
        total_tvd_values_a = j[3]
        injr_values_a = j[4]
        mud_density_values_a = j[5]
        pv_values_a = j[6]
        yp_values_a = j[7]
        #casing_id_values_a = j[8] не используется в расчете
        interval_num_list_a = j[9]

        if interval_num != 1: #если интервалов больше, чем один

            if interval_num_list_a == 1: #расчет для первого интервала
                Va_open_hole = (0.408 * float(injr_values_a)) / (math.pow(float(bit_id_values_a), 2) - math.pow(float(pipe_outer_diameter_values_a), 2)) #ft/sec

                Apparent_visc_open_hole = float(pv_values_a)+(5.45*float(yp_values_a)*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))/Va_open_hole) #cP

                Nre_open_hole = (757*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))*Va_open_hole*float(mud_density_values_a))/Apparent_visc_open_hole #Since NRe < 2100, flow is laminar

                print ("total_tvd_values_a=", total_tvd_values_a*0.3048, " ", "total_md_values_a=", " ", total_md_values_a*0.3048)

                if Nre_open_hole <= 2100:
                    Fa_open_hole = 16/Nre_open_hole

                    grad_dP_open_hole = (Fa_open_hole * (math.pow(Va_open_hole,2)) * float(mud_density_values_a))/(25.81*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))) #psi/ft

                    delta_P_open_hole = grad_dP_open_hole * float(total_md_values_a) #psi
                    delta_P = delta_P_open_hole

                    ECD_bottom = float(mud_density_values_a) + delta_P_open_hole / (0.052 * float(total_tvd_values_a))

                    ECD_bottom_metric = float(ECD_bottom) * 119.82642730074

                    if unit == 0:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(total_md_values_a), str(ECD_bottom), str(ECD_bottom), str(delta_P)]
                        table.insert(parent="", index="end", values=value_result)
                    else:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(int(total_md_values_a/3.281)), str(int(ECD_bottom*119.82642730074)), str(int(ECD_bottom*119.82642730074)), str(int(delta_P*0.0689476))]
                        table.insert(parent="", index="end", values=value_result)    
        
                else:
                    Fa_open_hole = 0.0791/(math.pow(Nre_open_hole, 0.25))

                    grad_dP_open_hole = (Fa_open_hole * (math.pow(Va_open_hole,2)) * float(mud_density_values_a))/(25.81*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))) #psi/ft

                    delta_P_open_hole = grad_dP_open_hole * float(total_md_values_a) #psi
                    delta_P = delta_P_open_hole

                    ECD_bottom = float(mud_density_values_a) + delta_P_open_hole / (0.052 * float(total_tvd_values_a))

                    ECD_bottom_metric = float(ECD_bottom) * 119.82642730074

                    if unit == 0:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(total_md_values_a), str(ECD_bottom), str(ECD_bottom), str(delta_P)]
                        table.insert(parent="", index="end", values=value_result)
                    else:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(int(total_md_values_a/3.281)), str(int(ECD_bottom*119.82642730074)), str(int(ECD_bottom*119.82642730074)), str(int(delta_P*0.0689476))]
                        table.insert(parent="", index="end", values=value_result)  

            else:    #расчеты для последующих интервалов
                # print(casing_id_values_pi_list_a)
                total_tvd_values_cs_a = total_tvd_values [interval_number-2]
                lenght_of_interval_a = total_md_values [interval_number-1] - total_md_values [interval_number-2]
                md_casing_a = total_md_values [interval_number-2]
                casing_id_values_pi_a = casing_id_values [interval_number-2]

                Va_casing = (0.408 * float(injr_values_a)) / (math.pow(float(casing_id_values_pi_a), 2) - math.pow(float(pipe_outer_diameter_values_a), 2)) #ft/sec
                Va_open_hole = (0.408 * float(injr_values_a)) / (math.pow(float(bit_id_values_a), 2) - math.pow(float(pipe_outer_diameter_values_a), 2)) #ft/sec

                Apparent_visc_casing = float(pv_values_a)+(5.45*float(yp_values_a)*(float(casing_id_values_pi_a)-float(pipe_outer_diameter_values_a))/Va_casing) #cP
                Apparent_visc_open_hole = float(pv_values_a)+(5.45*float(yp_values_a)*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))/Va_open_hole) #cP

                Nre_casing = (757*(float(casing_id_values_pi_a)-float(pipe_outer_diameter_values_a))*Va_casing*float(mud_density_values_a))/Apparent_visc_casing #Since NRe < 2100, flow is laminar
                Nre_open_hole = (757*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))*Va_open_hole*float(mud_density_values_a))/Apparent_visc_open_hole #Since NRe < 2100, flow is laminar

                print ("casing_id_values_pi_a=", casing_id_values_pi_a*25.4," ", "bit_id_values_a=", bit_id_values_a*25.4, " " , "pipe_outer_diameter_values_a=", pipe_outer_diameter_values_a*25.4, " ","total_tvd_values_cs_a=", total_tvd_values_cs_a*0.3048, " ", "total_tvd_values_a=", total_tvd_values_a*0.3048, " ", "lenght_of_interval_a=", " ", lenght_of_interval_a*0.3048, " ", "md_casing_a=", md_casing_a*0.3048)

                if Nre_open_hole <= 2100:
                    Fa_casing = 16/Nre_casing
                    Fa_open_hole = 16/Nre_open_hole

                    grad_dP_casing = (Fa_casing * (math.pow(Va_casing, 2)) * float(mud_density_values_a))/(25.81*(float(casing_id_values_pi_a)-float(pipe_outer_diameter_values_a))) #psi/ft
                    grad_dP_open_hole = (Fa_open_hole * (math.pow(Va_open_hole, 2)) * float(mud_density_values_a))/(25.81*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))) #psi/ft

                    delta_P_casing = grad_dP_casing * float(md_casing_a) #psi
                    delta_P_open_hole = grad_dP_open_hole * float(lenght_of_interval_a) #psi
                    delta_P = delta_P_casing + delta_P_open_hole
                    print ('delta_P_casing=', delta_P_casing, 'delta_P_open_hole', delta_P_open_hole, 'delta_P', delta_P)

                    ECD_casing_shoe = float(mud_density_values_a) + (delta_P_casing / (0.052 * float(total_tvd_values_cs_a)))
                    #ECD_bottom = float(mud_density_values_a) + (delta_P / (0.052 * float(total_tvd_values_a)))
                    ECD_bottom = ECD_casing_shoe + (delta_P_open_hole / (0.052 * (float(total_tvd_values_a)-float(total_tvd_values_cs_a))))

                    ECD_casing_shoe_metric = float(ECD_casing_shoe) * 119.82642730074
                    ECD_bottom_metric = float(ECD_bottom) * 119.82642730074
                    
                    if unit == 0:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(lenght_of_interval_a), str(ECD_casing_shoe), str(ECD_bottom), str(delta_P)]
                        table.insert(parent="", index="end", values=value_result)
                    else:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(int(lenght_of_interval_a*0.3048)), str(int(ECD_casing_shoe*119.82642730074)), str(int(ECD_bottom*119.82642730074)), str(int(delta_P*0.0689476))]
                        table.insert(parent="", index="end", values=value_result)  

                else:
                    Fa_casing = 0.0791/(math.pow(Nre_casing, 0.25))
                    Fa_open_hole = 0.0791/(math.pow(Nre_open_hole, 0.25))

                    grad_dP_casing = (Fa_casing * (math.pow(Va_casing,2)) * float(mud_density_values_a))/(25.81*(float(casing_id_values_pi_a)-float(pipe_outer_diameter_values_a))) #psi/ft
                    grad_dP_open_hole = (Fa_open_hole * (math.pow(Va_open_hole,2)) * float(mud_density_values_a))/(25.81*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))) #psi/ft

                    delta_P_casing = grad_dP_casing * float(md_casing_a) #psi
                    delta_P_open_hole = grad_dP_open_hole * float(lenght_of_interval_a) #psi
                    delta_P = delta_P_casing + delta_P_open_hole
                    print ('delta_P_casing=', delta_P_casing, 'delta_P_open_hole', delta_P_open_hole, 'delta_P', delta_P)

                    ECD_casing_shoe = float(mud_density_values_a) + (delta_P_casing / (0.052 * float(total_tvd_values_cs_a)))
                    #ECD_bottom = float(mud_density_values_a) + (delta_P / (0.052 * float(total_tvd_values_a)))
                    ECD_bottom = ECD_casing_shoe + (delta_P_open_hole / (0.052 * (float(total_tvd_values_a)-float(total_tvd_values_cs_a))))

                    ECD_casing_shoe_metric = float(ECD_casing_shoe) * 119.82642730074
                    ECD_bottom_metric = float(ECD_bottom) * 119.82642730074

                    if unit == 0:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(ECD_bottom), str(ECD_bottom), str(delta_P)]
                        table.insert(parent="", index="end", values=value_result)
                    else:
                        sections = 'Sections №' + str(interval_number)
                        value_result = [(str(sections)), str(int(lenght_of_interval_a*0.3048)), str(int(ECD_casing_shoe*119.82642730074)), str(int(ECD_bottom*119.82642730074)), str(int(delta_P*0.0689476))]
                        table.insert(parent="", index="end", values=value_result)  

            interval_number += 1 
        else: #если только один интервал для расчета
            
            Va_open_hole = (0.408 * float(injr_values_a)) / (math.pow(float(bit_id_values_a), 2) - math.pow(float(pipe_outer_diameter_values_a), 2)) #ft/sec

            Apparent_visc_open_hole = float(pv_values_a)+(5.45*float(yp_values_a)*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))/Va_open_hole) #cP

            Nre_open_hole = (757*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))*Va_open_hole*float(mud_density_values_a))/Apparent_visc_open_hole #Since NRe < 2100, flow is laminar

            if Nre_open_hole <= 2100:
                Fa_open_hole = 16/Nre_open_hole

                grad_dP_open_hole = (Fa_open_hole * (math.pow(Va_open_hole,2)) * float(mud_density_values_a))/(25.81*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))) #psi/ft

                delta_P_open_hole = grad_dP_open_hole * float(total_md_values_a) #psi
                delta_P = delta_P_open_hole

                ECD_bottom = float(mud_density_values_a) + delta_P_open_hole / (0.052 * float(total_tvd_values_a))

                ECD_bottom_metric = float(ECD_bottom) * 119.82642730074

                if unit == 0:
                    sections = 'Sections №' + str(interval_number)
                    value_result = [(str(sections)), str(total_md_values_a), str(ECD_bottom), str(ECD_bottom), str(delta_P)]
                    table.insert(parent="", index="end", values=value_result)
                else:
                    sections = 'Sections №' + str(interval_number)
                    value_result = [(str(sections)), str(int(total_md_values_a/3.281)), str(int(ECD_bottom*119.82642730074)), str(int(ECD_bottom*119.82642730074)), str(int(delta_P*0.0689476))]
                    table.insert(parent="", index="end", values=value_result)    
    
            else:
                Fa_open_hole = 0.0791/(math.pow(Nre_open_hole, 0.25))

                grad_dP_open_hole = (Fa_open_hole * (math.pow(Va_open_hole,2)) * float(mud_density_values_a))/(25.81*(float(bit_id_values_a)-float(pipe_outer_diameter_values_a))) #psi/ft

                delta_P_open_hole = grad_dP_open_hole * float(total_md_values_a) #psi
                delta_P = delta_P_open_hole

                ECD_bottom = float(mud_density_values_a) + delta_P_open_hole / (0.052 * float(total_tvd_values_a))

                ECD_bottom_metric = float(ECD_bottom) * 119.82642730074

                if unit == 0:
                    sections = 'Sections №' + str(interval_number)
                    value_result = [(str(sections)), str(total_md_values_a), str(ECD_bottom), str(ECD_bottom), str(delta_P)]
                    table.insert(parent="", index="end", values=value_result)
                else:
                    sections = 'Sections №' + str(interval_number)
                    value_result = [(str(sections)), str(int(total_md_values_a/3.281)), str(int(ECD_bottom*119.82642730074)), str(int(ECD_bottom*119.82642730074)), str(int(delta_P*0.0689476))]
                    table.insert(parent="", index="end", values=value_result)           

unit = IntVar(value=1)

def unit_change(value):
    global unit
    unit.set(value)
    if unit.get() == 1:
        unit_1.config(text='mm')
        unit_2.config(text='mm')
        unit_3.config(text='m')
        unit_4.config(text='m')
        unit_5.config(text='l/s')
        unit_6.config(text='kg/m\u00B3')
        unit_7.config(text='mm')

    else:
        unit_1.config(text='in')
        unit_2.config(text='in')
        unit_3.config(text='ft')
        unit_4.config(text='ft')
        unit_5.config(text='gal/m')
        unit_6.config(text='lb/ft\u00B3')
        unit_7.config(text='in')
    return    
  
#Создаю виджеты
Button(up_frame, command=row_add, width=3, text='+', font='Arial 8 bold').grid(row=1,  column=0,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')
Button(up_frame, width=3, text='Calc', font='Arial 8 bold', command=calc).grid(row=1,  column=6,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')
Label(up_frame, text='API', background=bg1, border=0, font='Arial 8 bold').grid(row=1, column=1, sticky='e')
Label(up_frame, text='Metric', background=bg1, border=0, font='Arial 8 bold').grid(row=1, column=3, sticky='w')
measurement_system = Scale(up_frame, orient=HORIZONTAL, from_= 0, to=1, length=50, showvalue=OFF, variable=unit, command=unit_change, troughcolor=bg1, highlightbackground=bg1)
measurement_system.grid(row=1, column=2, padx=1,  pady=0, sticky='e')
Label(up_frame, text='model: ', background=bg1).grid(row=1, column=4)
models = ["Bingham"]
model_type = StringVar(value=models[0])
combobox = ttk.Combobox(up_frame, values=models[0], textvariable=model_type, width=10, state='readonly')
combobox.grid(row=1, column=5)

Label(up_frame, text='cP', background=bg1).grid(row=2, column=14, sticky='s', pady=0)
Label(up_frame, text='lbf/100ft\u00B2', background=bg1).grid(row=2, column=16, sticky='s', pady=0)

unit_1 = Label(up_frame, text='mm', background=bg1)
unit_1.grid(row=2, column=2, sticky='s', pady=0) 
unit_2=Label(up_frame, text='mm', background=bg1)
unit_2.grid(row=2, column=4, sticky='s', pady=0) 
unit_3=Label(up_frame, text='m', background=bg1)
unit_3.grid(row=2, column=6, sticky='s', pady=0)
unit_4=Label(up_frame, text='m', background=bg1)
unit_4.grid(row=2, column=8, sticky='s', pady=0)
unit_5=Label(up_frame, text='l/s', background=bg1)
unit_5.grid(row=2, column=10, sticky='s', pady=0)
unit_6=Label(up_frame, text='kg/m\u00B3', background=bg1)
unit_6.grid(row=2, column=12, sticky='s', pady=0)
unit_7=Label(up_frame, text='mm', background=bg1)
unit_7.grid(row=2, column=18, sticky='s', pady=0)

Label(up_frame, text='1.', background=bg1, font='Arial 8 bold').grid(row=3, column=0, padx=0,  pady=0, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Drill Bit Diameter', background=bg1).grid(row=3,  column=1,  padx=0,  pady=0, sticky='w')
bit_id_entry = ttk.Entry(up_frame, width=10) 
bit_id_entry.grid(row=3, column=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Pipe Outer Diametr', background=bg1).grid(row=3,  column=3,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')
pipe_outer_diameter_entry = ttk.Entry(up_frame, width=10) 
pipe_outer_diameter_entry.grid(row=3, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Total MD', background=bg1).grid(row=3,  column=5,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
total_md_entry = ttk.Entry(up_frame, width=10) 
total_md_entry.grid(row=3, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='TVD', background=bg1).grid(row=3,  column=7,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
total_tvd_entry = ttk.Entry(up_frame, width=10) 
total_tvd_entry.grid(row=3, column=8, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Flow Rate', background=bg1).grid(row=3,  column=9,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
injr_entry = ttk.Entry(up_frame, width=10) 
injr_entry.grid(row=3, column=10, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Mud Density', background=bg1).grid(row=3,  column=11,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
mud_density_entry = ttk.Entry(up_frame, width=10) 
mud_density_entry.grid(row=3, column=12, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Plastic Viscosity', background=bg1).grid(row=3,  column=13,  padx=0,  pady=0, sticky='w'+'e'+'n'+'s')
pv_entry = ttk.Entry(up_frame, width=10) 
pv_entry.grid(row=3, column=14, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

label = Label(up_frame, text='Yield Point', background=bg1)
label.grid(row=3,  column=15,  padx=0,  pady=5, sticky='w'+'e'+'n'+'s')
yp_entry = ttk.Entry(up_frame, width=10) 
yp_entry.grid(row=3, column=16, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

Label(up_frame, text='Casing ID', background=bg1).grid(row=3,  column=17,  padx=0,  pady=0, sticky='w')
casing_id_entry = ttk.Entry(up_frame, width=10) 
casing_id_entry.grid(row=3, column=18, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

bit_id_list.append(bit_id_entry)
casing_id_list.append(casing_id_entry)
pipe_outer_diameter_list.append(pipe_outer_diameter_entry)
total_md_list.append(total_md_entry)
total_tvd_list.append(total_tvd_entry)
injr_list.append(injr_entry)
mud_density_list.append(mud_density_entry)
pv_list.append(pv_entry)
yp_list.append(yp_entry)

columns = ("Sections", "Drilling Interval", "ECD_shoe", "ECD_bottom", "dP_annular")
table = ttk.Treeview(down_frame, show = 'headings', columns=columns) 
table.grid(row=interval_num, column=4)

table.column("Sections", width=200, stretch=YES, anchor=CENTER)
table.column("Drilling Interval", width=300, anchor=CENTER, stretch=YES)
table.column("ECD_shoe", width=300, anchor=CENTER, stretch=YES)
table.column("ECD_bottom", width=300, anchor=CENTER, stretch=YES)
table.column("dP_annular", width=300, anchor=CENTER, stretch=YES)

table.heading("Sections", text='Sections', anchor=CENTER)
table.heading("Drilling Interval", text='Drilling Interval', anchor=CENTER)
table.heading("ECD_shoe", text="ECD_shoe", anchor=CENTER)
table.heading("ECD_bottom", text="ECD_bottom", anchor=CENTER)
table.heading("dP_annular", text="dP_annular", anchor=CENTER)

#------------------------------------------------------------------------------
def calculator():
    os.system("C:/WINDOWS/System32/calc.exe")
    return
def show_about():
    messagebox.showinfo(title="About", message="Version: 1.0\nAuthor: Stanislav Nikulin\nTelegram: @stan_nikulin\nDate: 2023\nLicense: MIT")
#меню
menu_bar = Menu(window)

file_menu = Menu(menu_bar, tearoff=0)
# file_menu.add_command(label="Сохранить", command=save_file)
# file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
# edit_menu.add_command(label="Копировать")
edit_menu.add_command(label="Calculator", command=calculator)

menu_bar.add_cascade(label="Options", menu=edit_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About...", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

window.config(menu=menu_bar)


#------------------------------------------------------------------------------

window.mainloop()

