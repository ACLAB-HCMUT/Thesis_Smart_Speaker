#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <server_ip>"
  exit 1
fi

SERVER_IP="$1"

echo "Switching Snapclient to $SERVER_IP..."

# Cập nhật file cấu hình
sudo sed -i "s/^SNAPCLIENT_OPTS=.*/SNAPCLIENT_OPTS=\"--host=$SERVER_IP --soundcard hw:USB,0\"/" /etc/default/snapclient

# Khởi động lại Snapclient
sudo systemctl restart snapclient

echo "Snapclient is now connected to $SERVER_IP"
