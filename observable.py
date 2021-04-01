from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


# A PyQT5 Observable object class.
class Observable(QObject):
    imgAdded = pyqtSignal(object)  # thumbnail image is added to the list
    imgDel = pyqtSignal(object)  # thumbnail image is deleted to the list
    imgUp = pyqtSignal(object)  # image is uploaded/show with exif data

    def __init__(self):
        super().__init__()
        self.list_previews = []
        self.current_img = None

    def observe(self, slot1, slot2, slot3):
        self.imgAdded.connect(slot1)
        self.imgDel.connect(slot2)
        self.imgUp.connect(slot3)

    @pyqtProperty(object)
    def previews(self):
        return self.list_previews

    @pyqtProperty(object)
    def currentImage(self):
        return self.current_img

    @previews.setter
    def previews(self, newElems):
        for elem in newElems:
            self.list_previews.append(elem)
        self.imgAdded.emit(newElems)

    def remove_imgs(self, path_imgs, items):
        """ remove one or more images and emit the corrispondent signal to delete these images from view  """
        current = False
        for elem in path_imgs:
            self.list_previews.remove(elem)
            if elem == self.current_img:
                current = True
                self.current_img = None
        self.imgDel.emit([items, current])

    def remove_all_imgs(self):
        """ remove all images and emit the correspondent signal to delete these images from view """
        self.list_previews = []
        self.current_img = None
        self.imgDel.emit([1, True])

    def upload_img(self, path_img, exif):
        """ stores the current image to shown and emit the correspondent signal to shown the image with its exif data"""
        self.current_img = path_img  # current_img is the image path
        indx = self.list_previews.index(self.current_img)
        self.imgUp.emit([self.current_img, indx, exif])
