import lib
import sys
import pygame

arguments = sys.argv
# print(arguments)
if len(arguments) != 3:
    raise RuntimeError("Not enough arguments. Require 2 arguments (Work time in minutes / Rest time in minutes)")

work_time = float(arguments[1])
rest_time = float(arguments[2])

pygame.init()
pygame.mixer.init()
pygame.font.init()

text_font = pygame.font.Font("font/3666-font.otf", 48)

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Pomodero Timer")

clock = pygame.time.Clock()
timer = lib.ui.PomoderoTimerUI(
    screen.get_width() - 80, 
    50, 
    5, 
    (255, 255, 255),
    2,
    (255, 105, 97),
    (193, 225, 193),
    (0, 0, 0),
    work_time,
    rest_time
)

running = True
timer.begin_rest_time()
while running:
    clock.tick(144)
    screen.fill((0, 0, 0))
    
    timer_text = text_font.render("Work time!" if timer.is_work_time() else "Rest time!", False, (255, 255, 255))
    screen.blit(timer_text, (screen.get_width() // 2 - timer_text.get_width() // 2, int((screen.get_height() // 2 - timer_text.get_height() // 2) - timer_text.get_height() * 1.25)))
    
    timer_surface = timer.draw_timer()
    screen.blit(timer_surface, (screen.get_width() // 2 - timer_surface.get_width() // 2, screen.get_height() // 2 - timer_surface.get_height() // 2))
    pygame.display.flip()
    
    
    timer.timer_update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            timer.stop_internal_timer()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                timer.stop_internal_timer()
                running = False
            if event.key == pygame.K_SPACE:
                timer.toggle_pause_timer()
            
    