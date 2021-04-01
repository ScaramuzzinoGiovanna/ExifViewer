import collections

import PIL.Image
from PIL.ExifTags import GPSTAGS

from observable import Observable


class Model:
    def __init__(self):
        self.listImages = Observable()

    def observe(self, slot1, slot2, slot3):
        self.listImages.observe(slot1, slot2, slot3)

    def add_imgs(self, path_imgs):
        """ stores the images in the list """
        try:
            for img in path_imgs:
                if img in self.listImages.previews:
                    print('image {} is already in the list'.format(img))
                    path_imgs.remove(img)
            self.listImages.previews = path_imgs
            if self.listImages.current_img == None:
                self.upload_img(self.listImages.previews[0])
        except:
            return

    def delete_AllImgs(self):
        """ delete all the images"""
        self.listImages.remove_all_imgs()

    def delete_SelectedImgs(self, items):
        """ delete selected images"""
        path_imgs_del = [i.toolTip() for i in items]
        if collections.Counter(path_imgs_del) == collections.Counter(self.listImages.previews):
            print('deleted all imgs')
            return self.delete_AllImgs()
        current_img = self.listImages.currentImage
        if current_img in path_imgs_del:  # if the current img is deleted, upload the next img
            img_up = self.search_up_img(path_imgs_del[path_imgs_del.index(current_img):])
            self.upload_img(img_up)
        self.listImages.remove_imgs(path_imgs_del, items)

    def search_up_img(self, next_partial_imgs_del):
        """ search the next (not deleted) image in list to show it """
        for img in next_partial_imgs_del:
            next = self.get_next_img(img)  # if img is the last of the list the next returned is the first
            if next not in next_partial_imgs_del:
                return next

    def upload_img(self, path_img):
        """ stores the image to show with its exif data """
        if type(path_img) != str:
            path_img = path_img.toolTip()
        exif = self.extract_exif_data(path_img)
        self.listImages.upload_img(path_img, exif)

    def upload_previous_img(self):
        """ stores the previous image to shown """
        current_img = self.listImages.currentImage
        if current_img != None:
            prev_img = self.get_prev_img(current_img)
            self.upload_img(prev_img)
        else:
            pass

    def get_prev_img(self, current_img):
        """ returns the previous image of the current one """
        list = self.listImages.previews
        indx_prev = (list.index(current_img) - 1) % len(list)
        prev_img = list[indx_prev]
        return prev_img

    def upload_next_img(self):
        """ stores the next image in the list """
        current_img = self.listImages.currentImage
        if current_img != None:
            next_img = self.get_next_img(current_img)
            self.upload_img(next_img)
        else:
            pass

    def get_next_img(self, current_img):
        """ returns the next image of the current one """
        list = self.listImages.previews
        indx_next = (list.index(current_img) + 1) % len(list)
        next_img = list[indx_next]
        return next_img

    def extract_exif_data(self, path_img):
        """ extract the exif data from the image"""
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
        """ return latitude or longitude coordinate """
        d, m, s = value

        if cardinal_point in ['S', 'W']:
            d = -d
            m = -m
            s = -s

        return d + m / 60.0 + s / 3600.0


M = Model()
