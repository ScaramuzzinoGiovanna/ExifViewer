from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize


class ImageView(QLabel):

    def __init__(self, img):
        QLabel.__init__(self, img)
        self.img = None

    def upload_img(self, path_img):
        self.img = QPixmap(path_img)

        if self.img.width() > self.img.height():
            img_resized = self.img.scaledToWidth(512)
        else:
            img_resized = self.img.scaledToHeight(512)
        self.setMaximumSize(img_resized.width(), img_resized.height())
        self.setPixmap(img_resized)
        self.adjustSize()

    def resizeEvent(self, event):
        if self.img == None:
            pass
        else:
            self.setPixmap(
                self.img.scaled(QSize(min(self.size().width(), 512), min(self.size().height(), 512)),
                                Qt.KeepAspectRatio,
                                Qt.FastTransformation))
