from observable import Observable
from PIL.ExifTags import GPSTAGS
import PIL.Image


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

    def upload_img(self, path_img):
        if type(path_img) != str:
            path_img = path_img.toolTip()
        exif = self.extract_exif_data(path_img)
        self.listPreviewImages.upload_img(path_img, exif)

    def previous_img(self):
        current_img = self.listPreviewImages.currentImg
        if current_img != None and current_img in self.listPreviewImages.values:  # TODO: qui volendo puoi impostare che venga selezionata l'imm dopo quando viene vcancellata una imm
            list = self.listPreviewImages.values
            indx_prev = (list.index(current_img) - 1) % len(list)
            prev_img = list[indx_prev]
            self.upload_img(prev_img)

    def next_img(self):
        current_img = self.listPreviewImages.currentImg
        if current_img != None and current_img in self.listPreviewImages.values:
            list = self.listPreviewImages.values
            indx_prev = (list.index(current_img) + 1) % len(list)
            prev_img = list[indx_prev]
            self.upload_img(prev_img)

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
