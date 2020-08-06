# Wagtail Gatsby Blog (Backend)

Example project for me to figure out how to connect Wagtail as CMS on the
backend with Gatsby for the frontend.

This setup is only designed for a single developer creating the site locally
and then deploying the CMS on a webserver. Once the production server is up
and running all content and media changes should be done directly there.

## Packaging Data for Distribution

To prepare data for distribution run the `./script/dist.sh` script.
This script packages the repository and necessary data into a
`./dist/dist.tar.gz`. This package is what you want to copy to the production
server.

Copy the archive to the production server with `scp`. On the server, create
a new dedicated directory for the app to live in and extract the archive
with `tar -xzf $tarfile.gz -C <path/to/app/dir>`.

The data that was added to the backend during development is stored locally in
the `db.sqlite` and in the `media` directories. This data is packaged by the
`dist.sh` script. This means the data is available on the host after the
archive has been extracted.

Apart from the content data, the distribution archive should also contain a
`.env` file that defines some secrets that are needed for the deployment.
E.g. you need to define the `DJANGO_SETTINGS_MODULE` you want to use during
production.

Also, you need to define a `SECRET_KEY` that Django needs as a cryptography
salt.

Furthermore, to allow the container to update itself with updated code from
GitHub, a deploy key needs to be defined in the `.env` file. This still needs
to be implemented. The repo is currently still public and no deploy key is
needed. If this file is missing, then the packaging will fail and complain.
You could of course just create an empty file and define the setting on the
server.

## Simulating the Production Setup

The `Vagrantfile` defines a machine that can be interpreted as a simulated
production server.

During provisioning, the `dist.sh` script is run with the `-x` flag.
This option extracts the `tar` file into the directory `./dist/app`.
This directory is available on the Vagrant machine as `/vagrant/dist/app`.
This directory represents the directory on the production server where you would
extract the `tar` file to.

The provisioning also runs the installation and configuration scripts in
`./server/` (or rather `/vagrant/dist/app/server`). These scripts install
`docker` and `nginx` and they configure `ufw` and `nginx`.

The `configure_nginx.sh` script will installs a site configuration file that
sets up the serving of static and media files and the proxy forward to the app
running in the container.

To start serving the backend on the VM, just change to the  `/vagrant/dist/app`
directory and execute the following commands.
```shell
$ cd /vagrant/dist/app
$ docker-compose build
$ docker-compose up -d
```

The container is running in detached mode and is set to restart automatically,
unless it is stopped explicitly. When the host restarts then the Docker daemon
will restart the container automatically.

The Vagrant machine is configured with port forwarding from `8080` on the host
to `80` on the VM. That means to test the backend setup, you can visit
`http://localhost:8080/admin` in the browser.



