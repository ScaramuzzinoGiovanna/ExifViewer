from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QLabel


class ImageView(QLabel):

    def __init__(self, img_w):
        QLabel.__init__(self, img_w)
        self.img = None

    def upload_img(self, path_img):
        """ upload the image to show"""
        self.img = QPixmap(path_img)
        self.setMax = False
        self.resize_img()

    def resize_img(self):
        """ resize the image to show """
        if self.img.width() > self.img.height():
            img_resized = self.img.scaledToWidth(512)
        else:
            img_resized = self.img.scaledToHeight(512)
        self.setMaximumSize(img_resized.width(), img_resized.height())
        self.setPixmap(img_resized)
        self.adjustSize()
        self.setMax = True

    def resizeEvent(self, event):
        """ resize the image as the window size changes (override QWidget method)"""
        if self.img != None and self.setMax == True:
            self.setPixmap(self.img.scaled(QSize(self.size().width(), self.size().height()), Qt.KeepAspectRatio))
        super().resizeEvent(event)

    def rotateRight(self):
        """ rotate the image 90 degrees to the right """
        self.img = self.img.transformed(QTransform().rotate(90))
        self.resize_img()

    def rotateLeft(self):
        """ rotate the image 90 degrees to the left """
        self.img = self.img.transformed(QTransform().rotate(-90))
        self.resize_img()
