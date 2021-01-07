from observable import Observable
from PIL.ExifTags import GPSTAGS
import PIL.Image
import collections


class Model:
    def __init__(self):
        self.listPreviewImages = Observable()

    def observe(self, slot1, slot2, slot3):
        self.listPreviewImages.observe(slot1, slot2, slot3)

    def add_imgs(self, path_imgs):
        try:
            for img in path_imgs:
                if img in self.listPreviewImages.values:
                    print('image {} is already in the list'.format(img))
                    path_imgs.remove(img)
            self.listPreviewImages.values = path_imgs  # set
            if self.listPreviewImages.currentImg == None:
                self.upload_img(self.listPreviewImages.values[0])
        except:
            return

    def delete_AllImgs(self):
        self.listPreviewImages.remove_all_imgs()

    def delete_SelectedImgs(self, items):
        path_imgs_del = [i.toolTip() for i in items]
        if collections.Counter(path_imgs_del) == collections.Counter(self.listPreviewImages.values):
            print('deleted all imgs')
            return self.delete_AllImgs()
        current_img = self.listPreviewImages.currentImg
        if current_img in path_imgs_del:  # if the current img is deleted, upload the next img
            img_up = self.search_up_img(path_imgs_del[path_imgs_del.index(current_img):])
            self.upload_img(img_up)
        self.listPreviewImages.remove_imgs(path_imgs_del, items)

    def search_up_img(self, next_partial_imgs_del):
        # search the next uploaded image which is not deleted
        for img in next_partial_imgs_del:
            next = self.get_next_img(img)
            if next not in next_partial_imgs_del:
                return next

    def upload_img(self, path_img):
        if type(path_img) != str:
            path_img = path_img.toolTip()
        exif = self.extract_exif_data(path_img)
        self.listPreviewImages.upload_img(path_img, exif)

    def upload_previous_img(self):
        current_img = self.listPreviewImages.currentImg
        if current_img != None:
            prev_img = self.get_prev_img(current_img)
            self.upload_img(prev_img)
        else:
            pass

    def get_prev_img(self, current_img):
        list = self.listPreviewImages.values
        indx_prev = (list.index(current_img) - 1) % len(list)
        prev_img = list[indx_prev]
        return prev_img

    def upload_next_img(self):
        current_img = self.listPreviewImages.currentImg
        if current_img != None:
            next_img = self.get_next_img(current_img)
            self.upload_img(next_img)
        else:
            pass

    def get_next_img(self, current_img):
        list = self.listPreviewImages.values
        indx_next = (list.index(current_img) + 1) % len(list)
        next_img = list[indx_next]
        return next_img

    def extract_exif_data(self, path_img):
        try:
            img = PIL.Image.open(path_img)
            self.exif = {PIL.ExifTags.TAGS[k]: v
                         for k, v in img._getexif().items()
                         if k in PIL.ExifTags.TAGS}
            if 'GPSInfo' in self.exif.keys():
                latitude = str(self.getCoordinate(self.exif['GPSInfo'][2], self.exif['GPSInfo'][1]))
                longitude = str(self.getCoordinate(self.exif['GPSInfo'][4], self.exif['GPSInfo'][3]))
                self.exif['GPSInfo'] = "https://www.google.com/maps/search/?api=1&query=" + str(latitude) + "," + str(
                    longitude)
            return self.exif
        except:
            return None

    def getCoordinate(self, value, cardinal_point):
        d, m, s = value

        if cardinal_point in ['S', 'W']:
            d = -d
            m = -m
            s = -s

        return d + m / 60.0 + s / 3600.0


M = Model()
