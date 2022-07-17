import game_lib.base as gb
import game_lib.item as gi
import pygame

from game_lib.particle import Particle

class Enemy(gb.Entity):
    def __init__(self,player,pos=[20,20]) -> None:
        super().__init__(pos=pos,size=[5,12],img="assets/player.png")
        # attributes
        self.data = gb.read_dat_file("devmode/enemy.dat")
        self.mleft = gb.string_to_bool(self.data["mleft"])
        self.mright = gb.string_to_bool(self.data["mright"])
        self.speed = int(self.data["speed"])
        self.pmovement = [0,0]
        self.scroll = player.scroll
        self.particles = []

        # weapon
        self.weapon = gi.Item()
        self.weapon.create_item(self,texpath="assets/weapons/sword.png")

        # gravity and jumping
        self.air_timer = 0
        self.y_momentum = int(self.data["ymomentum"])
        self.y_momentum_cap = 5
        self.jump_height = 4

        # debug
        self.debug_visible = False
    # draw
    def draw(self,surf: pygame.Surface) -> None:
        surf.blit(pygame.transform.flip(self.img,self.mleft,False),(self.rect.x-self.scroll[0],self.rect.y-self.scroll[1]))

        # displaying and updating weapon
        if self.mleft:
            self.weapon.pos = [self.rect.x-(self.rect.width)-self.scroll[0],self.rect.y-self.scroll[1]]
        elif self.mright:
            self.weapon.pos = [self.rect.x+(self.rect.width/2)-self.scroll[0],self.rect.y-self.scroll[1]]
        else:
            self.weapon.pos = [self.rect.x+(self.rect.width/2)-self.scroll[0],self.rect.y-self.scroll[1]]
        self.weapon.flip_x = self.mleft
        self.weapon.draw(surf)

    def movement(self,tiles) -> None:
        # movement
        self.pmovement = [0,0]
        if self.mleft:
            self.pmovement[0] -= 2
        if self.mright:
            self.pmovement[0] += 2

        # gravity
        self.pmovement[1] += self.y_momentum
        self.y_momentum += 0.2
        if self.y_momentum > self.y_momentum_cap:
            self.y_momentum = self.y_momentum_cap

        self.rect,collisions = self.move(tiles)
        # jump bug fixes
        if collisions["top"]:
            self.y_momentum = 0
        if collisions["bottom"]:
            self.y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

    # update
    def update(self,tiles: pygame.Rect,player) -> None:
        # update data
        newdata = gb.read_dat_file("devmode/enemy.dat")
        if newdata != self.data:
            for key in self.data:
                if newdata[key] != self.data[key]:
                    self.data[key] = newdata[key]
                    if key == "mleft":
                        self.mleft = gb.string_to_bool(self.data["mleft"])
                    elif key == "mright":
                        self.mright = gb.string_to_bool(self.data["mright"])
                    elif key == "speed":
                        self.speed = int(self.data["speed"])
                    elif key == "ymomentum":
                        self.y_momentum = int(self.data["ymomentum"])

        # movement
        self.scroll = player.scroll
        self.movement(tiles)

    def plane_collide_test(self,player):
        return gb.collision(self.rect,player.plane[0]+player.scroll[0],player.plane[1]+player.scroll[1],player.plane[2])

    def collision_test(self,tiles: pygame.Rect) -> list:
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def move(self, tiles: pygame.Rect) -> tuple:
        collision_types = {"top":False,"bottom":False,"right":False,"left":False}

        self.rect.x += self.pmovement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.pmovement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True

            elif self.pmovement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True

        self.rect.y += self.pmovement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.pmovement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True

            if self.pmovement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True

        return self.rect, collision_types