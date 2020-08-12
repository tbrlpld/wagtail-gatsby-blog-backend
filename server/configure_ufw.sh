#!/bin/bash
echo "Configuring ufw..."
if [[ $(sudo ufw status) == "Status: inactive" ]] 
then
	echo "UFW not active. Configuring..."
	ufw default deny incoming
	ufw default allow outgoing
	ufw allow ssh
	ufw allow 2222/tcp  # Only for vagrant VM.
	ufw allow 2200/tcp
	ufw allow www
	ufw allow 443  # https
	ufw --force enable
fi
ufw reload
echo "UFW " $(sudo ufw status)
