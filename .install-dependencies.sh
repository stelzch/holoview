#!/bin/sh
pip3 install -r requirements.txt
if [ ! -d "$OPENCV_DIR/lib" ]; then
    wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.tar.gz -O opencv-$OPENCV_VERSION.tar.gz
    tar xzf opencv-$OPENCV_VERSION.tar.gz
    rm opencv-$OPENCV_VERSION.tar.gz
    cd opencv-$OPENCV_VERSION
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX="$OPENCV_DIR" -DPYTHON3-EXECUTABLE=$(which python3)  -DPYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") ..
    make -j2
    make install
else
    echo OpenCV already built, using that install.
fi
cp -rv /usr/lib/python3/dist-packages/numpy* /home/travis/virtualenv/python$TRAVIS_PYTHON_VERSION/lib/python3/site-packages
ls -R /home/travis/virtualenv
