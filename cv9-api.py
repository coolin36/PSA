#!/usr/bin/env python3
from enum import Enum
from flask import Flask, request

APP = Flask(__name__)


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
    def __init__(self, id, title, artist, year, genre, track_no, medium_type):
        self._id = id
        self._title = title
        self._artist = artist
        self._year = year
        self._genre = genre
        self._track_no = track_no
        self._medium_type = medium_type

    def print(self):
        print("| {0} | {1} | {2} | {3} | {4} | {5} |"
              .format(self._title,
                      self._artist,
                      self._year,
                      self._genre,
                      self._track_no,
                      self._medium_type))
        
    def serialize(self):
        return {"id": self._id,
                "title": self._title,
                "artist": self._artist,
                "year": self._year,
                "genre": self._genre.value,
                "track_no": self._track_no,
                "medium_type": self._medium_type.value}


class Album_library():
    def __init__(self):
        self._album_library_list = list()
        self._last_id = 0

    def init_data(self):
        self.create_album("Reign in Blood", "Slayer", 1985, Genre.METAL, 10, Medium_type.LP)
        self.create_album("Meteora", "Linkin Park", 2003, Genre.ROCK, 13, Medium_type.CD)
        self.create_album("A Night at the Opera", "Queen", 1975, Genre.ROCK, 12, Medium_type.TAPE)

    def create_album(self, title, artist, year, genre, track_no, medium_type):
        self._last_id += 1
        id = self._last_id
        album = Album(id, title, artist, year, genre, track_no, medium_type)
        self._album_library_list.append(album)
        return album

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

    def get_albums(self):
        out = list()
        for album in self._album_library_list:
            out.append(album.serialize())
        return out
    
    def get_album(self, id):
        for album in self._album_library_list:
            if id == album._id:
                return album
        return None
          

def menu():
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

LIBRARY = Album_library()
LIBRARY.init_data()

@APP.route("/")
def index():    
    return "Hello from Album Library."

@APP.route("/api/albums")
def get_albums():
    return LIBRARY.get_albums()

@APP.route("/api/albums/<int:id>")
def get_album(id):
    album = LIBRARY.get_album(id)
    if album != None:
        return album.serialize()
    else:
        return '{"error": "ID not found."}', 404
    
@APP.route("/api/albums/<int:id>", methods=["DELETE"])
def delete_album(id):
    album = LIBRARY.get_album(id)
    if album != None:
        LIBRARY.del_album(album)
        return album.serialize()
    else:
        return '{"error": "ID not found."}', 404
    
@APP.route("/api/albums", methods=["POST"])
def create_album():
    dict_album = request.get_json()
    #TODO validate if all keys are present in json request
    album = LIBRARY.create_album(dict_album["title"],
                         dict_album["artist"],
                         dict_album["year"],
                         Genre(dict_album["genre"]),
                         dict_album["track_no"],
                         Medium_type(dict_album["medium_type"]))
    return album.serialize(), 201




if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)