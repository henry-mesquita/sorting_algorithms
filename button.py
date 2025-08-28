import pygame as pg

class Button:
    def __init__(self, text, width, height, fontsize, pos, screen):
        self.screen = screen
        
        # Main Attributes
        self.pressed = False
        self.font = pg.font.Font(None, fontsize)
        # Top rectangle
        self.top_rect = pg.Rect((0, 0), (width, height))
        self.top_rect.center = pos
        self.active_color = "#1AEC07"
        self.not_active_color = "#AF1B22FF"
        # Text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    
    def draw(self, sorting):
        if sorting:
            pg.draw.rect(self.screen, self.not_active_color, self.top_rect)
        else:
            pg.draw.rect(self.screen, self.active_color, self.top_rect)

        self.screen.blit(self.text_surf, self.text_rect)
    
    def clicked(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.top_rect.collidepoint(mouse_pos):
            if mouse_pressed:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True
        else:
            self.pressed = False
        return False
