#!/bin/bash

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

echo "=== .env konfigurieren ==="
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
ENV_EXAMPLE="$SCRIPT_DIR/.env.example"

# IP-Adresse des Pis ermitteln
BROKER_IP=$(hostname -I | awk '{print $1}')

if [ ! -f "$ENV_FILE" ]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
fi
sed -i "s/^BROKER_IP=.*/BROKER_IP=$BROKER_IP/" "$ENV_FILE"

echo "Broker IP gesetzt: $BROKER_IP"

echo "=== CUPS & Drucker installieren ==="
sudo apt-get install -y cups

# Drucker hinzufügen (Name: Termo)
sudo lpadmin -p Termo \
  -v "usb://STMicroelectronics/USB%20Portable%20Printer%20%20%20%20?serial=Printer" \
  -m drv:///cupsfilters.drv/textonly.ppd \
  -E

sudo cupsenable Termo
sudo cupsaccept Termo

echo "Testdruck:"
echo "Hallo Test" | lp -d Termo

echo "=== USB-Berechtigungen für Drucker setzen ==="
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0456", ATTRS{idProduct}=="0808", MODE="0666"' | sudo tee /etc/udev/rules.d/99-escpos.rules
sudo udevadm control --reload-rules

echo "Drucker bitte ab- und wieder anstecken!"

echo "=== Python venv erstellen ==="
python3 -m venv --system-site-packages "$SCRIPT_DIR/wiesbaden-env"

echo "=== Python Pakete installieren ==="
source "$SCRIPT_DIR/wiesbaden-env/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Systemd Service einrichten ==="
sudo bash -c "cat > /etc/systemd/system/idea-machine.service <<EOF
[Unit]
Description=Idea Machine Wiesbaden
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/wiesbaden-env/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable idea-machine.service

echo "=== Setup fertig ==="