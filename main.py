import pygame as pg
from constants import *
from button import Button
from random import shuffle
from time import time
from config_menu import show_config_menu
from algorithms import *

class Simulation:
    def __init__(
            self,
            algorithm: str="Bubble Sort",
            num_bars: int=40
        ) -> None:
        """
        Initialize the Simulation class.

        Args:
            algorithm (str): The sorting algorithm to be used. Default is "Bubble Sort".
            num_bars (int): The number of bars to be sorted. Default is 40.
        Returns:
            None
        """
        # MAIN CONFIG
        pg.display.set_caption('Sorting Algorithms')
        self.font: pg.font.Font = pg.font.Font(None, 20)
        self.num_bars: int = num_bars
        self.algorithm: str = algorithm

        # MAIN SURFACE
        self.screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock: pg.time.Clock = pg.time.Clock()

        # BARS SURFACE
        self.bars_surface: pg.Surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - SURFACE_OFFSET))
        self.sizes: list[int] = self.get_random_sizes()
        self.sort_btn: Button = Button(text='Sort Bars',
                               width=200, height=40,
                               pos=(SCREEN_WIDTH // 4, 25),
                               fontsize=30,
                               screen=self.screen)
        self.randomize_btn: Button = Button(text='Randomize Bars',
                                    width=200, height=40,
                                    pos=(SCREEN_WIDTH - SCREEN_WIDTH // 4, 25),
                                    fontsize=30,
                                    screen=self.screen)
        
        self.return_btn: Button = Button(text='Return to Menu',
                                 width=200, height=40,
                                 pos=(SCREEN_WIDTH // 2, 25),
                                 fontsize=30,
                                 screen=self.screen)

        self.generator = None
        self.sorting: bool = False
        self.elapsed_time: float = 0
        self.start_time: float = 0
        self.is_sorted: bool = False

        self.counts: dict = {
            'comparisons': 0,
            'array_accesses': 0
        }
    
    def calculate_bars(self) -> tuple[int, int, float, float, int]:
        """
        Calculate the width and height of the bars.

        Returns:
            tuple: A tuple containing the width and height of the bars.
        """
        surface_width: int = self.bars_surface.get_width()
        surface_height: int = self.bars_surface.get_height()

        m = 20
        k = 0.5

        available_width = surface_width - 2 * m

        bw = available_width / (self.num_bars + (self.num_bars - 1) * k)
        gap = k * bw

        return (surface_width, surface_height, bw, gap, m)
    
    def draw_bars(self, bar_1: int=None, bar_2: int=None) -> None:
        """
        Draw the bars on the bars surface.

        Args:
            bar_1 (int): The index of the first bar to be highlighted.
            bar_2 (int): The index of the second bar to be highlighted.

        Returns:
            None
        """
        surface_width, surface_height, bw, gap, m = self.calculate_bars()

        for i in range(self.num_bars):
            x = m + i * (bw + gap)

            if i in (bar_1, bar_2):
                pg.draw.rect(self.bars_surface, DARK_PURPLE,
                                (x, surface_height - self.sizes[i], bw, self.sizes[i]))
            else:
                pg.draw.rect(self.bars_surface, WHITE,
                            (x, surface_height - self.sizes[i], bw, self.sizes[i]))


    def get_random_sizes(self) -> list[int]:
        """
        Generate a list of random sizes for the bars.

        Returns:
            list: A list of random sizes for the bars.
        """
        max_value = self.bars_surface.get_height() - 60
        min_value = 30
        step = (max_value - min_value) // (self.num_bars - 1)

        sizes = []

        for i in range(self.num_bars):
            sizes.append(min_value + i * step)

        shuffle(sizes)

        return sizes

    def randomize_bars(self) -> None:
        """
        Randomize the sizes of the bars.

        Returns:
            None
        """
        self.sizes = self.get_random_sizes()
    
    def draw_text(self, info: str, x: int=10, y: int=10):
        """
        Draw text on the bars surface.

        Args:
            info (str): The text to be drawn.
            x (int, optional): The x position of the text. Defaults to 10.
            y (int, optional): The y position of the text. Defaults to 10.

        Returns:
            None
        """
        debug_surface = self.font.render(str(info), True, DARK_PURPLE)
        debug_rect = debug_surface.get_rect(topleft=(x, y))
        pg.draw.rect(self.bars_surface, 'Black', debug_rect)
        self.bars_surface.blit(debug_surface, debug_rect)

    def event_loop(self) -> None:
        """
        Returns:
            None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    def check_button_click(self) -> bool:
        """
        Check if a button has been clicked.

        Returns:
            bool: True if a button has been clicked, False otherwise.
        """
        if self.sort_btn.clicked() and not self.sorting and not self.is_sorted:
            self.sorting = True
            self.counts['comparisons'] = 0
            self.counts['array_accesses'] = 0
            self.start_time = time()

            match self.algorithm:
                case 'Bubble Sort':
                    self.generator = bubble_sort_gen(self.sizes, self.counts)
                case 'Quick Sort':
                    self.generator = quick_sort_gen(self.sizes, 0, len(self.sizes) - 1, self.counts)
                case 'Merge Sort':
                    self.generator = merge_sort_gen(self.sizes, 0, len(self.sizes) - 1, self.counts)
                case 'Insertion Sort':
                    self.generator = insertion_sort_gen(self.sizes, self.counts)

        if self.randomize_btn.clicked() and not self.sorting:
            self.randomize_bars()
            self.is_sorted = False
            self.generator = None

        if self.return_btn.clicked() and not self.sorting:
            self.running = False
    
    def check_and_sort(self) -> bool:
        """
        Check if the bars are sorted and sort them if they are not.

        Returns:
            bool: True if the bars are sorted, False otherwise.
        """
        if self.sorting:
            self.elapsed_time = self.start_time - time()
            self.draw_text(f'Elapsed Time: {abs(self.elapsed_time):.2f}', 10, 60)
            try:
                i, j, comparisons, array_accesses = next(self.generator)
                self.counts['comparisons'] = comparisons
                self.counts['array_accesses'] = array_accesses
                self.draw_bars(i, j)
            except StopIteration:
                self.sorting = False
                self.end_time = time()
                self.elapsed_time = self.start_time - self.end_time
                self.generator = None
                self.is_sorted = True
        else:
            self.draw_bars()
            self.draw_text(f'Elapsed Time: {abs(self.elapsed_time):.2f}', 10, 60)
    
    def draw_everything(self) -> None:
        """
        Draw everything on the screen.

        Returns:
            None
        """
        self.screen.fill(BLACK)
        self.screen.blit(self.bars_surface, (0, SURFACE_OFFSET))
        self.bars_surface.fill(BLACK)

        self.randomize_btn.draw(self.sorting)
        self.sort_btn.draw(self.sorting)
        self.return_btn.draw(self.sorting)

        self.draw_text(f'Algorithm: {self.algorithm}', 10, 20)
        self.draw_text(f'Number of Bars: {self.num_bars}', 10, 40)
        self.draw_text(f'Comparisons: {self.counts["comparisons"]}', 10, 80)
        self.draw_text(f'Array Accesses: {self.counts["array_accesses"]}', 10, 100)

    def run(self) -> None:
        """
        Run the simulation (game loop).

        Returns:
            None
        """
        self.running = True
        while self.running:
            self.event_loop()
            self.check_button_click()
            self.check_and_sort()
            self.draw_everything()

            pg.display.update()
            self.clock.tick(FRAMERATE)

def main():
    pg.init()
    game_running: bool = True
    while game_running:
        try:
            algorithm, num_bars, game_running = show_config_menu()
            if game_running == True:
                simulation: Simulation = Simulation(algorithm, num_bars)
                simulation.run()
            else:
                break
        except Exception as e:
            print(f'Exeption: {e}')
            break
    pg.quit()

if __name__ == '__main__':
    main()
