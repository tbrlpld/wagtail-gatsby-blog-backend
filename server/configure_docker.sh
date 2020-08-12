if id dockrunner > /dev/null 2>&1
then
	echo "User dockrunner exists."
else 
	echo "Creating restricted user dockrunner..."
	mkdir /home/dockrunner
	useradd -M -d /home/dockrunner -s /bin/rbash dockrunner
	usermod -aG docker dockrunner
	mkdir /home/dockrunner/bin
	ln -s /usr/bin/docker /home/dockrunner/bin/docker
	ln -s /usr/local/bin/docker-compose /home/dockrunner/bin/docker-compose
	chmod -R 755 /home/dockrunner/bin/
	touch /home/dockrunner/.profile
	echo "PATH=/home/dockrunner/bin" > /home/dockrunner/.profile
	echo "export PATH" >> /home/dockrunner/.profile
	chmod -R 755 /home/dockrunner/.profile
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

