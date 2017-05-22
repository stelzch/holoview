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
-----

The usage of HoloView is fairly simple. It has two main modes, which both have to panes:

Capture mode:
    In this mode, the light hitting the camera chip's surface will be converted into electrical signals and then be stored in a two-dimensional matrix. This process is commonly known as *taking a photo*.

Script mode:
    Here you can write a litte computer-program that manipulates, analyses or processes the images.



Capturing
---------

On the left side of the window you can adjust a variety of settings, consult **TODO** for an explaination. The default settings usually fit your needs. A really important parameter is the resolution. Because the processing power of the Raspberry Pi is limited, everything will take some time. Lowering the resolution usually lowers the processing speed.

After you are happy with the settings, you can hit that *Preview* button at the very bottom or simply type `<Ctrl-P>`. This will open up a live preview allowing you to see what the Pi Camera sees. Please note that some of the capture parameters have no effect on the live preview, most namely `exposure`. If you are connected to the Pi via VNC, you won't be able to see anything. This is due to the Pi's GPU rendering the images directly ontop of the framebuffer driver -- making it only visible on the HDMI output.
Once you are happy with what you are seeing and you want to keep it (atleast for five minutes or so) hit the `c` (for **capture***) button on your keyboard. This will take you back to the Desktop, but if you look now at the right side of the HoloView window, you'll recognize the image of the camera being displayed.
If you just want to quit this whole stuff to tweak the camera parameters, press `q` and you'll be returned to the Raspbian desktop with HoloView and no image captured.

Now you can switch over to...

Scripting 101
-------------
Now, as we mentioned earlier, you can work on the images with these small computer programs. Well, there are many ways to write a computer program, but in HoloView we use **Python**.

What is Python? It is a programming language which is especially easy for beginners, yet it provides many features for advanced users, so you don't have any limits other than processing power/time/speed, RAM, storage space, creativity, money, coffee, ...

There are many online resources available to learn python, just visit the *Getting started* page [#pythongs]_, have a look at the official python tutorial [#pythontut]_ or read through the python-course[#pythonkurs]_, also available in german

If you programmed in any other language before, you won't have much trouble getting into python. But enough of talking, let's dive straight into the first script! Capture and image, switch to the Scripting tab and type the following script

.. code-block:: python

    output_figs['Figure 1'] = plt.figure()     # Create a new figure
    plt.imshow(image)                          # Show the captured image in it
    output_vars['Some Var'] = 'Hello, World!'  # Display some text

To run the script, press the button in the menu bar or simply hit `<Ctrl-R>`. Now, what will this script do? As you can see, the image is shown again in the scripting tab. Also, on the bottom we have a table with an entry called *Some Var* containing *Hello, World!*. Okay okay, I know, this demo is not the most impressive thing you have seen. But it is a good starting point for changes. Before making changes however, let's examine the script.

Your script is going to work with 5 basic variables: `image`, `output_figs`, `output_vars`, `width` and `height`. As their names already suggest, `output_figs` and `output_vars` are variables used to output things from your script into HoloView. What happens in the background is basically HoloView evaluating your script, taking its output_figs and output_vars and bring them into a shape that can be displayed inside the window.

These output variables are a dictionary, basically a list with named entries. In the above example, we defined a entry called *Some Var** and it had the string *Hello, World!* as content. Try adding some more variables if you like!
The image displaying is a little bit more complicated. Your script receives an variable called `image`, which is a 3-dimensional array. The NumPy library is used to represent this object [#numpy]_ .
Now you might say: *Hang on, you mean the image is a 2-dimensional array, right?*. And at the first thought it seems logical that an image is stored in a 2-dimensional array, because the image is two-dimensional, right? Naturally yes, but because its a color image and we define colors as an array of red, green and blue values, it actually is 3-dimensional (the third dimension only contains three values, though).
`plt` is a sub-module of matplotlib [#matplotlib]_ , another great python library used to create mathematical figures. The `.figure()` creates a new Figure for us and the `plt.imshow` displays a numpy array as image.

Previously we talked about the image being a 3-dimensional array. How can we access the actual pixel values of it?

.. code-block:: python

    output_vars['Pixel value'] = image[50][20][1]

This script will print the blue-value of the pixel at x=20 and y=50. Here are multiple things to notice: First, you might have guessed the `[1]` refers to the first channel, and that being red not blue. Second, the coordinates seem swapped.
Well, the blue-red-thing is due to programmers starting to count at 0, not 1, hence red being channel 0 and blue being channel 1. And the coordinates of the image are reversed because when it's represented as a matrix, you first indicate the column (y-axis) and then the row(x-axis). So in general, you get a pixel value using `matrix[y][x][c]`.



.. [#pythongs] https://www.python.org/about/gettingstarted/
.. [#pythontut] https://docs.python.org/3/tutorial/index.html
.. [#pythonkurs] English: http://www.python-course.eu German: http://www.python-kurs.eu
.. [#numpy] http://www.numpy.org
.. [#matplotlib] http://matplotlib.org
