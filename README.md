# Wagtail Gatsby Blog (Backend)

![example workflow file path](https://github.com/tbrlpld/wagtail-gatsby-blog-backend/workflows/Greet%20Everyone/badge.svg)

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

The packing will include a locally available `.env` file. This file should be
configured for production before generating the distribution package. This file
may also be empty and be configured on the production host. It's only real
purpose is to define the `SECRET_KEY` environment variable in production that
Django needs as a cryptography salt. Other settings set typically through
environment variables that are not sensitive are set in the `docker-compose.yml`.


## Simulating the Production Setup

The `Vagrantfile` defines a machine that can be interpreted as a simulated
production server.

The provisioning installs and configures the necessary software on the VM. Most
of those steps are performed by the scripts in the `/server` directory. This
directory is contained in the `dist.tar.gz` archive.

During provisioning, the `dist.sh` script packages the data. This package is
then extracted into `/home/dockrunner/app`. This is simulating the copying to the
server and extracting of the data with your non-root sudo user.

The following steps are basically just running the scripts in the `./server`
directory, which is included in the distribution archive. These scripts install
and configure `docker`, `nginx` and `ufw`.

The first script also create the `dockrunner` user. This name is important as
it is used in the other docker configuration steps. The user name could be
anything else. It is only important that the user name is kept consistent
between the script concerning the docker configuration. The `dockrunner`
user, which is created during the provisioning, has a restricted login shell.
This means the user will only be able to execute a very limited set of commands.

Once the provisioning is done and you login to the VM with `vagrant ssh` you
should switch to the `dockrunner` user with `sudo -u dockrunner -i`. This will
give you the restricted shell experience that this user would experience after
login. If you do need to run unrestricted commands as the typically restricted
user, you can start a different like so `sudo -u dockrunner bash`. This of
course is only possible from a `sudo` user account.

To start serving the backend as the `dockrunner` user (which will always be
logged into it's home directory and is not allowed to switch directories) by
running following command.

```shell
$ docker-compose -f ./app/docker-compose.yml up -d --no-build
```

The container is running in detached mode and is set to restart automatically,
unless it is stopped explicitly. When the host restarts, then the Docker daemon
will restart automatically and then restart the container automatically.

The Vagrant machine is configured with port forwarding from `8000` on the host
to `80` on the VM. That means to test production the backend setup, you can be
visited at `http://localhost:8000/cms` in the browser.

If you make changes to the code base that you want to test in a production
like configuration, you will need to build the images manually on the VM. This
can be achieved by starting an unrestricted shell for `dockrunner` with
`sudo -u dockrunner bash`, then `cd /vagrant` to switch to the shared
directory and run `docker-compose build`.

## Production Configuration

The production configuration requires two environment variables to be set.

`SECRET_KEY` is critical and must exist otherwise the app won't start. this
is the encryption salt used by Django to secure the sessions with the backend.

`NETLIFY_BUILD_HOOK_URL` is not required, but certainly recommended. This URL
is triggered whenever a page is published on the backend and results in a rebuild
of the Gatsby frontend. The app will start without this variable, but then
each build of the frontend needs to be triggered manually. This means that
publishing a page on the in Wagtail does not really result in a published page
on the frontend.

Both these variables can be defined in a `.env` file the lives next to the
`docker-compose.yml` on the production host. These variables are available in
the Wagtail container environment when it is started through the compose file.
