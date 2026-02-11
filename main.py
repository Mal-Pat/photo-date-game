import os
import random
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import pickle

def get_folders(folder_paths_file):
    folder_paths = []
    with open(folder_paths_file, "r") as infile:
        for line in infile:
            folder_paths.append(line.strip())
    return folder_paths

def get_image_date(path):
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return None
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "DateTimeOriginal" or tag == "DateTime":
                    # Standard EXIF format is YYYY:MM:DD HH:MM:SS
                    return value
    except Exception:
        return None
    return None

def get_images(folder_paths):
    image_pool = []
    extensions = ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')
    for folder in folder_paths:
        if not os.path.exists(folder):
            print(f"Warning: Folder {folder} not found.")
            continue
        num = 0 
        for root, _, files in os.walk(folder):
            for file in files:
                num += 1
                if num%500 == 0:
                    print(f"{num} images loaded from {folder}")
                if file.endswith(extensions):
                    full_path = os.path.join(root, file)
                    date = get_image_date(full_path)
                    # Skip the image if missing date or other issues
                    if not date:
                        continue
                    image_pool.append((full_path, date))
    return image_pool

def write_cache(image_pool, cache_name):
    cache_path = f"cache/{cache_name}.pkl"
    if not os.path.exists("cache"):
        try:
            os.mkdir("cache")
        except OSError as e:
            print(f"Error creating directory cache: {e}")
    with open(cache_path, "wb") as outfile:
        pickle.dump(image_pool, outfile)

def read_cache(cache_name):
    cache_path = f"cache/{cache_name}.pkl"
    if not os.path.exists(cache_path):
        raise Exception(f"{cache_path} not found!")
    with open(cache_path, "rb") as infile:
        image_pool = pickle.load(infile)
    return image_pool

def ask_cache(image_pool):
    ans = input("Do you wish to cache the paths for quick loading next time? [y/n]: ")
    if ans != "n":
        cache_name = input("Name the cache file: ")
        write_cache(image_pool, cache_name)

def initiate(folder_paths_file):
    ans = input("Do you wish to read from cache? [y/n]: ")
    if ans == "Y" or ans == "y":
        cache_name = input("Name of cache file: ")
        image_pool = read_cache(cache_name)
        if not image_pool:
            raise Exception("No images found in the cache!")
    else:
        folder_paths = get_folders(folder_paths_file)
        image_pool = get_images(folder_paths)
        ask_cache(image_pool)
        if not image_pool:
            raise Exception("No images found in the folders!")
    return image_pool

def get_date_diff(date_str1, date_str2):
    """
    Takes two dates in EXIF format ('YYYY:MM:DD HH:MM:SS') 
    and returns the difference between them in days.
    """
    # The standard EXIF date format
    date_format = "%Y:%m:%d %H:%M:%S"
    try:
        # Convert strings to datetime objects
        dt1 = datetime.strptime(date_str1, date_format)
        dt2 = datetime.strptime(date_str2, date_format)
        # Calculate the absolute difference
        delta = abs(dt2 - dt1)  
        # Convert the total seconds of the difference into days
        days = delta.total_seconds() / (24*60*60)
        return days
    except ValueError as e:
        print(f"Format error: {e}. Ensure dates are in 'YYYY:MM:DD HH:MM:SS' format.")
        return None
    
def get_players_info():
    print("\n____________Enter Info____________")
    n = int(input("Number of players: "))
    if n <= 0:
        raise Exception("Number of players cannot be <= 0")
    players, wins, scores = {}, {}, {}
    for i in range(n):
        players[i+1] = input(f"Player {i+1}/{n}: ")
        wins[i+1] = 0
        scores[i+1] = 0
    return n, players, wins, scores

class PhotoGame:
    
    def __init__(self, folder_paths_file):
        self.image_pool = initiate(folder_paths_file)
        self.n, self.players, self.wins, self.scores = get_players_info()

    def get_random_image(self):
        img_path, img_date = random.choice(self.image_pool)
        print("Displaying image...")
        with Image.open(img_path) as img:
            img.show()
        return img_date
    
    def display_stats(self):
        print("\n______________Stats______________")
        scores_print, wins_print = "|", "|"
        for i in range(self.n):
            scores_print += f" {self.players[i+1]} : {round(self.scores[i+1], 2)} |"
            wins_print += f" {self.players[i+1]} : {self.wins[i+1]} |"
        print(f"\nWins: {wins_print}")
        print(f"\nScores: {scores_print}")

    def display_round_scores(self, diffs):
        sorted_diffs = sorted(diffs.items(), key = lambda item : item[1])
        diffs_print = "|"
        for key, value in sorted_diffs:
            diffs_print += f" {self.players[key]} : {round(value, 2)} |"
        print("\n___________Round Score___________")
        print(diffs_print)
    
    def game_round(self, r):
        print(f"\n_____________Round {r}_____________")
        img_date = self.get_random_image()
        guesses, diffs = {}, {}
        for i in range(self.n):
            while True:
              guesses[i+1] = input(f"{self.players[i+1]}'s guess: ")
              diffs[i+1] = get_date_diff(img_date, guesses[i+1])
              if diffs[i+1] == None:
                  print("Incorrect date format! It must be 'YYYY:MM:DD HH:MM:SS'. Try again: ")
                  continue
              break
            self.scores[i+1] += diffs[i+1]
        print("\n______________Answer______________")
        print(img_date)
        min_diff = min(diffs.values())
        winners = [key for key, value in diffs.items() if value == min_diff]
        for winner in winners:
            self.wins[winner] += 1
        self.display_round_scores(diffs)
        self.display_stats()
    
    def start_game(self):
        r = 1
        cont = "y"
        while cont != "n":
            self.game_round(r)
            r += 1
            cont = input(f"\nContinue to round {r}? [Y/n]: ")
        print("\n____________Game Ends_____________")

folder_paths_file = "folders.txt"
game = PhotoGame(folder_paths_file)
game.start_game()