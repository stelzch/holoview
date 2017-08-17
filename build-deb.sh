#!/bin/sh
SCRIPTFILE=$(readlink -f "$0")
SRCDIR=$(dirname "$SCRIPTFILE")

get_meta () {
    echo $(python3 $SRCDIR/setup.py --$1)
}
get_dir_size () {
    echo $(du -sB K $1 | sed -r 's/([0-9]+).+/\1/')
}

rm -r dist/*
mkdir -p dist/data dist/control
python3 setup.py bdist --format=gztar
cd dist
mv *.tar.gz data.tar.gz
tar xf data.tar.gz -C data
cd data
find -type f -exec md5sum {} + | sed -r 's/([0-9a-f]{32})  .\//\1 /' > ../control/md5sums
cd ..

# control file
echo "Package: $(get_meta name)
Version: $(get_meta version)
Section: science
Priority: optional
Architecture: all
Depends: python3, python3-gi, gir1.2-gtk-3.0, python3-picamera, python3-pil, \
opencv-python(>=3.2.0), opencv-libs(>=3.2.0),python3-matplotlib, \
python3-numpy, python3-cairocffi, gir1.2-gtksource-3.0, python3-gi-cairo
Suggests: holoview-doc
Installed-Size: $(get_dir_size data)
Maintainer: $(get_meta contact) <$(get_meta contact-email)>
Description: $(get_meta description)" > control/control
echo -e "2.0\n" > debian-binary

tar czf control.tar.gz -C control .
ar -q $(get_meta name)-$(get_meta version).deb \
    debian-binary {control,data}.tar.gz
rm -r {control,data}.tar.gz control data debian-binary
