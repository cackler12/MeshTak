#!/bin/bash

package_name="meshtak"
version="0.1.0"
arch="amd64"

echo "Building docker image"

docker build -t $package_name:latest .

docker save -o $package_name-$version.tar $package_name:latest

echo "Building deb package"

mkdir -p $package_name-$version-$arch/usr/bin/meshtak/dist
mkdir -p $package_name-$version-$arch/DEBIAN

cp $package_name-$version.tar $package_name-$version-$arch/usr/bin/meshtak/dist
cp docker/docker-compose.yml $package_name-$version-$arch/usr/bin/meshtak
cp pkg/meshtak.service $package_name-$version-$arch/usr/bin/meshtak
cp pkg/setup-service.sh $package_name-$version-$arch/usr/bin/meshtak
cp pkg/control pkg/postrm pkg/postinst $package_name-$version-$arch/DEBIAN/

dpkg-deb --build $package_name-$version-$arch

echo "Cleaning up and removing docker image"

rm -rf $package_name-$version.tar
rm -rf $package_name-$version-$arch

mkdir -p build

rm -rf build/*

mv $package_name-$version-$arch.deb build

docker rmi $package_name:latest