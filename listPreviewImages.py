from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget


class ListPreviewImages(QListWidget):

    def __init__(self, widget):
        QListWidget.__init__(self, widget)

    def mousePressEvent(self, event):
        """ override QlistWidget method to deselect images when click right """
        if event.button() == Qt.RightButton:
            self.clearSelection()
        else:
            super(ListPreviewImages, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """ override QlistWidget method to select new image
            (which is shown with the relative exif data)
            and deselect all the other
        """
        try:
            item = self.currentItem()
            self.clearSelection()
            item.setSelected(True)
            super(ListPreviewImages, self).mouseDoubleClickEvent(event)
        except:
            print('No item selected')
