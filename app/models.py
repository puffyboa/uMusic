from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app, url_for, escape
import json

from app import app, db, basedir


class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Track(Base):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

    name = db.Column(db.String)
    path = db.Column(db.String, unique=True)

    image_path = db.Column(db.String, nullable=True)
    id3_genre = db.Column(db.String, nullable=True)
    id3_title = db.Column(db.String, nullable=True)
    id3_release_date = db.Column(db.String, nullable=True)

    @staticmethod
    def get_or_create(name, path):
        already_existing = Track.query.filter_by(
            name=name, path=path
        ).first()
        return already_existing if already_existing is not None else Track(name=name, path=path)

    def serialize(self):
        return {
            # 'id': self.id,
            # 'album_id': self.album_id,
            # 'artist_id': self.artist_id,
            # 'name': self.name,
            # 'path': self.path,
            # 'image_path': self.image_path,
            # 'id3_genre': self.id3_genre,
            # 'id3_title': self.id3_title,
            # 'id3_release_date': self.id3_release_date,

            'audio_url': url_for('main.play_track', track_id=self.id),
            'image_url': url_for('main.download_image', track_id=self.id)
        }


class Album(Base):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

    name = db.Column(db.String)

    tracks = db.relationship('Track', backref='album')

    @staticmethod
    def get_or_create(name):
        already_existing = Album.query.filter_by(
            name=name
        ).first()
        return already_existing if already_existing is not None else Album(name=name)


class Artist(Base):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True)

    albums = db.relationship('Album', backref='artist')
    tracks = db.relationship('Track', backref='artist')

    @staticmethod
    def get_or_create(name):
        already_existing = Artist.query.filter_by(
            name=name
        ).first()
        return already_existing if already_existing is not None else Artist(name=name)