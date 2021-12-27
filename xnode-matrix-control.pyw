import tkinter as tk
from tkinter.constants import W
import json
from functools import partial

from LWRPClient import LWRPClient

input_channels = {  # list of channel names and numbers in xnode matrix
    'NonStop PC':   1,
    'Studio 1': 5,
    'Studio 2': 7,
    'Sonobus Feed': 13,
    'Productie PC': 15,
    'Line 1 in':    17,
    'Line 2 in':    19,
    'Line 3 in':    21,
    'AES in':       23,
}

mytitle="Simple Xnode Matrix Control"
xnode_address="localhost"
xnode_port=1993

# ----------------------
LWRP = LWRPClient(xnode_address, xnode_port)

def handle_destroy(event):
    """Handle window destroy event - must end LWRP connection to xnode"""
    xnode_stop()

def matrixCallback(data):
    print ("--- MATRIX CALLBACK ---")
    # data is a list of connections
    for d in data:
        dest=d["dst"]
        source=d["src"]  # source is again a list of sources
        # print (dest," ", source)
        
        for src in source:
            srcnum=src["num"]
            for inp, inp_ch in input_channels.items():
                if srcnum == inp_ch:
                    print(f"{dest}L - srcnum: {srcnum}")
                    txt_text.insert(tk.END, f"{dest}L: {srcnum} - MATCH\n")
                    btn_conn[inp_ch]["background"]="orange"

                if srcnum == inp_ch+1:
                    print(f"{dest}L - srcnum: {srcnum}")
                    txt_text.insert(tk.END, f"{dest}R: {srcnum} - MATCH\n")



def xnode_connect():
    LWRP.login()
    window.title(mytitle + f" LWRP:{xnode_address}:{xnode_port}")
    LWRP.matrixSub(matrixCallback)

def xnode_connect_input(srcchan : int, dstchan: int):
    # Mixer matrix channel input srcchan(+1) to output dst(+1), -3dB gain
    if srcchan==0 or dstchan==0:
        return
    LWRP.matrixSet(dstchan,srcchan,-30) # Left
    LWRP.matrixSet((dstchan+1),(srcchan+1),-30) # Right

def xnode_disconnect_input(srcchan : int, dstchan : int):
    if srcchan==0 or dstchan==0:
        return
    LWRP.matrixSet(dstchan,srcchan,"-")
    LWRP.matrixSet(dstchan+1,(srcchan+1),"-")
    btn_conn[srcchan]["background"]="green"

def xnode_stop():
    LWRP.stop()
    window.mainloop(exit())

# --------------------
window = tk.Tk()
window.title(mytitle)
window.bind("<Destroy>", handle_destroy)

#window.rowconfigure([0, 1, 2, 3],minsize=100, weight=1)
window.columnconfigure([0, 1], weight=1)

fr_buttons=tk.Frame(master=window)
fr_text=tk.Frame(master=window)

fr_buttons.grid(row=0,column=0, sticky="ns", padx=10, pady=10)

lbl_title=tk.Label(master=fr_buttons, text="xNode Matrix connections:", font=("Trebuchet MS",14, "bold"))
lbl_title.grid(column=0,row=0, columnspan=2)

# array of connect/disconnect buttons for each channel
btn_conn = {}
btn_disc = {}

rownr = 1
# create buttons for each channel and place them in a grid
for channel_name, channel_nr in input_channels.items():
    btn_conn[channel_nr]=tk.Button(master=fr_buttons, text=f"Connect {channel_name}",background="green",
        relief=tk.RAISED, borderwidth=5, command=partial(xnode_connect_input, channel_nr, 1))
    btn_disc[channel_nr]=tk.Button(master=fr_buttons, text=f"Disconnect {channel_name}",background="red",
        relief=tk.RAISED, borderwidth=5, command=partial(xnode_disconnect_input, channel_nr, 1))
    btn_conn[channel_nr].grid(column=0, row=rownr, padx=5, pady=5, sticky="ew")
    btn_disc[channel_nr].grid(column=1, row=rownr, padx=5, pady=5, sticky="ew")
    rownr += 1


txt_text=tk.Text(master=fr_text, padx=5, pady=5)
txt_text.grid(column=0,row=1, columnspan=2, sticky="ew")

fr_text.grid(row=1, column=0, columnspan=2, sticky="nsew")

xnode_connect()

window.mainloop()