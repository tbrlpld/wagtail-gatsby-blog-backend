#!/bin/bash
# Get base directory for following operations. 
basedir="$(dirname $(dirname $0))"

# Remove existing dist dir
distdir=$basedir/dist
if [ -d $distdir ]
then
	rm -rf $distdir
fi

# Create new dist dir
mkdir $distdir 

tarfile=$distdir/dist.tar
# Add all files in the base dir, except for the ones listed in .dockerignore
tar -cf $tarfile -X .dockerignore $basedir/* $basedir/.gitignore $basedir/.dockerignore
# Add the .env file explicitly (this file is usually ignored)
tar -rf $tarfile $basedir/.env
# Compress archive
gzip $tarfile

# Extract (this is only to check the contents)
if [ "$1" = "-x" ]
then
	mkdir $distdir/out
	tar -xzvf $tarfile.gz -C $distdir/out
fi
