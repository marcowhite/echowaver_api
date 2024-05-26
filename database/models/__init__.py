from sqlalchemy.orm import DeclarativeBase

class Model(DeclarativeBase):
    pass

from .user import UserTable, UserRoleTable
from .country import CountryTable
from .song import SongTable, SongTagTable,SongListenTable
from .album import AlbumTable, AlbumTypeTable
from .interactions import LikedSongTable,RepostedSongTable
from .interactions import LikedAlbumTable,RepostedAlbumTable