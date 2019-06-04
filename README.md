## Camino Gui
<img src="res/blue-sailing-boat-water.svg" align="right" alt="Camino GUI" width="150"/>

This program provides a graphical user interface to configure and control the AIS
transponder devices from the AMEC Camino (R) series which are typically found on
sailing yachts.
The software allows to program the ship data into the AIS transponder device (name, call sign, dimensions, ...).
Additionally the NMEA log, sent by the device can be monitored and the GPS status
information is displayed.
The program is written and tested on a Linux platform but may function as well on other operating systems.

## Installation and usage
On Ubuntu you need to install (at least)

```bash
sudo apt-get install python-qt4 pyqt4-dev-tools python-serial make
```

Then build the user interface classes

```bash
make
```

Run the program with

```bash
python2 camino-qtGui.py
```

At this point the camino device needs to be connected (via USB) to the computer.
The user needs to have read/write permissions for the USB device.

## Disclaimer
The software is provided "as is" and the author disclaims all warranties with
regard to the software including all implied warranties of merchantability
and fitness. In no event shall the author be liable for any special, direct,
indirect, or consequential damages or any damages whatsoever resulting from
loss of use, data or profits, wheter in an action of contract, negligence or
other tortious action, arising out of or in connection with the use or performance
of this software.

## License
This software is released under the terms of the GPL (3.0). It is not connected
in any way with the AMEC (TM) corporation.
