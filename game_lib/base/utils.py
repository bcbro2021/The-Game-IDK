import math

def load_map(path: str) -> list:
    game_map = []
    with open(path,"r") as file:
        data = file.readlines()
    for y in range(len(data)):
        row = []
        line = data[y].strip()
        tiles = line.split(",")
        for x in range(len(tiles)):
            row.append(tiles[x])
        game_map.append(row)

    return game_map

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def load_map_from_data(dat: str) -> list:
    game_map = []
    data = dat.split("\n")
    for y in range(len(data)):
        row = []
        line = data[y].strip()
        tiles = line.split(",")
        for x in range(len(tiles)):
            row.append(tiles[x])
        game_map.append(row)

    return game_map

def string_to_bool(dat: str) -> bool:
    if dat == "False":
        return False
    elif dat == "True":
        return True

def read_dat_file(filename: str) -> dict:
    data = {}
    with open(filename,"r") as file:
        filedata = file.readlines()
        for line in filedata:
            linedata = line.strip().split(",")
            data[linedata[0]] = linedata[1]
    return data

def collision(rect,center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rect.x + rect.width/2, rect.y + rect.height/2

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rect.x > cright or rbottom < ctop or rect.y > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rect.x, rect.x+rect.width):
        for y in (rect.y, rect.y+rect.height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rect.x <= center_x <= rright and rect.y <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected