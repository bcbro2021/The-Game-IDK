import game_lib.base as gb
import game_lib.item as gi
import game_lib.lights as gl
import pygame

from game_lib.particle import Particle

class Player(gb.Entity):
    def __init__(self) -> None:
        super().__init__(pos=[20,20],size=[5,12],img="assets/player.png")
        # attributes
        self.mleft = False
        self.mright = False
        self.speed = 5
        self.pmovement = [0,0]
        self.air_timer = 0
        self.scroll = [0,0]
        self.particles = []
        # basic lighting
        self.plane = [self.rect.x/2,self.rect.y/2,150]

        # weapon
        self.weapon = gi.Item()
        self.weapon.create_item(self,texpath="assets/weapons/sword.png")

        # gravity and jumping
        self.y_momentum = 0
        self.y_momentum_cap = 5
        self.jump_height = 4

        # debug
        self.debug_visible = False
        self.pos_dis = gb.Text(f"{self.rect.x},{self.rect.y}",(20,255,20),(0,0,0),10,[30,10])
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

    def movement(self,tiles,dis_size) -> None:
        # movement
        self.scroll[0] += (self.rect.x-self.scroll[0]-(dis_size[0]/2))
        self.scroll[1] += (self.rect.y-self.scroll[1]-(dis_size[1]/2))

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
        
        # wall jump
        if self.air_timer > 0:
            if collisions["left"] or collisions["right"]:
                self.air_timer = 0

    # update
    def update(self,dis: pygame.Surface,tiles: pygame.Rect,dis_size) -> None:
        # particles
        self.particles.append(Particle(pos=[self.rect.x+2-self.scroll[0],self.rect.y-self.scroll[1]+1],size=[1,1],color=(200,100,100)))
        for particle in self.particles:
            particle.draw(dis)
            particle.update()
            if particle.kill:
                self.particles.remove(particle)

        self.movement(tiles,dis_size)
        self.plane[0] = (self.rect.x)-self.scroll[0]
        self.plane[1] = (self.rect.y)-self.scroll[1]
        self.pos_dis.text = f"{self.rect.x},{self.rect.y}"
        self.pos_dis.update()

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

    # events
    def keydownev(self,event: pygame.event.Event) -> None:
        if event.key == pygame.K_a:
            self.mleft = True
        if event.key == pygame.K_d:
            self.mright = True
        if event.key == pygame.K_F3:
            if self.debug_visible:
                self.debug_visible = False
            else:
                self.debug_visible = True
        if event.key == pygame.K_SPACE:
            if self.air_timer < 20:
                self.y_momentum = -self.jump_height
    def keyupev(self,event: pygame.event.Event) -> None:
        if event.key == pygame.K_a:
            self.mleft = False
        if event.key == pygame.K_d:
            self.mright = False