# Photo Date Game

Guess the date (and time) a photo was taken!

## Instructions

Clone this repo.

Open `folders.txt` and delete the text in it.

Add the complete path of each folder containing the images.

Each new folder must be on a new line.

The program will extract the path of every image inside the folder, including images nested in sub-folders. Hence, you do not need to add sub-folders.

The folders can contain files other than images - they will be ignored.

Run `main.py` to start the game.

## Cache

The code takes around 1 second to extract 100-200 images. For thousands of images, this can take some time.

You can choose to cache the image paths in the `cache` directory.

After extracting the images, you will be asked if you wish to cache the image paths in a file whose name you can set.

You will be asked to name the cache, so you can have multiple caches for different sets of images.

If the `cache` directory is present, the program will ask you at the start whether you wish to load the image paths from a particular cache.

Note: This only caches the image paths; not the images themselves. If you move the images from their location, those paths will become invalid. If you add new images to the directory, they will not be automatically added to the cache. You will have to re-read it and cache it from the start.