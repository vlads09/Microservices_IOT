#! /bin/bash

mkdir grafana_data
mkdir influxdb_data

chmod o+w grafana_data

docker build -f adapter/Dockerfile -t adapter adapter

docker stack deploy -c stack.yml scd3

echo "Wait for the services to start..."
sleep 10
echo "Done."
