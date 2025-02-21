#!/bin/bash

docker stack rm scd3

echo "Wait for the services to stop..."
sleep 10
echo "Done."

read -p "Do you want to delete the volumes? (y/n): " delete_volumes

if [[ "$delete_volumes" =~ ^[Yy]$ ]]; then
    rm -rf grafana_data
    rm -rf influxdb_data
    echo "Volumes deleted."
else
    echo "Volumes not deleted."
fi
