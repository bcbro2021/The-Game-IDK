import pygame
import game_lib.base as gb

# const
TILE_SIZE = 16

# assets
spritesheet = gb.load_image("assets/blocks.png")
grass_block = gb.load_image_at(spritesheet,(0,0,16,16))
dirt_block = gb.load_image_at(spritesheet,(16,0,16,16))
null_block = gb.load_image_at(spritesheet,(64,64,16,16))
stone_block = gb.load_image_at(spritesheet,(32,0,16,16))
mob_block = gb.load_image_at(spritesheet,(48,0,16,16))

# map
game_map = []

def map_rules(tile,dis,coords):
    if tile == "1":
        dis.blit(dirt_block,coords)
    elif tile == "2":
        dis.blit(grass_block,coords)
    elif tile == "3":
        dis.blit(stone_block,coords)
    elif tile == "4":
        dis.blit(mob_block,coords)
    elif tile != "0":
        dis.blit(null_block,coords)

def render_map(dis: pygame.Surface,player: gb.Entity,collidables: list,plane):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            coords = (x * TILE_SIZE-player.scroll[0],y * TILE_SIZE-player.scroll[1])
            tile = game_map[y][x]
            if gb.collision(pygame.Rect(coords[0],coords[1],TILE_SIZE,TILE_SIZE),plane[0],plane[1],plane[2]):
                map_rules(tile,dis,coords)
                if tile != "0":
                    collidables.append(pygame.Rect(x * TILE_SIZE,y * TILE_SIZE,TILE_SIZE,TILE_SIZE))