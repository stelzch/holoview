#!/bin/sh
###############################################################################
###  BUILD A .DEB-PACKAGE FROM THE SOURCE                                   ###
###############################################################################
# 1. prepare the target directory					      #
# 2. create python binary distribution package				      #
# 3. calculate the md5sums of its files					      #
# 4. add metadata in a control file                                           #
# 5. archive the data and control directory                                   #
#                                                                             #
# For general information about the structure of a .deb-package:	      #
#   - http://tldp.org/HOWTO/html_single/Debian-Binary-Package-Building-HOWTO  #
#   - https://en.wikipedia.org/wiki/Deb_(file_format)                         #
###############################################################################

# Check if sed is present, otherwise quit.
command -v sed >/dev/null 2>&1 || {
    echo "Error: this script requires sed, the stream editor."
    exit 1
}

# Determine the source code directory.
SCRIPTFILE=$(readlink -f "$0")
SRCDIR=$(dirname "$SCRIPTFILE")

cd $SRCDIR 

get_meta () {
    # This function gets a value supplied to the setup.py file.
    # With python3 setup.py --help you can see the possible values, these
    # include:
    # - name
    # - version
    # - author, author-email, maintainer, maintainer-email
    # - contact, contact-email
    # - url, licence
    echo $(python3.6 $SRCDIR/setup.py --$1)
}

get_dir_size () {
    # This determines the directory size in kibibytes (2^10 bytes)
    # https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-Installed-Size
    echo $(du -sB K $1 | sed -r 's/([0-9]+).+/\1/')
}

# ------------------------------ Step 1 ---------------------------------------
# Clear the dist directory
if [ -d dist ]; then
    rm -r dist/*
fi
# Make sure that it has the subdirectories data and control
mkdir -p dist/data dist/control

# ------------------------------ Step 2 ---------------------------------------
# Use the python distutils to build a binary distribution package. This creates
# a tar.gz archive in the dist directory
python3.6 $SRCDIR/setup.py bdist --format=gztar
cd dist
mv *.tar.gz data.tar.gz

# ----------------------------- Step 3 ----------------------------------------
# To calculate the checksums, we first have to extract the package
tar xf data.tar.gz -C data
cd data
# Run `md5sum` on every file and remove the leading ./ in filenames using sed
find -type f -exec md5sum {} + | sed -r 's/([0-9a-f]{32})  .\//\1 /' > ../control/md5sums
#                                              ^ ascii puke!
cd ..

# ----------------------------- Step 4 ----------------------------------------
# The control file describes the packages name, version and dependencies.
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

# ----------------------------- Step 5 ----------------------------------------
# Create the deb file using `ar`. The order of files is important:
# 1. debian-binary
# 2. control.tar.gz
# 3. data.tar.gz
ar -q $(get_meta name)-$(get_meta version).deb \
    debian-binary {control,data}.tar.gz
# Remove the temporary build files
rm -r {control,data}.tar.gz control data debian-binary

# And that's it! We have just build a debian package from scratch, without any
# debian-specific tooling.
