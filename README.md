# ExifViewer
EXIF metadata viewer of JPEG images.

_Mini project of human computer interaction course_.

# Installation
1. Clone this repository with:
```sh
git clone https://github.com/ScaramuzzinoGiovanna/ExifViewer.git
```
2. Prerequisites for run this code:
    * python 3.8.5 
    * pillow 8.0.1   
    * pyqt 5.9.2
   
   You can install these using pip or Anaconda

## Usage for the user

1. Run the script _main.py_ to open the GUI

# Functionality

The application allow you to:
1. __Add one or more images__ to be displayed directly in the GUI. The thumbnails of these images can be viewed in a list on the left.
2. __Delete__ all or some of the __images selected from the list__.
3. __View an image__ by selecting (with double click of the mouse) it from the list. By default the first image in the list is shown. This image can reach a __maximum size of 512 pixels__, with the resizing of the window.
5. The displayed image can be __rotated 90 degrees left and right__ using the central buttons below it.
6. The displayed image can also be __changed to the previous or next one__ in the list using the buttons on the right and left below it.
7. __View__ the __exif data__ of the image in a table on the right.
8. If an image has GPS geolocation tags (GPSInfo) in its EXIF tag set, the __link to open the GPS location on Google Maps__ is shown in the Data column.

**note: 1. 2. and 8. are the __extra features__ of the project: view multiple images and geolocalizaton.
