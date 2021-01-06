from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt


class ListPreviewImages(QListWidget):

    def __init__(self, widget):
        QListWidget.__init__(self, widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.clearSelection()
        else:
            super(ListPreviewImages, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        try:
            item = self.currentItem()
            self.clearSelection()
            item.setSelected(True)
            super(ListPreviewImages, self).mouseDoubleClickEvent(event)
        except:
            print('No item selected')
