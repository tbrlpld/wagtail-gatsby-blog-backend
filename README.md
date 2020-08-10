# Wagtail Gatsby Blog (Backend)

![example workflow file path](https://github.com/tbrlpld/wagtail-gatsby-blog-backend/.github/workflows/first-workflow.yml/badge.svg)

Example project for me to figure out how to connect Wagtail as CMS on the
backend with Gatsby for the frontend.

This setup is only designed for a single developer creating the site locally
and then deploying the CMS on a webserver. Once the production server is up
and running, all changes to content and media should be done directly on the
production server (as I am not sure about any good merging strategies).

## Development

You can either run the development completely locally, or you can run in side
the container.

To start the Wagtail container with development settings just run the following
command in the repo root.

```shell
$ docker-compose -f dev.docker-compose.yml
```

You should be able to connect to the Wagtail admin at
`http://localhost:8000/cms`.

## Packaging Data for Distribution

To prepare data for distribution run the `./script/dist.sh` script.
This script packages the necessary data into a `./dist/dist.tar.gz`.
This archive is what you want to copy to the production server (with `scp` for
example).

The data that was added to the Wagtail admin during development is stored
locally in the `data/db.sqlite` and in the `data/media` directories.
This data is packaged by the `dist.sh` script. This means the data is available
on the host after the archive is extracted.

Also, you need to define a `SECRET_KEY` that Django needs as a cryptography
salt.

## Simulating the Production Setup

The `Vagrantfile` defines a machine that can be interpreted as a simulated
production server.

The provisioning installs and configures the necessary software on the VM. Most
of those steps are performed by the scripts in the `/server` directory. This
directory is contained in the `dist.tar.gz` archive.

During provisioning, the `dist.sh` script packages the data. This package is
then extracted into `/home/vagrant/app`. This is simulating the copying to the
server and extracting of the data with your non-root sudo user.

The following steps are basically just running the scripts in the `./server`
directory, which is included in the distribution archive. These scripts install
and configure `docker`, `nginx` and `ufw`.

The first script also create the `dockrunner` user. This name is important as
it is used in the other docker configuration steps. The user name could be
anything else. It is only important that the user name is kept consistent
between the script concerning the docker configuration.

Once the provisioning is done and you login to the VM with `vagrant ssh` you
should switch to the `dockrunner` user with `su - dockrunner`. You might have to
set a password for `dockrunner` (with `sudp passwd dockrunner`) before you can
login to the user. Or you do not set a password and run commands as the user
from your sudo user.

You can now start serving Wagtail by changing into `/home/dockrunner/app` and
running following commands.

```shell
$ cd /vagrant/dist/app
$ docker-compose build
$ docker-compose up -d
```

The container is running in detached mode and is set to restart automatically,
unless it is stopped explicitly. When the host restarts, then the Docker daemon
will restart automatically and then restart the container automatically.

The Vagrant machine is configured with port forwarding from `8080` on the host
to `80` on the VM. That means to test the backend setup, you can visit
`http://localhost:8080/cms` in the browser.

If you make changes to the code base that you want to test in a production
like configuration, just stop the container on the VM with `docker-compose down`
and then on the host rerun the provisioning `vagrant provision`.
This will rebuild the container images on the VM that can then be started again.
