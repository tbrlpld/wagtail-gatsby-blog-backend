if id dockrunner > /dev/null 2>&1
then
	echo "User dockrunner exists."
else 
	echo "Creating user dockrunner..."
	useradd -m -s /bin/bash dockrunner
	usermod -aG docker dockrunner
fi
daemon_config_content='{ "userns-remap":"dockrunner" }'
daemon_config_path="/etc/docker/daemon.json"
if [ "$(cat $daemon_config_path)" != "$daemon_config_content" ]
then
	echo "Activating user namespace remapping for docker..."
	echo "$daemon_config_content" > $daemon_config_path
	systemctl restart docker
else 
	echo "User namespace remapping already configured for docker."
fi

