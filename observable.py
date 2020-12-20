from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

# A PyQT5 Observable object class.
class Observable(QObject):
    imgAdded = pyqtSignal(object)
    imgDel = pyqtSignal(object)

    def __init__(self, val):
        super().__init__()
        self.listElem = []
        # self._values =self.values.append(val)

    def observe(self, slot1,slot2):
        self.imgAdded.connect(slot1) #permette di connettere gli ascoltatori, e quando verrà emesso il segnale verranno contattati
        self.imgDel.connect(slot2)
    # We access the value through this getter/setter property.
    @pyqtProperty(object, notify=imgAdded)
    def values(self):
        return self.listElem

    # Note that we need to explicitly emit() the signal. Declaring the
    # pyqtProperty with the notify=valueChanged above will have
    # benefits when we, for example, want to use this model in QML.
    @values.setter
    def values(self, newElems):
        for elem in newElems:
            self.listElem.append(elem)
        self.imgAdded.emit(newElems)  #emesso dopo che il valore è stato cambato

    def remove_imgs(self, items):
        imgs = [i.toolTip() for i in items]
        for elem in imgs:
            self.listElem.remove(elem)
        self.imgDel.emit(items)

    def remove_all_imgs(self):
        self.listElem = []
        self.imgDel.emit(1)
