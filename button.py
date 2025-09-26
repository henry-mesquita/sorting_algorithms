import pygame as pg

class Button:
    def __init__(
            self,
            text: str="Default Text",
            width: int=200,
            height: int=40,
            fontsize: int=30,
            pos: tuple[int, int]=(0, 0),
            screen: pg.Surface=None
        ) -> None:
        """
        Initialize the Button class.

        Args:
            text (str): The text to be displayed on the button. Default is "Default Text".
            width (int): The width of the button. Default is 200.
            height (int): The height of the button. Default is 40.
            fontsize (int): The font size of the text. Default is 30.
            pos (tuple[int, int]): The position of the button. Default is (0, 0).
            screen (pg.Surface): The surface to draw the button on. Default is None.
        Returns:
            None
        """
        # Main Attributes
        self.screen: pg.Surface = screen
        
        # Main Attributes
        self.pressed: bool = False
        self.font: pg.font.Font = pg.font.Font(None, fontsize)
        # Top rectangle
        self.top_rect: pg.Rect = pg.Rect((0, 0), (width, height))
        self.top_rect.center = pos
        self.active_color: str = "#1AEC07"
        self.not_active_color: str = "#AF1B22FF"
        # Text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    
    def draw(self, sorting: bool=False) -> None:
        """
        Draw the button on the screen.

        Args:
            sorting (bool): True if the button is active, False otherwise. Default is False.
        Returns:
            None
        """
        if sorting:
            pg.draw.rect(self.screen, self.not_active_color, self.top_rect)
        else:
            pg.draw.rect(self.screen, self.active_color, self.top_rect)

        self.screen.blit(self.text_surf, self.text_rect)
    
    def clicked(self) -> bool:
        """
        Check if the button has been clicked.

        Returns:
            bool: True if the button has been clicked, False otherwise.
        """
        mouse_pos: tuple[int, int] = pg.mouse.get_pos()
        mouse_pressed: tuple[bool, bool, bool] = pg.mouse.get_pressed()[0]
        if self.top_rect.collidepoint(mouse_pos):
            if mouse_pressed:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True
        else:
            self.pressed = False
        return False
