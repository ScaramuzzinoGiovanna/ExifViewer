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

    def upload_img(self, item, indx=None):
        self.listPreviewImages.upload_img(item, indx)

    def previous_img(self):
        # list = self.listPreviewImages.values
        # if not list:
        #     return
        current_img = self.listPreviewImages.currentImg
        if current_img != None:
            list = self.listPreviewImages.values
            indx_prev = (list.index(current_img) - 1) % len(list)
            prev_img = list[indx_prev]
            self.upload_img(prev_img, indx_prev)

    def next_img(self):
        current_img = self.listPreviewImages.currentImg
        if current_img != None:
            list = self.listPreviewImages.values
            indx_prev = (list.index(current_img) + 1) % len(list)
            prev_img = list[indx_prev]
            self.upload_img(prev_img, indx_prev)


M = Model()
