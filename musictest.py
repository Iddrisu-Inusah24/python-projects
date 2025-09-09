import pygame

pygame.init()
pygame.mixer.init()

# Load and play a test sound
sound = pygame.mixer.Sound("Artifact - The Dark Contenent - Kevin MacLeod.wave")  # Make sure the file exists
sound.play()

input("Press Enter to exit...")  # Keeps the script running to hear the sound