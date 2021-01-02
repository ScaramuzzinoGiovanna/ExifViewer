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

    def remove_imgs(self, items):
        current = False
        imgs = [i.toolTip() for i in items]
        for elem in imgs:
            self.listElem.remove(elem)
            if elem == self.currentImg:
                current = True
        self.imgDel.emit([items, current])

    def remove_all_imgs(self):
        self.listElem = []
        self.imgDel.emit([1, True])

    def upload_img(self, item, i):
        if type(item) == str:  # è già il path dell'imm
            self.currentImg = item
        else:
            self.currentImg = item.toolTip()
            i = self.listElem.index(self.currentImg)
        indx = i
        self.imgUp.emit([self.currentImg, indx])  # ritorna il path img
