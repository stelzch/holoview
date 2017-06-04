#!/bin/sh

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 VERSION" >&2
    exit -1
fi

if ! hash dpkg-deb 2> /dev/null; then
    echo "Sorry, you have to install the dpkg-deb executable"
    exit -1
fi
if ! hash sphinx-build 2> /dev/null; then
    echo "You do not have the sphinx doc tool installed! It is required!"
    exit -1
fi

VERSION=$1
# Replace the version number
sed -i "s/VERSION/$VERSION/g" python3-holoview-doc/DEBIAN/control

sphinx-build . python3-holoview-doc/usr/share/doc/python3-holoview
dpkg-deb --build python3-holoview-doc
