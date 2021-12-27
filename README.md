# LWRP-xnode-matrix-controller
A simple Desktop tool to control an Axia xNode's mixer-matrix connections using LWRP, written in Python 3.

To use this tool, change xnode_address (and xnode_port) to your xnode's IP address. 
Adjust the input_channels[] list to your situation.

Based on the Livewire Routing protocol client written by Anthony Eden available on Github:
https://github.com/anthonyeden/Livewire-Routing-Protocol-Client
you need to copy the 2 .py files from this project to the same location where the xnode-matrix-control.pyw resides.

Disclaimer: 
Do not use on LIVE On Air equipment without first testing it. A single button click can make your station silent.
