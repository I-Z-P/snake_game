#new game module

# libraries
import pygame
import sys
import random
import time

pygame.init()

#Rotating function
def rotate(texture, direction="up"):
    if direction == "left":
        surf = pygame.transform.rotate(texture,90)
    elif direction == "right":
        surf = pygame.transform.rotate(texture,270)
    elif direction == "down":
        surf = pygame.transform.rotate(texture,180)
    else:
        surf = texture
    return surf

#Corner rotating function
def rotate_corner(texture, previous_direction, new_direction):

    if (previous_direction == "up" and new_direction == "right") or (previous_direction == "left" and new_direction == "down"):
        surf = texture
    if (previous_direction == "up" and new_direction == "left") or (previous_direction == "right" and new_direction == "down"):
        surf = pygame.transform.rotate(texture, 270)
    if (previous_direction == "down" and new_direction == "right") or (previous_direction == "left" and new_direction == "up"):
        surf = pygame.transform.rotate(texture, 90)
    if (previous_direction == "down" and new_direction == "left") or (previous_direction == "right" and new_direction == "up"):
        surf = pygame.transform.rotate(texture, 180)

    try:
        return surf
    except:
        pass

#Snake printing and self colision detection function
def snake_body(head, body, body_direction, score=0):
    global screen, surface_body, surface_tail, direction, surface_corner, active_corners, change_direction, previous_direction
    #colision detection
    if head in body:
        print("game over")
        print("score: ",score)
        sys.exit(0)

    #body length
    if len(body) > score:
        del(body[0])

    #body direction
    body_direction[str(head)] = direction

    # #corners position and directions
    # if change_direction:
    #     surf = surface_corner
    #     surf = rotate_corner(surf, previous_direction, direction)
    #     active_corners[str(snake)] = surf
    #     change_direction = False

    #body printing
    for part in body:

        #Tail
        if part == body[0]:
            surf = surface_tail
            surf = rotate(surf, body_direction[str(part)])
                    
        #Corners
        elif str(part) in active_corners:
            surf = active_corners[str(part)]
            
        #Body
        else:
            surf = surface_body
            surf = rotate(surf, body_direction[str(part)])

        rect = surf.get_rect()
        rect.x = part.x
        rect.y = part.y

        #Pushing on screen
        screen.blit(surf,rect)
        
    #Previous values
    previous_direction = direction

    #Add new element
    body.append(pygame.Rect(head))

#Apple spawning and colision detection function
def apple_functions(head,apple):
    global screen, score

    #"is eaten" detection or first iteration
    if score == 1 or head == apple:
        score = score + 1
        spawn = True
    else:
        spawn = False

    #Apple spawning function
    while spawn:
        height = random.randint(0,1080)
        width = random.randint(0,1920)
        
        #Checking height and width to spawn apple at right place
        if height%40 == 0 and width%40 == 0:
            if height != 1080 and width != 1920:
                break
            else:
                continue
        else:
            continue

    #Apple returning
    surface_food = pygame.image.load("assets/apple.png")
    apple = surface_food.get_rect()
    apple.x = width
    apple.y = height
    return apple

#Main function
def run():

    #Tickrate values
    clock = pygame.time.Clock()
    delta = 0.0
    max_tps = 100

    #start variables
    global score
    global screen
    global direction
    global active_corners
    change_direction = False
    global previous_direction
    global previous_block
    global next_block
    global corner_rect
    active_corners = {}
    previous_direction = ""
    previous_block = pygame.Rect(960,560,40,40)
    corner_rect = pygame.Rect(960,560,40,40)
    y = 0
    x = 0
    body = []
    body_direction = {}
    direction = "None"
    score = 100
    first_game = True
    next_block = True

    #pygame variables
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
    apple = pygame.Rect(40,40,40,40)
    font = pygame.font.Font('freesansbold.ttf', 38)
    controls = pygame.image.load('assets/controls.png')
    surface_background = pygame.image.load("assets/game_background.png")
    rect_background = surface_background.get_rect()
    keys = None

    #textures variables
    global surface_body
    global body_texture
    global surface_tail
    global tail
    global surface_corner
    surface_food = pygame.image.load("assets/apple.png")
    surface_head = pygame.image.load("assets/head.png")
    snake = surface_head.get_rect()
    snake.x = 960
    snake.y = 560
    surface_body = pygame.image.load("assets/body.png")
    body_texture = surface_body.get_rect()
    surface_tail = pygame.image.load("assets/tail.png")
    tail = surface_tail.get_rect()
    surface_corner = pygame.image.load('assets/body_right.png')


    #Main loop
    while True:

        #Checking output keys to exit program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        #Tickrate
        delta += clock.tick()/1000.0
        while delta > 1 / max_tps:
            delta -= 1 / max_tps

            #Snake turning
            keys = pygame.key.get_pressed()

            if direction == "down" or direction == "up" or direction == "None":
                if keys[pygame.K_a]:
                    x = -40
                    y = 0
                    direction = "left"
                    change_direction = True
                    first_game = False
                    corner_rect = snake
                if keys[pygame.K_d]:
                    x = 40
                    y = 0
                    direction = "right"
                    change_direction = True
                    first_game = False
                    corner_rect = snake
            if direction == "left" or direction == "right" or direction == "None":
                if keys[pygame.K_w]:
                    y = -40
                    x = 0
                    direction = "up"
                    change_direction = True
                    first_game = False
                    corner_rect = snake
                if keys[pygame.K_s]:
                    y = 40
                    x = 0
                    direction = "down"
                    change_direction = True
                    first_game = False
                    corner_rect = snake

        #corners position and directions
        if change_direction:
            surf = surface_corner
            surf = rotate_corner(surf, previous_direction, direction)
            active_corners[str(snake)] = surf
            change_direction = False



        #New head position
        time.sleep(0.1)
        snake.y += y
        snake.x += x

        #Band colison detection
        if snake.x >= 1920:
            sys.exit(0)
        if snake.x < 0:
            sys.exit(0)
        if snake.y < 0:
            sys.exit(0)
        if snake.y >= 1080:
            sys.exit(0)

        #Background
        screen.blit(surface_background,rect_background)

        #Showing controls guide on first game
        if first_game:
            x = 0
            y = 0
            screen.blit(controls, (0,0))
        else:

            #Body drawing and self colision detection
            snake_body(snake,body,body_direction,score)

            #Head drawing
            surf = rotate(surface_head,direction)
            screen.blit(surf,snake)

            #Apple spawning and colision detection function
            try:
                apple = apple_functions(snake,apple)
            except:
                pass
            screen.blit(surface_food,apple)

            #Score printing
            score_counter = font.render("Score: " + str(score - 2), True, (255,255,255))
            screen.blit(score_counter, (100,60))

        #Frame printing
        pygame.display.flip()

# init function
if __name__ == "__main__":
    run()