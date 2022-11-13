import pygame
import io
import keyboard

def play(song: bytes) -> None:
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(io.BytesIO(song))
    clock = pygame.time.Clock()
    sound.play()
    
    while pygame.mixer.get_busy():
        clock.tick(1000)
        if keyboard.is_pressed('q'):
            sound.stop()