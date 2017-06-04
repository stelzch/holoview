Scripting Cookbook
==================

Convert image to grayscale
--------------------------
For many calculations you won't need the color information. To convert a image
to grayscale, you can use the OpenCV library, which has color-conversion methods
built in:

.. code-block:: python

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
