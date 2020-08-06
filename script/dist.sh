#!/bin/bash

# Save working directory to return to after script is done
initialdir=$(pwd)

# Get base directory for following operations. 
basedir="$(realpath $(dirname $(dirname $0)))"
cd $basedir

# Remove existing dist dir
distdir=./dist

if [ -d $distdir ]
then
	rm -rf $distdir
fi

# Create new dist dir
mkdir $distdir 

tarfile=$distdir/dist.tar
# Add all files in the base dir, except for the ones listed in .dockerignore
tar --create --file=$tarfile --exclude=./dist --exclude-from=.dockerignore .
# tar ignores .dotfiles by default, so I have to add them back manually.
# Add the .env file explicitly (this file is usually ignored)
tar --append --file=$tarfile .env .gitignore .dockerignore .python-version
# Compress archive
gzip $tarfile

# Extract (this is only to check the contents)
if [ "$1" = "-x" ]
then
	mkdir $distdir/app
	tar -xzf $tarfile.gz -C $distdir/app
fi

# Return to initial working directory
cd $initialdir