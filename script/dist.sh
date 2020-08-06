#!/bin/bash
# Get base directory for following operations. 
initialdir=$(pwd)
basedir="$(realpath $(dirname $(dirname $0)))"
cd $basedir

# Remove existing dist dir
distdir=./dist
echo $distdir

if [ -d $distdir ]
then
	rm -rf $distdir
fi

# Create new dist dir
mkdir $distdir 

tarfile=$distdir/dist.tar
echo $tarfile
# Add all files in the base dir, except for the ones listed in .dockerignore
# tar ignores .dotfiles by default, so I have to add them back manually.
tar -cf $tarfile -X .dockerignore ./* .gitignore .dockerignore .python-version
# Add the .env file explicitly (this file is usually ignored)
tar -rf $tarfile .env
# Compress archive
gzip $tarfile

# Extract (this is only to check the contents)
if [ "$1" = "-x" ]
then
	mkdir $distdir/app
	tar -xzvf $tarfile.gz -C $distdir/app
fi
cd $initialdir