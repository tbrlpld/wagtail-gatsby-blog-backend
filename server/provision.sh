scriptdir=$(realpath $(dirname $0))
appdir=$(realpath $(dirname $scriptdir))

echo "*** Configure server setup ***"
$scriptdir/install_docker.sh
$scriptdir/install_nginx.sh
$scriptdir/configure_nginx.sh
$scriptdir/configure_ufw.sh
$scriptdir/configure_docker.sh

echo "*** Set ownership of data to user dockrunner ***"
chown -R dockrunner:dockrunner $appdir

echo "*** Add data to container ***"
$scriptdir/data_to_container.sh