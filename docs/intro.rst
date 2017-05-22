Introduction - Getting started!
===============================

Installation
------------
Primary Requirements: Raspberry Pi 3 with attached PiCamera running Raspbian

The preferred way of installation is through our debian repository. This ensures you have the most recent version of HoloView installed, alongside with its dependencies. To add our debian repository, append this line to your `/etc/apt/sources.list` file on the Raspberry Pi:
`deb http://debian.ch-st.de/ jessie main`. 

Now you can easily install `python3-holoview` after a quick `apt update`. Below are all steps listed necessary to install HoloView:

.. code:: shell

    $ sudo -s
    # cat "deb http://debian.ch-st.de/ jessie main" >> /etc/apt/sources.list
    # apt update
    # apt install python3-holoview
    # exit

And that's it! You can now launch HoloView from the start menu under the *Education* tab.    

Usage
=====

The usage of HoloView is fairly simple. It has two main modes, which both have to panes:

Capture mode:
    In this mode, the light hitting the camera chip's surface will be converted into electrical signals and then be stored in a two-dimensional matrix. This process is commonly known as *taking a photo*.
    On the left side of the window you can adjust a variety of settings, consult **TODO** for an explaination. The default settings usually fit your needs. A really important parameter is the resolution. Because the processing power of the Raspberry Pi is limited, everything will take some time. Lowering the resolution usually lowers the processing speed.
    After you are happy with the settings, you can hit that *Preview* button at the very bottom or simply type `<Ctrl-P>`. This will open up a live preview allowing you to see what the Pi Camera sees. Please note that some of the capture parameters have no effect on the live preview, most namely `exposure`. If you are connected to the Pi via VNC, you won't be able to see anything. This is due to the Pi's GPU rendering the images directly ontop of the framebuffer driver -- making it only visible on the HDMI output.

Script mode:
    
