from observable import Observable


class Model:
    def __init__(self):
        self.listPreviewImages = Observable('')

    def observe(self, slot1, slot2):
        self.listPreviewImages.observe(slot1, slot2)

    def add_img(self, path_img):
        path_img = path_img[0]
        self.listPreviewImages.values = path_img  # set

    def delete_AllImgs(self):
        # togliere imm visualizzata
        self.listPreviewImages.remove_all_imgs()

    def delete_SelectedImgs(self, items):
        # se è una delle imm che è visuallizata grande, allora devi toglierla pure da li
        self.listPreviewImages.remove_imgs(items)


M = Model()
