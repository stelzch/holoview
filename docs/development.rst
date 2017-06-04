Developing HoloView
===================

If you are interested in enhancing HoloView by adding new features, fixing bugs or providing additional documentation, this page is for you.


Building from source
--------------------
This project has several dependencies, not only python libraries but also native packages. This is a list of debian-packages needed to build and run this software:

* python3-picamera
* python3-pil
* python3-matplotlib
* python3-numpy
* python3-cairocffi
* python3-gi
* python3-gi-cairo
* gir1.2-gtk-3.0
* gir1.2-gtksource-3.0
* opencv-python (>= 3.2.0)

Once you have installed them, you can clone the master branch from github:

.. code-block:: shell

    $ git clone https://github.com/stelzch/holoview

For development, it is recommended to make a so called editable install. Python's package manager pip will only link your current codebase with its package index, so that any changes you have made have an immediate effect. To install the package editable, go to the project directory and execute

.. code-block:: shell

    $ sudo pip3 install -e .
    $ python3 -m holoview.__init__  # To launch the program

The other options are listed below:

.. code-block:: shell

    $ python3 setup.py sdist       # Create a source package
    $ python3 setup.py install     # Install program
    $ python3 --command-packages=stdeb.command bdist_deb  # Create a deb file

This will produce a .deb-file, which can be easily installed using `dpkg -i python3-holoview.deb`. Be aware that you have to take care of the dependencies by yourself if you are using the `dpkg -i` command. For automatic installation and updates we have set up the APT repository.
 
