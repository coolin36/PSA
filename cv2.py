#!/usr/bin/env python3
from enum import Enum

class Medium_type(Enum):
    CD = 1
    DVD = 2
    LP = 3
    TAPE = 4
    DIGITAL = 5

class Genre(Enum):
    METAL = 1
    ROCK = 2
    HIPHOP = 3
    POP = 4
    BLUES = 5
    COUNTRY = 6
    JAZZ = 7
    CLASSICAL = 8

class Album():
    def __init__(self, title, artist, year, genre, track_no, medium_type):
        self._title = title
        self._artist = artist
        self._year = year
        self._genre = genre
        self._track_no = track_no
        self.medium_type = medium_type

    def print(self):
        print("| {0} | {1} | {2} | {3} | {4} | {5} |"
              .format(self._title,
                      self._artist,
                      self._year,
                      self._genre,
                      self._track_no,
                      self.medium_type))


class Album_library():
    def __init__(self):
        self._album_library_list = list()

    def init_data(self):
        self.add_album(Album("Reign in Blood", "Slayer", 1985, Genre.METAL, 10, Medium_type.LP))
        self.add_album(Album("Meteora", "Linkin Park", 2003, Genre.ROCK, 13, Medium_type.CD))
        self.add_album(Album("A Night at the Opera", "Queen", 1975, Genre.ROCK, 12, Medium_type.TAPE))

    def add_album(self, album : Album):
        self._album_library_list.append(album)

    def del_album(self, album : Album):
        self._album_library_list.remove(album)
    
    def find_album(self, search_string):
        for album in self._album_library_list:
            if search_string.lower() in album._title.lower():
                return album 
            if search_string.lower() in album._artist.lower():
                return album
        
        return None
    
    def print(self):
        print("|  Album Library vAlpha1  |")
        print("| ----------------------- |")
        for album in self._album_library_list:
            album.print()
        print("| ----------------------- |")
          

if __name__ == "__main__":
    
    library = Album_library()
    library.init_data()

    while True:
        print("------Menu-------")
        print("(1) print library")
        print("(2) add album")
        print("(3) remove album")
        print("(4) find album")
        print("(5) exit program")
        print("-----------------")
        choice = input("Enter your selection: ")

        if choice == "1":
            library.print()
            input("Press any key to continue.")
            continue
        elif choice == "2":
            print("To be implemented.")
            input("Press any key to continue.")
            continue
        elif choice == "3":
            string = input("Enter string to delete: ")
            album = library.find_album(string)
            album.print()
            confirm = input("Do you really want to remove the record (y/n): ")
            if confirm == "y":
                library.del_album(album)
            continue
        elif choice == "4":
            print("To be implemented.")
            input("Press any key to continue.")
            continue
        else:
            break