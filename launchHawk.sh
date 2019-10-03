#!/bin/bash

# Attempts to remove existing cards, start Fabric, run npm install, add card and start composer rest server.
# NOTE: This script assumes the HawKoin-Fabric distro and fabric-dev-servers are in ~/

echo "Starting..."

echo "Attempt to remove existing card"

composer card delete -c PeerAdmin@hlfv1

composer card delete -c admin@hawkoin-network


cd ~/fabric-dev-servers

./startFabric.sh

./createPeerAdminCard.sh

echo "Moving to ~/HawKoin-Fabric"

cd ~/HawKoin-Fabric

npm install


echo "Moving to ~/HawKoin-Fabric/dist"

cd ~/HawKoin-Fabric/dist

composer network install -a hawkoin-network.bna -c PeerAdmin@hlfv1

# NOTE: -V needs to have the latest version in the project's package.json or the command will fail.
composer network start -n hawkoin-network -V 0.1.5 -c PeerAdmin@hlfv1 -A admin -S adminpw -f networkadmin.card

composer card import --file networkadmin.card

composer-rest-server -c admin@hawkoin-network -n always

