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
from viewer import AppImageView
from widget import ImageView
#I have test this programm in linux in evoirnment which I found scrolling stays 
# in the same focus of view as your mouse is pointing over, ctr+click for panning also works good, 
#for shift-draging to create a selectable region it's zooming factor looks like big with in the second click 
# it almost finishes the zoom.
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
            
        #Example of pixel points recorded after double click are shown below and I found simlar problem that 
#        it moves down one pixel so it is good idea to test it by double clicking twise and checking if the 
#        returned last_scene_pos is the same as the second click possition.
        #(93.38888888888889, 70.61111111111111)
        #(93.64197530864197, 69.59876543209877)
        #(93.85288065843623, 69.59876543209879)
        #(94.12627648224358, 69.5206523395824)
        #(94.1696726447527, 69.4338600145642)
        #(94.14556366558097, 69.37358756663488)
        #(94.15895754289859, 69.3802845052937)
        #(94.16639858585285, 69.40632815563353)
        #(94.13952815296255, 69.40839511200971)

          # The following variables may be helpful in implementing this function:
#         centerPos = self.window.image_view.last_pos
         centerScenePos = self.window.image_view.last_scene_pos
         #print(last_posd)L
         pt = QtCore.QPoint(20,20)
         QTest.mouseDClick(self.viewport,Qt.LeftButton,pos=pt, delay =40)
         QTest.mouseDClick(self.viewport,Qt.LeftButton,pos=pt, delay =40)
         assert self.window.image_view.last_pos == centerScenePos

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
