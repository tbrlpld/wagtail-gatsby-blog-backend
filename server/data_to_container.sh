scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))

sudo -H -u dockrunner docker-compose -f $basedir/docker-compose.yml pull
sudo -H -u dockrunner docker-compose -f $basedir/docker-compose.yml up --no-start
sudo -H -u dockrunner docker cp $basedir/data wagtail-gatsby-blog-wagtail:/code