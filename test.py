# References:
# http://johnnado.com/pyqt-qtest-example/
# In particular, see the BitBucket link on that page

from PyQt5.QtTest import QTest
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import Qt

import mock
import sys
import unittest

from viewer import ImageViewerWindow

app = QApplication(sys.argv)
class WindowTest(unittest.TestCase):
    def setUp(self):
        input_image = "/home/dawit/pyqimageview-master/angry_unicorn.png"
        image = QtGui.QImage()
        image.load(input_image)
        self.window = ImageViewerWindow(image, input_image)
        self.window.show()

        self.viewport = self.window.image_view.viewport()

    def test_doubleClick(self):
        # The following variables may be helpful in implementing this function:
         centerPos = self.window.image_view.last_pos
         centerScenePos = self.window.image_view.last_scene_pos
         #print(last_posd)L
         pt = QtCore.QPoint(20,20)
         QTest.mouseDClick(self.viewport,Qt.LeftButton,pos=pt, delay =40)
         assert self.window.image_view.last_pos == centerScenePos
         
        #   pass

    @mock.patch('viewer.ImageViewerWindow.quit')
    def test_escape(self, quit_function):
        """ Ensure the escape key calls quit() """
        quit_function.assert_not_called()
        QTest.keyClick(self.window, Qt.Key_Escape, delay=5)
        quit_function.assert_called()

    def test_click_updates_pos(self):
        """ Ensure the escape key calls quit() """
        assert self.window.image_view.last_pos is None

        # Note: I am clicking instead of using a mouseMove event because
        # the mouseMove event does not reliably send Qt events; it looks like
        # it actually attempts to move the OSX cursor, and hopes that OSX
        # returns a mouse event, but that's not deterministically true.
        pt = QtCore.QPoint(20, 20)
        QTest.mouseClick(self.viewport, Qt.LeftButton, pos=pt, delay=40)

        assert self.window.image_view.last_pos == pt

unittest.main()
