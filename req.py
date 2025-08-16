import subprocess

try:
    from PIL import Image
except ImportError:
    subprocess.run(["pip", "install", "pillow"])
    pillowExists = False

try:
    import pygame
    from pygame.locals import *
except ImportError:
    pygameExists = False

if not pillowExists:
    print("Pillow not found. Installing.")
    subprocess.run(["pip", "install", "pillow"])
if not pygameExists:
    print("Pygame not found. Installing.")
    subprocess.run(["pip", "install", "pygame"])