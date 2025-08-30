import pygame as pg
import pygame_gui
from constants import *

def show_config_menu():
    WINDOW_SIZE = (800, 600)
    config_screen = pg.display.set_mode(WINDOW_SIZE)
    manager = pygame_gui.UIManager(WINDOW_SIZE)

    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((350, 100), (100, 50)),
        text='Start',
        manager=manager
    )

    dropdown_algorithm = pygame_gui.elements.UIDropDownMenu(
        options_list=[
            'Bubble Sort',
            'Quick Sort',
            'Merge Sort',
            'Insertion Sort'
        ],
        starting_option='Bubble Sort',
        relative_rect=pg.Rect((300, 200), (200, 50)),
        manager=manager
    )

    bars_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pg.Rect((300, 300), (200, 50)),
        start_value=40,
        value_range=(40, 400),
        manager=manager
    )

    bars_label = pygame_gui.elements.UILabel(
        relative_rect=pg.Rect((200, 300), (120, 50)),
        text=f'Bars: {int(bars_slider.get_current_value())}',
        manager=manager
    )

    quit_btn = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((350, 400), (100, 50)),
        text='Quit',
        manager=manager
    )

    running = True
    num_bars = 20

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == bars_slider:
                    bars_label.set_text(f'Bars: {int(bars_slider.get_current_value())}')

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_btn:
                    algorithm = dropdown_algorithm.selected_option[0]
                    num_bars = int(bars_slider.get_current_value())
                    running = False
                    return algorithm, num_bars, True
                if event.ui_element == quit_btn:
                    algorithm = dropdown_algorithm.selected_option[0]
                    num_bars = int(bars_slider.get_current_value())
                    running = False
                    return algorithm, num_bars, False
            manager.process_events(event)

        manager.update(FRAMERATE)
        config_screen.fill((40, 40, 40))
        manager.draw_ui(config_screen)
        pg.display.update()
