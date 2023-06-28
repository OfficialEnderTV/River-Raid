from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import time

app=Ursina(development_mode=True)
window.fullscreen=True

#---------------------------HUD-----------------------#
hud=Entity(model="quad", color=rgb(142,142,142), parent=camera.ui, scale=(1.274, .2), origin=(0, 2))
hud_outline=Entity(model="quad", color=color.black, parent=hud, scale=(1, .03), position=(0, -1.5))
logo=Entity(model="quad", texture="resources/hud/activision.png", scale=(0.2, .3), position=(0.03, -2.35), parent=hud)
fuel_meter=Entity(model="quad", texture="resources/hud/fuel/fuel.png", parent=hud, scale=(.25, .25), position=(0, -2.1))
fuel_check=Entity(model="quad", texture="resources/hud/fuel/fuelcheck.png", parent=fuel_meter, scale=(.05, .67), position=(.4, -0.1))
border1=Entity(model="quad", color=color.black, position=(6.722,0), scale=(3, 10))
border2=Entity(model="quad", color=color.black, position=(-6.722,0), scale=(3, 10))
lives=Entity(model="quad", texture="resources/hud/numbers/three.png", scale=(.032, .15), position=(-0.11, -2.37), parent=hud)

#--------------------------player---------------------#
plane=PlatformerController2d(model="quad", texture="resources/player/player.png", color=color.white, scale=(.6, .55), collider="box", visible=False)

#---------------------shoting---------------------#
shot_delay = .3
last_shot_time=0
def shot():
    global last_shot_time
    current_time=time.time()
    if current_time - last_shot_time >= shot_delay:
        bullet = Entity(y=plane.y + 0.5, x=plane.x, model="quad", texture="resources/player/bullet.png", scale=(0.128, 0.25))
        print("created new bullet object")
        bulletray = raycast(origin=(bullet.x, bullet.y), direction=(0,0.0001,0), distance=2, ignore=[plane, map], debug=True)
        print("created new bulletray")
        bullet.animate_y(60, duration=8, curve=curve.linear)
        print("moving bullet from player position")
        invoke(destroy_bullet, bullet, delay=.7)
        invoke(destroy_bulletray, bulletray, delay=.15)
        last_shot_time = current_time
        print("creating delay")
def destroy_bullet(bullet):
    destroy(bullet)
    print("destroyed bullet")
def destroy_bulletray(bulletray):
    destroy(bulletray)
    print("destroyed bulletray")

#------------------UPDATE------------------#
def update():
    #change player sprite and speed bugfix
    if held_keys["a"] and held_keys["d"]:
        plane.velocity=.3
        plane.texture="resources/player/player.png"
    if held_keys["a"]:
        plane.texture="resources/player/playerleft.png"
        plane.velocity=-.3
    if not held_keys["a"] and not held_keys["d"]:
        plane.texture="resources/player/player.png"
        plane.velocity=0
    if held_keys["d"]:
        plane.texture="resources/player/playerright.png"
        plane.velocity=.3

    #shoting
    if held_keys["space"]:
        shot()

    #starting game
    if held_keys["enter"]:
        #plane visibility
        plane.position=0, -1
        plane.visible=True

        #object moving
        map.animate_y(60, duration=250, curve=curve.linear)
        fuel_tank.animate_y(-60, duration=100, curve=curve.linear)
        ship.animate_y(-60, duration=100, curve=curve.linear)

        #hud element
        fuel_check.animate_x(-60, duration=2500, curve=curve.linear)

    ray1=raycast(origin=(plane.x-.245, plane.y), direction=(90,0,0), distance=.5, ignore=[plane,], traverse_target=fuel_tank)
    
    fuel_tank_explosion=raycast(origin=(fuel_tank.x-.218, fuel_tank.y-.37), direction=(90,0,0), distance=.4)
    fuel_tank_explosion_wall1=raycast(origin=(fuel_tank.x-.218, fuel_tank.y-.37), direction=(0,0.0001,0), distance=.7)
    fuel_tank_explosion_wall2=raycast(origin=(fuel_tank.x+.218, fuel_tank.y-.37), direction=(0,0.0001,0), distance=.7)

    if ray1.hit:
        print("tanking the plane...")
    if fuel_tank_explosion.hit:
        ship.texture="resources/explosions/shipexplode1.png"
        plane.texture="resources/explosions/playerexplode.png"
    if fuel_tank_explosion_wall1:
        plane.velocity=0
        plane.texture="resources/explosions/playerexplode.png"
        ship.texture="resources/explosions/shipexplode1.png"
    if fuel_tank_explosion_wall2:
        plane.velocity=0
        plane.texture="resources/explosions/playerexplode.png"
        ship.texture="resources/explosions/shipexplode1.png"

#---------------------------MAP-----------------------#
bg=Entity(model="quad", color=rgb(45, 50, 184), scale=(40, 8000), position=(0, -1, 1))
map=Entity(model="quad", texture="resources/map.png", collider="resources/map", scale_x=10.4375, scale_y=483.9375, y=217)
fuel_tank=Entity(model="quad", texture="resources/interactive/fueltank.png", scale=(1.4, .3), position=(-.2, 2), visible=False)
ship=Entity(model="quad", texture="resources/enemy/ship.png", scale=(1.4, .3), position=(-.2, 2))

app.run()

#fuel_tank.scale=(.45, .75)