from functools import total_ordering


@total_ordering
class Song:
    def __init__(self, id, title, artist, album, genre, release_year):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.release_year = release_year
    
    def __str__(self):
        return f"Song: {self.title} by {self.artist}"
    
    def __repr__(self):
        return f"Song(id={self.id}, title={self.title}, artist={self.artist}, album={self.album}, genre={self.genre}, release_year={self.release_year})"
    
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
                    f"Genre: {self.genre}\n"
                    f"Release Year: {self.release_year}")
    
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
        return cls(song_dict['id'], song_dict['title'], song_dict['artist'], song_dict['album'], song_dict['genre'], song_dict['release_year'])
    
    
        