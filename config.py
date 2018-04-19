#file config
import os

class Config:
    CRSF_ENABLED = True
    SECRET_KEY = 'hihi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmenConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/magicshop'
    DEBUG = True

config = {
    'development':DevelopmenConfig,
    'default':DevelopmenConfig
}