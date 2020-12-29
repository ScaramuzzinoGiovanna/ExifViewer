from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QListWidgetItem, QListView
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from ui_exifViewer import Ui_ExifViewer
from model import M
import sys
from os.path import expanduser


class ExifViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # set up the user interface from Designer
        self.ui = Ui_ExifViewer()
        self.ui.setupUi(self)

        self.ui.button_rotateRight.clicked.connect(lambda: print('rotR'))
        self.ui.button_rotateLeft.clicked.connect(lambda: print(''))
        self.ui.button_previous.clicked.connect(lambda: print(''))
        self.ui.button_next.clicked.connect(lambda: print(''))
        self.ui.button_addImages.clicked.connect(lambda: M.add_img(
            QFileDialog.getOpenFileNames(self, 'Open file', expanduser("~"), "Image files (*.jpg)")))
        self.ui.button_deleteAllImages.clicked.connect(M.delete_AllImgs)
        self.ui.button_deleteSelectedImages.clicked.connect(
            lambda: M.delete_SelectedImgs(self.ui.listWidget.selectedItems()))
        self.ui.listWidget.itemDoubleClicked.connect(lambda: M.upload_img(self.ui.listWidget.currentItem()))
        M.observe(self.show_preview_image_into_list, self.delete_preview, self.show_img)

    def show_preview_image_into_list(self, img_path):
        for img in img_path:
            icon = QIcon(QPixmap(img))
            item = QListWidgetItem(icon, None)
            item.setToolTip(img)
            self.ui.listWidget.addItem(item)

    def delete_preview(self, sign):
        items = sign[0]
        delCurrentImageUp = sign[1]
        if items == 1:  # flag che indica che devo eliminare tutte le immagini
            self.ui.listWidget.clear()
        else:
            for item in items:
                self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
        if delCurrentImageUp == True:
            self.ui.image.clear()
            self.defaultImage()

    def defaultImage(self):
        self.ui.image.setText('Select image')

    def show_img(self, path_img):
        self.ui.image.upload_img(path_img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExifViewer()
    window.show()
    sys.exit(app.exec_())
