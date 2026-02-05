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
    echo "BROKER_IP=$BROKER_IP" >> "$ENV_FILE"
else
    sed -i "s/^BROKER_IP=.*/BROKER_IP=$BROKER_IP/" "$ENV_FILE"
fi

echo "Broker IP gesetzt: $BROKER_IP"

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
echo "Hallo Test" | lp -d Termo

echo "=== Python venv erstellen ==="
python3 -m venv --system-site-packages "$SCRIPT_DIR/wiesbaden-env"

echo "=== Python Pakete installieren ==="
source "$SCRIPT_DIR/wiesbaden-env/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Setup fertig ==="
