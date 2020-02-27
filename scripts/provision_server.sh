#!/bin/bash

# Setup server for data-pipeline 
# install MinIO and MySQL

# Setup MINio
wget https://dl.min.io/server/minio/release/linux-amd64/minio
sudo chmod +x minio
sudo mkdir /data
sudo chown ubuntu /data && sudo chmod u+rxw /data

# get MySQL 
sudo apt-get update 
sudo apt-get install mysql-server

