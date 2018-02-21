import pygame
from pygame.locals import *

class IO:
    def __init__(self, memory):
        self.memory = memory
        pygame.init()
        self.window = pygame.display.set_mode((320, 240 + 20 + 20)) # Screen, lEDs, buttons
        self.window.fill(pygame.Color('black'))

    def display(self, screen):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[1] > 240 + 20:
                        idx = event.pos[0] // 10
                        self.memory.set(0x4004, ''.join([
                            bit if i != idx else ('0' if bit == '1' else '1')
                            for i, bit in enumerate(self.memory.get(0x4004))
                        ]))

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Screen
        if screen:
            # for x in range(320):
            #    for y in range(240):
            #        self.display_screen_pixel(x, y)
            address = self.memory.pop_updated_VRAM()
            if address is not None:
                self.display_screen_pixel(address=address)
        # lEDs
        for i, led in enumerate(self.memory.get(0x4000)):
            pygame.draw.circle(self.window, pygame.Color('green') if led == '1' else pygame.Color('red'), (10 * i + 5, 240 + 10), 4)
        # Buttons
        for i, button in enumerate(self.memory.get(0x4004)):
            pygame.draw.rect(self.window, pygame.Color('green') if button == '1' else pygame.Color('red'), (10 * i + 1, 240 + 20 + 1, 9, 9))
        pygame.display.flip()
        pass

    def display_screen_pixel(self, x=0, y=0, address=None):
        if address is None:
            address = 0x80000 + 4 * (y * 320 + x)
        else:
            x = ((address - 0x80000)/4) % 320
            y = ((address - 0x80000)/4) // 320
        color_bytes = self.memory.get(address)[16:32]
        red = color_bytes[0:5]
        green = color_bytes[5:11]
        blue = color_bytes[11:16]
        color = pygame.Color(
            int(int(red, 2) * 256 / 32),
            int(int(green, 2) * 256 / 64),
            int(int(blue, 2) * 256 / 32),
            0
        )
        pygame.draw.rect(self.window, color, (x, y, 1, 1))
