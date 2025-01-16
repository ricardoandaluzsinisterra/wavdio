from functools import total_ordering
from datetime import datetime


@total_ordering
class Song:
    _id_counter = 1
    
    def __init__(self, title, author, album, upload_time=None):
        self.title = title
        self.author = author
        self.album = album
        self.upload_time =  datetime.now()
    
    def __str__(self):
        return f"Song: {self.title} by {self.author}"
    
    def __repr__(self):
        return f"Song(title={self.title}, author={self.author}, album={self.album}, upload_time={self.upload_time})"
    
    def __format__(self, format):
        format = format.lower()
        if format == "simple":
            return self.__str__()
        elif format == "variables":
            return self.__repr__()
        elif format == "redaction":
            return (f"Title: {self.title}\n"
                    f"Author: {self.author}\n"
                    f"Album: {self.album}\n"
                    f"Upload Time: {self.upload_time}")
    
    def __eq__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        return self.title == other.title and self.author == other.author
    
    def __gt__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        return self.title > other.title
    
    @classmethod
    def from_dictionary(cls, song_dict):
        try:
            upload_time = datetime.fromisoformat(song_dict['upload_time']) if 'upload_time' in song_dict else None
            song = cls(
                title=song_dict['title'],
                author=song_dict['author'],
                album=song_dict['album'],
                upload_time=upload_time
            )
            return song
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid value for field: {e}")
    
    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'album': self.album,
            'upload_time': self.upload_time.isoformat()
        }
