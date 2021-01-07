from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


# A PyQT5 Observable object class.
class Observable(QObject):
    imgAdded = pyqtSignal(object)
    imgDel = pyqtSignal(object)
    imgUp = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.listElem = []
        self.currentImg = None

    def observe(self, slot1, slot2, slot3):
        self.imgAdded.connect(slot1)
        self.imgDel.connect(slot2)
        self.imgUp.connect(slot3)

    # We access the value through this getter/setter property.
    @pyqtProperty(object)
    def values(self):
        return self.listElem

    # Note that we need to explicitly emit() the signal. Declaring the
    # pyqtProperty with the notify=valueChanged above will have
    # benefits when we, for example, want to use this model in QML.
    @values.setter
    def values(self, newElems):
        for elem in newElems:
            self.listElem.append(elem)
        self.imgAdded.emit(newElems)  # emesso dopo che il valore è stato cambato

    def remove_imgs(self, path_imgs, items):
        current = False
        for elem in path_imgs:
            self.listElem.remove(elem)
            if elem == self.currentImg:
                current = True
                self.currentImg = None
        self.imgDel.emit([items, current])

    def remove_all_imgs(self):
        self.listElem = []
        self.currentImg = None
        self.imgDel.emit([1, True])

    def upload_img(self, path_img, exif):
        self.currentImg = path_img
        indx = self.listElem.index(self.currentImg)
        self.imgUp.emit([self.currentImg, indx, exif])  # ritorna il path img
