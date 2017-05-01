import unittest
import numpy as np
import cv2
from matplotlib.figure import Figure
from holoview.scripting import Script
from holoview.project import Project
import holoview.log


logger = holoview.log.create_custom_logger('HoloView')
logger.debug('Starting application')

class TestScriptMethods(unittest.TestCase):
    script = Script()
    image = np.zeros((480, 320))

    def test_source_parameter(self):
        self.script.set_source('Hello World✓')
        self.assertEqual(self.script.get_source(), 'Hello World✓')

    def test_basic_execute(self):
        self.script.set_source("""output_vars["testvar1"] = 45.123455
output_vars["pi"] = 3
output_vars["boolVal"] = False
output_vars["cvVersion"] = cv2.__version__""")
        self.script.execute(self.image)
        vars, figs = self.script.get_results()
        self.assertEqual(len(figs), 0)
        self.assertEqual(len(vars), 4)
        self.assertEqual(vars["testvar1"], 45.123455)
        self.assertEqual(vars["pi"], 3)
        self.assertEqual(vars["cvVersion"], cv2.__version__)
        self.assertFalse(vars["boolVal"])

    def test_figure_execute(self):
        self.script.set_source("""output_figs["testfig"] = plt.figure()
plt.axis('off')""")
        self.script.execute(self.image)
        vars, figs = self.script.get_results()
        self.assertEqual(vars, dict())
        self.assertEqual(len(figs), 1)
        self.assertIsInstance(figs["testfig"], Figure)

class TestProjectMethods(unittest.TestCase):

    def test_params(self):
        author1 = "John Doe <jdoe@example.com>"
        desc1 = "Example\nText"

        p = Project(author=author1)
        self.assertEqual(p.get_author(), author1)
        self.assertEqual(p.get_title(), "")
        self.assertEqual(p.get_description(), "")
        
        p.set_description(desc1)
        self.assertEqual(p.get_description(), desc1)
        self.assertEqual(p.get_title(), "")
    
    def test_export(self):
        author = "Alice"
        title = "Ex Proj"
        desc = "Some description"
        script = Script()
        script.set_source("hello testcase")
        p = Project(title, author, desc)
        p.set_script(script)
        p.set_image(np.ones((480, 320, 3)))
        p.save("/tmp/exproj.zip")
        p2 = Project()
        p2.load("/tmp/exproj.zip")

        self.assertEqual(p2.get_author(), p.get_author())
        self.assertEqual(p2.get_author(), author)
        self.assertEqual(p2.get_title(), title)
        self.assertEqual(p2.get_title(), p.get_title())
        self.assertEqual(p2.get_description(), desc)
        self.assertEqual(p2.get_description(), p.get_description())
        self.assertEqual(p2.get_script().get_source(), script.get_source())
        self.assertEqual(p2.get_script().get_source(),
                         p.get_script().get_source())
    


if __name__ == '__main__':
    unittest.main()
