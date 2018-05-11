import configparser

config = configparser.ConfigParser()
config.read('config.ini')

gameconfig = config['GAME']
LIMIT_FPS = gameconfig.getint('LIMIT_FPS')

windowconfig = config['WINDOW']
SCREEN_WIDTH = windowconfig.getint('SCREEN_WIDTH')
SCREEN_HEIGHT = windowconfig.getint('SCREEN_HEIGHT')

mapconfig = config['MAP']
MAP_WIDTH = mapconfig.getint('MAP_WIDTH')
MAP_HEIGHT = mapconfig.getint('MAP_HEIGHT')

roomsconfig = config['ROOMS']
ROOM_MAX_SIZE = roomsconfig.getint('ROOM_MAX_SIZE')
ROOM_MIN_SIZE = roomsconfig.getint('ROOM_MIN_SIZE')
MAX_ROOMS = roomsconfig.getint('MAX_ROOMS')

fovconfig = config['FOV']
FOV_ALGO = fovconfig['FOV_ALGO']
FOV_LIGHT_WALLS = fovconfig.getboolean('FOV_LIGHT_WALLS')
TORCH_RADIUS = fovconfig.getint('TORCH_RADIUS')