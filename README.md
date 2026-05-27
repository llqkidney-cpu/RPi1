sudo apt update && sudo apt upgrade -y

sudo apt install rtl-sdr -y

rtl_test

sudo apt install python3-pip -y 


pip install pyrtlsdr --break-system-packages

sudo apt install rtl-sdr librtlsdr-dev -y


pip install pyrtlsdr==0.2.92 --break-system-packages


GPS STUFF

sudo nano /boot/firmware/config.txt
dtoverlay=pps-gpio,gpiopin=4
sudo apt install pps-tools 
sudo ppstest /dev/pps0
sudo apt install gpsd gpsd-clients
sudo nano /etc/default/gpsd:

DEVICES="/dev/ttyUSBO /dev/pps0"
GPSD_OPTIONS="-n"
START_DAEMON="true"
sudo systemetl restart gpsd
sudo ntpshmmon

sudo apt install chrony gpsd gpsd-clients

sudo nano /etc/chrony/chrony.conf
refclock SHM 0 refid GPS precision 1e-1 
refclock SHM 2 refid PPS precision 1e-7

sudo systemctl restart chrony
chronyc sources - v


