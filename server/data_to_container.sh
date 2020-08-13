scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))

sudo -H -u dockrunner docker-compose -f $basedir/docker-compose.yml pull -q
sudo -H -u dockrunner docker-compose -f $basedir/docker-compose.yml up --no-start --no-build
sudo -H -u dockrunner docker cp $basedir/data wagtail-gatsby-blog-wagtail:/code