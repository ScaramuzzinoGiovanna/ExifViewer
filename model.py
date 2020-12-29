from observable import Observable


class Model:
    def __init__(self):
        self.listPreviewImages = Observable()

    def observe(self, slot1, slot2, slot3):
        self.listPreviewImages.observe(slot1, slot2, slot3)

    def add_img(self, path_img):
        path_img = path_img[0]
        self.listPreviewImages.values = path_img  # set

    def delete_AllImgs(self):
        self.listPreviewImages.remove_all_imgs()

    def delete_SelectedImgs(self, items):
        self.listPreviewImages.remove_imgs(items)

    def upload_img(self, item):
        self.listPreviewImages.upload_img(item)


M = Model()
