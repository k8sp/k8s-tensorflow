#!/bin/bash

function usage(){
    echo "usage: sudo $0 domain crtfile"
}



domain=$1
crtfile=$2

docker_certs_path="/etc/docker/certs.d/$domain"
centos_certs_path="/etc/pki/ca-trust/source/anchors"

mkdir -p ${docker_certs_path}
cp $crtfile ${docker_certs_path}/ca.crt

cp $crtfile ${centos_certs_path}/${domain}.crt
update-ca-trust

systemctl restart docker
