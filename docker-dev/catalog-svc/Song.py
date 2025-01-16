from functools import total_ordering
from datetime import datetime


@total_ordering
class Song:
    _id_counter = 1
    def __init__(self, title, artist, album, ):
        self.id = Song._id_counter
        self.title = title
        self.artist = artist
        self.album = album
        self.upload_time = datetime.now()
    
    def __str__(self):
        return f"Song: {self.title} by {self.artist}"
    
    def __repr__(self):
        return f"Song(id={self.id}, title={self.title}, artist={self.artist}, album={self.album}, upload_time={self.upload_time})"
    
    def __format__(self, format):
        format = format.lower()
        if format == "simple":
            return self.__str__()
        elif format == "variables":
            return self.__repr__()
        elif format == "redaction":
            return (f"Title: {self.title}\n"
                    f"Artist: {self.artist}\n"
                    f"Album: {self.album}\n"
                    f"Upload Time: {self.upload_time}")
    
    def __eq__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        return self.title == other.title and self.artist == other.artist
    
    def __gt__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        return self.title > other.title
    
    @classmethod
    def from_dictionary(cls, song_dict):
        return cls(song_dict['id'], song_dict['title'], song_dict['artist'], song_dict['album'], song_dict['upload_time'])
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'album': self.album,
            'upload_time': self.upload_time
        }

    
    
        