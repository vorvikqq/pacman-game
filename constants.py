TILEWIDTH = 20
TILEHEIGHT = 20
NROWS = 36
NCOLS = 28
SCREENWIDTH = NCOLS * TILEWIDTH
SCREENHEIGHT = NROWS * TILEHEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

BLACK = (0,0,0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
#temp colors for painting ghosts
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

PACMAN = 0
GHOST = 3

PELLET = 1
POWERPELLET = 2
PORTAL = 3

CHASE = "CHASE"
SCATTER = "SCATTER"
WAIT = "WAIT"