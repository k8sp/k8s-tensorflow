##!/bin/bash
#
# https://github.com/vmware/harbor/blob/master/docs/configure_https.md
#

if [[ "$#" -ne 2 ]]; then
  echo "Usage $0 ail.unisound.com 1(use exist private key)/0(create new private key)"
  echo "Usage $0 10.10.10.1 1(use exist private key)/0(create new private key)"
  exit -1
fi

# Clean
rm -rf ./*.{crt,csr,cnf,pem}
rm -rf demoCA

domain_IP=$1
isIP=0
days=3650

# Create config file
cat > openssl.cnf <<EOF
[ req ]
prompt = no
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
C = CN 
ST = Beijing
L = Beijing
O = Unisound
OU = AILabs
CN = $domain_IP
emailAddress = liuqingsong@unisound.com
EOF


if [[ $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  isIP=1
  echo "IP: $domain_IP"
else
  echo "Domain: $domain_IP"
fi




if [[ $2 =~ "1" ]]; then
  echo "Using exist ca.key and ${domain_IP}.key"

# Create your own CA certificate
openssl req \
    -new -key ca.key \
    -config openssl.cnf -x509 -days $days -out ca.crt

# Generate a Certificate Signing Request
# e.g. harbor.ail.unisound.com -> domain=ail.unisound.com
openssl req \
    -new -key ${domain_IP}.key \
    -config openssl.cnf -out ${domain_IP}.csr

else
  echo "Creating new ca.key and ${domain_IP}.key"
  rm -rf ./*.key

# Create your own CA certificate
openssl req \
    -newkey rsa:4096 -nodes -sha256 -keyout ca.key \
    -config openssl.cnf -x509 -days $days -out ca.crt

# Generate a Certificate Signing Request
# e.g. harbor.ail.unisound.com -> domain=ail.unisound.com
openssl req \
    -newkey rsa:4096 -nodes -sha256 -keyout ${domain_IP}.key \
    -config openssl.cnf -out ${domain_IP}.csr

fi


# Generate the certificate of your registry host
# Ubuntu
. /etc/os-release
if [[ $ID == "ubuntu" ]]; then
  echo "OS: $ID"
  mkdir -p demoCA
  cd demoCA
  touch index.txt
  echo '01' > serial
  cd ..

else 
  echo "unsupported OS: $ID"
# CentOS
#rm /etc/pki/CA/index.txt
#touch /etc/pki/CA/index.txt
#echo 00 > /etc/pki/CA/serial

fi


if [[ $isIP -eq 0 ]]; then
  echo "Use Domain: $domain_IP"
  openssl ca -in ${domain_IP}.csr -out ${domain_IP}.crt -cert ca.crt -keyfile ca.key -days $days -outdir .
else
  echo "Use IP: $domain_IP"
  echo subjectAltName = IP:$domain_IP > extfile.cnf
  openssl ca -in ${domain_IP}.csr -out ${domain_IP}.crt -cert ca.crt -keyfile ca.key -days $days -extfile extfile.cnf -outdir .
fi

# How to use
echo "-------------------------------------------------"
echo "Use ${domain_IP}.{crt,key} for harbor nginx"
echo "Use ca.crt for client"
echo "-------------------------------------------------"



