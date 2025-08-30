import pygame as pg
from constants import *
from button import Button
from random import shuffle
from time import time
from config_menu import show_config_menu
from algorithms import *

class Main:
    def __init__(self, algorithm, num_bars):
        # MAIN CONFIG
        pg.display.set_caption('Sorting Algorithms')
        self.font = pg.font.Font(None, 20)
        self.num_bars = num_bars
        self.algorithm = algorithm

        # MAIN SURFACE
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        # BARS SURFACE
        self.bars_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - SURFACE_OFFSET))
        self.sizes = self.get_random_sizes()
        self.sort_btn = Button(text='Sort Bars',
                               width=200, height=40,
                               pos=(SCREEN_WIDTH // 4, 25),
                               fontsize=30,
                               screen=self.screen)
        self.randomize_btn = Button(text='Randomize Bars',
                                    width=200, height=40,
                                    pos=(SCREEN_WIDTH - SCREEN_WIDTH // 4, 25),
                                    fontsize=30,
                                    screen=self.screen)
        
        self.return_btn = Button(text='Return to Menu',
                                 width=200, height=40,
                                 pos=(SCREEN_WIDTH // 2, 25),
                                 fontsize=30,
                                 screen=self.screen)

        self.generator = None
        self.sorting = False
        self.comparisons = 0
        self.elapsed_time = 0
        self.start_time = 0
        self.is_sorted = False
        self.array_accesses = 0
    
    def calculate_bars(self):
        surface_width = self.bars_surface.get_width()
        surface_height = self.bars_surface.get_height()

        m = 20
        k = 0.5

        available_width = surface_width - 2 * m

        bw = available_width / (self.num_bars + (self.num_bars - 1) * k)
        gap = k * bw

        return surface_width, surface_height, bw, gap, m
    
    def draw_bars(self, bar_1=None, bar_2=None):
        surface_width, surface_height, bw, gap, m = self.calculate_bars()

        for i in range(self.num_bars):
            x = m + i * (bw + gap)

            if i in (bar_1, bar_2):
                pg.draw.rect(self.bars_surface, GREEN,
                                (x, surface_height - self.sizes[i], bw, self.sizes[i]))
            else:
                pg.draw.rect(self.bars_surface, WHITE,
                            (x, surface_height - self.sizes[i], bw, self.sizes[i]))


    def get_random_sizes(self):
        max_value = self.bars_surface.get_height() - 60
        min_value = 30
        step = (max_value - min_value) // (self.num_bars - 1)

        sizes = []

        for i in range(self.num_bars):
            sizes.append(min_value + i * step)

        shuffle(sizes)

        return sizes

    def randomize_bars(self):
        self.sizes = self.get_random_sizes()
    
    def draw_text(self, info, x=10, y=10):
        debug_surface = self.font.render(str(info), True, 'Green')
        debug_rect = debug_surface.get_rect(topleft=(x, y))
        pg.draw.rect(self.bars_surface, 'Black', debug_rect)
        self.bars_surface.blit(debug_surface, debug_rect)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    def check_button_click(self):
        if self.sort_btn.clicked() and not self.sorting and not self.is_sorted:
            self.sorting = True
            self.comparisons = 0
            self.array_accesses = 0
            self.start_time = time()
            if self.algorithm == 'Bubble Sort':
                self.generator = bubble_sort_gen(self.sizes, self.comparisons, self.array_accesses)
            elif self.algorithm == 'Quick Sort':
                self.generator = quick_sort_gen(self.sizes, 0, len(self.sizes) - 1, self.comparisons, self.array_accesses)
            elif self.algorithm == 'Merge Sort':
                self.generator = merge_sort_gen(self.sizes, 0, len(self.sizes) - 1, self.comparisons, self.array_accesses)
            elif self.algorithm == 'Insertion Sort':
                self.generator = insertion_sort_gen(self.sizes, self.comparisons, self.array_accesses)

        if self.randomize_btn.clicked() and not self.sorting:
            self.randomize_bars()
            self.is_sorted = False
            self.generator = None

        if self.return_btn.clicked() and not self.sorting:
            self.running = False
    
    def check_sort(self):
        if self.sorting:
            self.elapsed_time = self.start_time - time()
            self.draw_text(f'Elapsed Time: {abs(self.elapsed_time):.2f}', 10, 60)
            try:
                i, j, self.comparisons, self.array_accesses = next(self.generator)
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
    
    def draw_everything(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.bars_surface, (0, SURFACE_OFFSET))
        self.bars_surface.fill(BLACK)

        self.randomize_btn.draw(self.sorting)
        self.sort_btn.draw(self.sorting)
        self.return_btn.draw(self.sorting)

        self.draw_text(f'Algorithm: {self.algorithm}', 10, 20)
        self.draw_text(f'Number of Bars: {self.num_bars}', 10, 40)
        self.draw_text(f'Comparisons: {self.comparisons}', 10, 80)
        self.draw_text(f'Array Accesses: {self.array_accesses}', 10, 100)

    def run(self):
        self.running = True
        while self.running:
            self.event_loop()
            self.check_button_click()
            self.check_sort()
            self.draw_everything()

            pg.display.update()
            self.clock.tick(FRAMERATE)

def main():
    pg.init()
    game_running = True
    while game_running:
        try:
            algorithm, num_bars, game_running = show_config_menu()
            if game_running == True:
                simulation = Main(algorithm, num_bars)
                simulation.run()
            else:
                break
        except Exception as e:
            print(f'Exeption: {e}')
            break
    pg.quit()

if __name__ == '__main__':
    main()
