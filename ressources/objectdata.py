from PIL import Image

def get_all_sprites():
    liste = []
    backgrounds = Image.open("./sprites/backgrounds.png")
    left, top, right, bottom = 0, 0, 32, 32
    for i in range(3):
        for j in range(13):
            liste.append(backgrounds.crop((left, top, right, bottom)))
            left += 32
            right += 32
        top += 32
        bottom += 32
        left, right = 0, 32
    
    checkpoints = Image.open("./sprites/checkpoints.png")
    left, top, right, bottom = 0, 0, 64, 64
    for j in range(4):
        liste.append(checkpoints.crop((left, top, right, bottom)))
        left += 32
        right += 32
    
    conveyors = Image.open("./sprites/conveyors.png")
    left, top, right, bottom = 0, 0, 32, 32
    for i in range(3):
        for j in range(13):
            liste.append(conveyors.crop((left, top, right, bottom)))
            left += 32
            right += 32
        top += 32
        bottom += 32
        left, right = 0, 32
