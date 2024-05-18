from sqlalchemy.orm import DeclarativeBase

class Model(DeclarativeBase):
    pass

from .user import UserTable, UserTypeTable
from .country import CountryTable
from .song import SongTable, TagsTable,ListeningTable
from .album import AlbumTable, AlbumTypeTable
from .interactions import LikedSongsTable,RepostedSongsTable
from .interactions import LikedAlbumsTable,RepostedAlbumsTable