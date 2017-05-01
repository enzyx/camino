## Camino gui
This program provides a useful tool to configure and control the AIS transponder
devices from the AMEC Camino (R) series. The program provides a convenient tool
to program the ship data into the device (name, call sign, dimensions, ...).
Additionally the NMEA log sent by the device can be monitored and the GPS status
information is displayed in a nice widget. To program is written and tested to
run on a Linux platform but may function as well on other operating systems.

## Installation and usage
On ubuntu you need to install (at least)

```bash
sudo apt-get install python-qt4 pyqt4-dev-tools python-serial make
```

Then you need to build the user interface classes

```bash
make
```

Run the program by with

```bash
python2 camino-qtGui.py
```

At this point your camino device needs to be connected (via USB) to your computer.
Make sure that the device is accessible from your user account.

## Disclaimer
The software is provided "as is" and the author disclaims all warranties with
regard to the software including all implied warranties of merchantability
and fitness. In no event shall the author be liable for any special, direct,
indirect, or consequential damages or any damages whatsoever resulting from
loss of use, data or profits, wheter in an action of contract, negligence or
other tortious action, arising out of or in connection with the use or performance
of this software.

## License
This software is released under the terms of the GPL (3.0)
