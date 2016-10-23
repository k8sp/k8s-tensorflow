#!/bin/bash

function usage(){
    echo "usage: sudo $0 domain crtfile"
}



domain=$1
crtfile=$2

docker_certs_path="/etc/docker/certs.d/$domain"

mkdir -p ${docker_certs_path}
cp $crtfile ${docker_certs_path}/ca.crt

systemctl restart docker
