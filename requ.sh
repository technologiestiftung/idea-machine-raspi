#!/bin/bash
#chmod +x requ.sh

echo "=== Systemupdate ==="
sudo apt-get update
sudo apt-get upgrade -y

echo "=== Mosquitto installieren ==="
sudo apt-get install -y mosquitto mosquitto-clients

echo "=== Mosquitto konfigurieren ==="
sudo bash -c 'cat > /etc/mosquitto/conf.d/listeners2.conf <<EOF
allow_anonymous true
listener 1883
EOF'

sudo systemctl restart mosquitto
sudo systemctl enable mosquitto

echo "=== CUPS & Drucker installieren ==="
sudo apt-get install -y cups

# Drucker hinzufügen (Name: Thermo)
sudo lpadmin -p Thermo \
  -v "usb://STMicroelectronics/USB%20Portable%20Printer%20%20%20%20?serial=Printer" \
  -m drv:///cupsfilters.drv/textonly.ppd \
  -E

sudo cupsenable Termo
sudo cupsaccept Termo

echo "Testdruck:"
echo "Hallo Test" | lp -d Thermo

echo "=== Python venv erstellen ==="
python3 -m venv --system-site-packages /home/wiesbaden2026/idea-machine-raspi-wiesbaden/wiesbaden-env

echo "=== Python Pakete installieren ==="
source /home/wiesbaden2026/idea-machine-raspi-wiesbaden/wiesbaden-env/bin/activate
pip install --upgrade pip
pip install paho-mqtt openai

echo "=== requirements_jim.txt erzeugen ==="
pip freeze > /home/wiesbaden2026/idea-machine-raspi-wiesbaden/requirements.txt

echo "=== Setup fertig ==="
