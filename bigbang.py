from tkinter import *
from psutil import virtual_memory, cpu_percent,disk_partitions,disk_usage
import wmi

window=Tk()
window.geometry("900x600")
window.title("CPU - RAM Kullanımı")

def get_cpu_usage():
    c = wmi.WMI()
    cpu_info = c.Win32_PerfFormattedData_PerfOS_Processor()[0]
    idle_percentage = float(cpu_info.PercentIdleTime)
    return 100.0 - idle_percentage

def show_cpu_info():
    cpu_percentage = get_cpu_usage()
    cpu_label.config(text='{} %'.format(cpu_percentage))
    cpu_label.after(200, show_cpu_info)
def consevor_bytes_to_gb(byte):
    one_gigabyte=1073741824
    giga = byte/one_gigabyte
    giga="{0:.1f}".format(giga)
    return giga

def show_ram_info():
    ram_usage = virtual_memory()
    ram_usage=dict(ram_usage._asdict())
    print(ram_usage)
    for key in ram_usage:
        if key!= 'percent':
            ram_usage[key]=consevor_bytes_to_gb(ram_usage[key])
    ram_label.config(text='{} GB / {} GB ({} %)'.format(ram_usage["used"], ram_usage["total"], ram_usage["percent"]))
    ram_label.after(200,show_ram_info)

title_program=Label(window,text="PC Performans Kullanım",font="arial 40 bold", fg="#14747F")
title_program.place(x=110, y=20)

cpu_title_label = Label(window, text="CPU Kullanımı: ", font="arial 24 bold", fg="#FA5125")
cpu_title_label.place(x=20,y=155)

cpu_label=Label(window, bg="#071C1E", fg='#FA5125', font="Arial 24 bold", width=20)
cpu_label.place(x=270,y=150)

ram_title_label=Label(window, text="RAM Kullanımı: ", font="arial 24 bold", fg="#FA5125")
ram_title_label.place(x=20,y=255)

ram_label=Label(window, bg="#071C1E", fg='#FA5125', font="Arial 24 bold", width=20)
ram_label.place(x=270,y=255)

if __name__=='__main__':
    show_cpu_info()
    show_ram_info()
    window.mainloop()
