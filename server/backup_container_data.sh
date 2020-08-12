scriptdir=$(realpath $(dirname $0))
basedir=$(realpath $(dirname $scriptdir))

docker run --rm --volumes-from wagtail-gatsby-blog-wagtail -v $basedir/backup:/backup ubuntu tar cvf /backup/backup.tar /code/data