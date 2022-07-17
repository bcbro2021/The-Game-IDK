import pygame, sys, os, socket
import game_lib.base as gb
import game_lib.lights as gl
from pygame.locals import *
pygame.init()

# CONST
USERNAME = sys.argv[1]
MAX_FPS = 60
WIN_SIZE = (800,600)
WIN_TITLE = f"Game IDK! - {sys.argv[1]}"
SAVES_FOLDER = "saves/"
filename = f"{SAVES_FOLDER}save.gm"

# window and init stuff
clock = pygame.time.Clock()
win = gb.Window(WIN_SIZE,WIN_TITLE).return_window()
dis_size = [(WIN_SIZE[0]//2),(WIN_SIZE[1]//2)]
zoomed_size = [(WIN_SIZE[0]//2)/2,(WIN_SIZE[1]//2)/2]
zoomed = False
dis = pygame.Surface(dis_size)
mode = "mainmenu"
bg_color = [0,0,0]
# variables
selected_id = "1"
stg_btn = gb.Entity(pos=[10,570],size=[20,20])

# events
def quitev(event: pygame.event.Event) -> None:
    pygame.quit()
    sys.exit()
def zoomev(event: pygame.event.Event) -> None:
    global dis_size
    global zoomed
    if event.key == pygame.K_z:
        if zoomed:
            dis_size = [400,300]
            zoomed = False
        else:
            dis_size = [200,150]
            zoomed = True

## main menu mode
Title = gb.Text("A GAME!",(0,255,0),(0,0,0),60,[WIN_SIZE[0]//2,100])
play_btn = gb.Text("Play",(255,255,255),(0,0,0),20,[WIN_SIZE[0]//2,200])
edit_btn = gb.Text("Edit",(255,255,255),(0,0,0),20,[WIN_SIZE[0]//2,230])
mulplay_btn = gb.Text("Multiplay",(255,255,255),(0,0,0),20,[WIN_SIZE[0]//2,260])

## level select mode
list_title = gb.Text("LEVEL SELECT",(0,255,0),(0,0,0),50,[WIN_SIZE[0]//2,100])
## map list
enable_map_list = False
map_type = "game"
maplist = os.listdir("saves/")
mapbtns = []
for i in range(len(maplist)):
    maptxt = gb.Text(maplist[i].split(".gm")[0],(255,255,255),(0,0,0),20,[WIN_SIZE[0]//2,i*30+200])
    mapbtn = gb.Entity(pos=maptxt.pos)
    mapbtn.rect = maptxt.textRect
    mapbtns.append((maptxt,mapbtn))
create_map_btn = gb.Text("Create",(255,255,255),(0,0,0),10,[30,590])
print(maplist)

## play mode
# player entity
import game_lib.player as glp
player = glp.Player()
# test enemy
import game_lib.enemy as gle
enemies = []

# player lighting
darkness_surf = pygame.Surface((400,300))
darkness_surf.fill((0,0,0))
player_light = gl.round_light(5,player.plane[2]).create()
# blit them
darkness_surf.blit(player_light,(((darkness_surf.get_width()/2)/2)/2,player.plane[1]))

# gui stuff
pause_btn = gb.Entity(pos=[0,0],size=[16,16],img="assets/GUI/exitmain.png")

## edit mode
class Tile(gb.Entity):
    def __init__(self, x,y,w,h) -> None:
        super().__init__(pos=(x,y), size=(w,h), img="none")
        self.index = (0,0)
        self.id = "0"

def save_map():
    global grid, filename
    
    data = ""
    for y in range(len(grid)):
        row = ""
        for x in range(len(grid[y])):
            if len(grid[y]) - 1 == x:
                row += grid[y][x].id
            else:
                row += grid[y][x].id + ","
        row += "\n"
        data += row
    with open(filename,"w") as file:
        file.write(data)

# grid
grid = []
def create_grid():
    global grid, filename
    with open(filename,"r") as file:
        data = file.readlines()
        for i in range(len(data)):
            line = data[i].strip().split(",")
            newline = ""
            for tile in line:
                newline = newline + tile
            data[i] = newline

    for y in range(WIN_SIZE[1]//16):
        row = []
        for x in range(WIN_SIZE[0]//16):
            tile = Tile(x*16,y*16,16,16)
            tile.index = (x,y)
            tile.id = data[y][x]
            row.append(tile)
        grid.append(row)

# multiplayer
def start_client():
    HOST = '127.0.0.1'
    PORT = 5000

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    player_2 = gb.Entity(pos=[0,0],size=[5,12],img="assets/player.png")

    return client, player_2
client = None
player_2 = None
player_2_name = gb.Text("player_name",(255,255,255),(0,0,0),5,[0,0])

# game loop
import game_lib.world as glw
glw.game_map = gb.load_map(filename)

# modes
def main_menu_mode():
    # globals
    global map_type
    global mode
    global player_2

    win.fill(bg_color)
    # rendering
    Title.draw(win)
    play_btn.draw(win)
    edit_btn.draw(win)
    mulplay_btn.draw(win)

    # events
    for event in pygame.event.get():
        gb.quit_event(event,quitev)

        # switch to play mode
        if play_btn.clicked_on(event):
            map_type = "game"
            mode = "maplist"

        # switch to edit mode
        if edit_btn.clicked_on(event):
            map_type = "edit"
            mode = "maplist"
        
        # switch to multiplayer mode
        if mulplay_btn.clicked_on(event):
            client, player_2 = start_client()
            waittext = gb.Text("Waiting for other clients!",(255,255,255),(0,0,0),30,([WIN_SIZE[0]//2,560]))
            waittext.draw(win)
            map_data = client.recv(2048*2).decode()
            # change map to server map
            glw.game_map = gb.load_map_from_data(map_data)
            mode = "multigame"
def map_list_mode():
    global mode
    global filename

    win.fill(bg_color)
    # rendering title
    list_title.draw(win)
    # rendering buttons
    for i in range(len(mapbtns)):
        mapbtns[i][0].draw(win)
    if map_type == "edit":
        create_map_btn.draw(win)

    for event in pygame.event.get():
        gb.quit_event(event, quitev)
        if create_map_btn.clicked_on(event):
            if map_type == "edit":
                filename = f"{SAVES_FOLDER}empty.gm"
                create_grid()
                glw.game_map = gb.load_map(filename)
                Input = input("world name>>")
                filename = f"{SAVES_FOLDER}{Input}.gm"
                mode = "edit"
        # actual switching
        for i in range(len(mapbtns)):
            if mapbtns[i][1].clicked_on(event):
                if map_type == "game":
                    filename = f"{SAVES_FOLDER}{mapbtns[i][0].text}.gm"
                    glw.game_map = gb.load_map(filename)
                    for y in range(len(glw.game_map)):
                        for x in range(len(glw.game_map[y])):
                            if glw.game_map[y][x] == "4":
                                newenemy = gle.Enemy(player,pos=[x * 16,y * 16 - 16])
                                enemies.append(newenemy)
                    mode = "game"
                if map_type == "edit":
                    filename = f"{SAVES_FOLDER}{mapbtns[i][0].text}.gm"
                    create_grid()
                    glw.game_map = gb.load_map(filename)
                    mode = "edit"
def edit_mode():
    # globals
    global mode
    global selected_id

    win.fill(bg_color)
    # rendering
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            tile = grid[y][x]
            glw.map_rules(tile.id,win,(tile.rect.x,tile.rect.y))

    stg_btn.draw(win)
    # current block
    glw.map_rules(selected_id,win,(780,580))

    # changer id
    print(selected_id)

    # events
    for event in pygame.event.get():
        gb.quit_event(event,quitev)
        if event.type == KEYDOWN:
            # saving map
            if event.key == K_s:
                save_map()

        # block picker
        if event.type == MOUSEWHEEL:
            id = int(selected_id)
            if event.y == -1:
                id += 1
                selected_id = str(id)
            elif event.y == 1:
                id -= 1
                selected_id = str(id)

        # editing block
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x].clicked_on(event):
                    grid[y][x].id = selected_id
        
        # switch to game
        if stg_btn.clicked_on(event):
            save_map()
            glw.game_map = gb.load_map(filename)
            mode = "game"
def game_mode():
    # globals
    global mode

    dis.fill(bg_color)
    # rendering
    collidables = []
    glw.render_map(dis,player,collidables,player.plane)

    for enemy in enemies:
        if enemy.plane_collide_test(player):
            enemy.draw(dis)
    player.draw(dis)
    # player lighting
    dis.blit(darkness_surf,(0,0),special_flags=pygame.BLEND_RGB_MULT)
    

    # events
    for event in pygame.event.get():
        gb.quit_event(event,quitev)

        gb.keydown_event(event,player.keydownev)
        gb.keydown_event(event,zoomev)
        gb.keyup_event(event,player.keyupev)
        
        # pause button
        if pause_btn.clicked_on(event):
            player.rect.x = player.pos[0]
            player.rect.y = player.pos[1]
            for enemy in enemies:
                enemy.rect.x = enemy.pos[0]
                enemy.rect.y = enemy.pos[1]
            mode = "mainmenu"

    # updating
    player.update(dis,collidables,dis_size)
    for enemy in enemies:
        if enemy.plane_collide_test(player):
            enemy.update(collidables,player)

    # GUI rendering
    pause_btn.draw(dis)

    surf = pygame.transform.scale(dis,WIN_SIZE)
    win.blit(pygame.transform.flip(surf,False,False),(0,0))
    clock.tick(MAX_FPS)
def multiplayer_mode():
    # globals
    global mode

    client.send(f"{USERNAME}:{str(player.rect.x)},{str(player.rect.y)}\n".encode())
    data = client.recv(256).decode().strip()
    print(data)
    player_2.rect.x = int(data.split(":")[1].split(",")[0])
    player_2.rect.y = int(data.split(":")[1].split(",")[1])
    player_2_name.text = data.split(":")[0]
    player_2_name.pos = [player_2.rect.x-player.scroll[0]+((player_2_name.textRect.width//2)//2),player_2.rect.y-player.scroll[1]-5]
    player_2_name.update()

    # game
    dis.fill(bg_color)
    # rendering
    
    dis.blit(player_2.img,(player_2.rect.x-player.scroll[0],player_2.rect.y-player.scroll[1]))

    collidables = []
    glw.render_map(dis,player,collidables,player.plane)
    player_2_name.draw(dis)
    player.draw(dis)
            
    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            client.close()
            mode = "mainmenu"

        gb.keydown_event(event,player.keydownev)
        gb.keydown_event(event,zoomev)
        gb.keyup_event(event,player.keyupev)
        
        # pause button
        if pause_btn.clicked_on(event):
            player.rect.x = player.pos[0]
            player.rect.y = player.pos[1]
            client.close()
            mode = "mainmenu"
    # updating
    player.update(dis,collidables,dis_size)

    # GUI rendering
    if player.debug_visible:
        player.pos_dis.draw(dis)
    pause_btn.draw(dis)

    surf = pygame.transform.scale(dis,WIN_SIZE)
    win.blit(pygame.transform.flip(surf,False,False),(0,0))
    clock.tick(MAX_FPS)

while True:
    dis = pygame.Surface(dis_size)
    ######### MAIN MENU
    if mode == "mainmenu":
        main_menu_mode()

    ######## MAP LIST MODE
    if mode == "maplist":
        map_list_mode()

    ######## EDIT MODE
    elif mode == "edit":
        edit_mode()

    ######## GAME MODE
    elif mode == "game":
        game_mode()

    ###### MULTIPLAYER
    elif mode == "multigame":
        multiplayer_mode()

    # window updates
    pygame.display.update()