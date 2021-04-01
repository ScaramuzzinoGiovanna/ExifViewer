import sys
from os.path import expanduser

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QListWidgetItem

from model import M
from ui_exifViewer import Ui_ExifViewer


class ExifViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # set up the user interface from Designer
        self.ui = Ui_ExifViewer()
        self.ui.setupUi(self)
        self.initTable()

        # Connect buttons with functions
        self.ui.button_rotateRight.clicked.connect(self.rotateRight)
        self.ui.button_rotateLeft.clicked.connect(self.rotateLeft)
        self.ui.button_previous.clicked.connect(M.upload_previous_img)
        self.ui.button_next.clicked.connect(M.upload_next_img)
        self.ui.button_addImages.clicked.connect(lambda: M.add_imgs(
            QFileDialog.getOpenFileNames(self, 'Open file', expanduser("~"), "Image files (*.jpg)")[0]))
        self.ui.button_deleteAllImages.clicked.connect(M.delete_AllImgs)
        self.ui.button_deleteSelectedImages.clicked.connect(
            lambda: M.delete_SelectedImgs(self.ui.listWidget.selectedItems()))
        self.ui.listWidget.itemDoubleClicked.connect(lambda: M.upload_img(self.ui.listWidget.currentItem()))

        M.observe(self.show_preview_images_into_list, self.delete_preview_images_from_list, self.show_img)

    def initTable(self):
        """ initialize the exif data table """
        self.ui.ExifDataTab.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Exif'))
        self.ui.ExifDataTab.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Data'))
        self.ui.ExifDataTab.horizontalHeader().setVisible(True)
        self.ui.ExifDataTab.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        font = self.ui.ExifDataTab.horizontalHeader().font()
        font.setPointSize(14)
        font.setBold(True)
        self.ui.ExifDataTab.horizontalHeader().setFont(font)
        self.ui.ExifDataTab.setColumnWidth(0, 300)

    def show_preview_images_into_list(self, img_path):
        """ adds one or more thumbnail(previews) images to the list """
        for img in img_path:
            icon = QIcon(QPixmap(img))
            item = QListWidgetItem(icon, None)
            item.setToolTip(img)
            self.ui.listWidget.addItem(item)

    def delete_preview_images_from_list(self, sign):
        """ delete one or more thumbnail(previews) images to the list """
        items = sign[0]
        delCurrentImageUp = sign[1]
        if items == 1:  # flag indicating that all images must be deleted from the list
            self.ui.listWidget.clear()
        else:
            for item in items:
                self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
        # if preview image is the one displayed
        if delCurrentImageUp == True:
            self.ui.image.clear()
            self.ui.image.img = None
            self.ui.ExifDataTab.clearContents()
            self.ui.ExifDataTab.setRowCount(0)
            if M.listImages.currentImage == None:
                self.defaultImage()

    def defaultImage(self):
        """ sets the default text when there are no images to display """
        self.ui.image.setText('No image loaded')

    def show_img(self, item_info):
        """ shows the selected image and its exif data """
        path_img = item_info[0]
        indx = item_info[1]
        exif = item_info[2]
        self.ui.image.upload_img(path_img)
        self.ui.listWidget.clearSelection()
        self.ui.listWidget.setCurrentRow(indx)
        self.show_exifData(exif)

    def show_exifData(self, exif):
        """ show exif data """
        self.ui.ExifDataTab.clearContents()

        if exif == None or len(exif) == 0:
            self.ui.ExifDataTab.setRowCount(1)
            self.ui.ExifDataTab.setItem(0, 0, QtWidgets.QTableWidgetItem('No Exif Data for this image'))
            self.ui.ExifDataTab.setItem(0, 1, QtWidgets.QTableWidgetItem(''))
        else:
            self.ui.ExifDataTab.setRowCount(len(exif))
            items = exif.items()
            for i, elem in enumerate(items):
                self.ui.ExifDataTab.setItem(i, 0, QtWidgets.QTableWidgetItem(str(elem[0])))
                if elem[0] == 'GPSInfo':
                    gps = QLabel()
                    gps.setText('<a href="' + elem[1] + '">Open on Google Maps</a>')
                    gps.setOpenExternalLinks(True)
                    self.ui.ExifDataTab.setCellWidget(i, 1, gps)
                else:
                    self.ui.ExifDataTab.setItem(i, 1, QtWidgets.QTableWidgetItem(str(elem[1])))
        self.ui.ExifDataTab.horizontalHeader().setResizeContentsPrecision(-1)

    def rotateRight(self):
        """ rotate the image 90 degrees to the right """
        current_img = M.listImages.currentImage
        if current_img != None:
            self.ui.image.rotateRight()

    def rotateLeft(self):
        """ rotate the image 90 degrees to the left """
        current_img = M.listImages.currentImage
        if current_img != None:
            self.ui.image.rotateLeft()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExifViewer()
    window.show()
    sys.exit(app.exec_())
