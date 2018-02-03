#!/bin/sh

echo "Stopping services"
sudo systemctl stop keyboard-rasiel.service
systemctl --user stop chroma-rasiel.service
sleep 1
echo "Reloading daemons"
sudo systemctl daemon-reload
systemctl --user daemon-reload
sleep 1
echo "Starting services"
sudo systemctl start keyboard-rasiel.service
systemctl --user start chroma-rasiel.service
echo "Done"
