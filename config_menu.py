import pygame as pg
from pygame_gui.elements import *
from pygame_gui import *
from constants import *

def show_config_menu() -> tuple[str, int, bool]:
    """
    Show the configuration menu for the game.

    Returns:
        tuple[str, int, bool]: A tuple containing the sorting algorithm, number of bars, and wether to run the simulation.
    """
    WINDOW_SIZE: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
    config_screen: pg.Surface = pg.display.set_mode(WINDOW_SIZE)
    manager: UIManager = UIManager(WINDOW_SIZE)

    width_start_btn: int = 100
    height_start_btn: int = 50

    x_start_btn: int = int((SCREEN_WIDTH // 2) - (width_start_btn // 2))
    y_start_btn: int = int(SCREEN_HEIGHT * 0.2)

    start_btn: UIButton = UIButton(
        relative_rect=pg.Rect((x_start_btn, y_start_btn), (width_start_btn, height_start_btn)),
        text='Start',
        manager=manager
    )

    width_dropdown: int = 200
    height_dropdown: int = 50
    
    x_dropdown: int = int((SCREEN_WIDTH // 2) - (width_dropdown // 2))
    y_dropdown: int = int(SCREEN_HEIGHT * 0.4)

    dropdown_algorithm: UIDropDownMenu = UIDropDownMenu(
        options_list=[
            'Bubble Sort',
            'Quick Sort',
            'Merge Sort',
            'Insertion Sort'
        ],
        starting_option='Bubble Sort',
        relative_rect=pg.Rect((x_dropdown, y_dropdown), (width_dropdown, height_dropdown)),
        manager=manager
    )

    width_bars_slider: int = 200
    height_bars_slider: int = 50
    
    x_bars_slider: int = int((SCREEN_WIDTH // 2) - (width_bars_slider // 2))
    y_bars_slider: int = int(SCREEN_HEIGHT * 0.6)

    bars_slider: UIHorizontalSlider = UIHorizontalSlider(
        relative_rect=pg.Rect((x_bars_slider, y_bars_slider), (width_bars_slider, height_bars_slider)),
        start_value=40,
        value_range=(40, 400),
        manager=manager
    )

    width_bars_label: int = 200
    height_bars_label: int = 50
    offset_bars_label: int = 135
    
    x_bars_label: int = int((SCREEN_WIDTH // 2) - (width_bars_label // 2) - offset_bars_label)
    y_bars_label: int = int(SCREEN_HEIGHT * 0.6)

    bars_label: UILabel = UILabel(
        relative_rect=pg.Rect((x_bars_label, y_bars_label), (width_bars_label, height_bars_label)),
        text=f'Bars: {int(bars_slider.get_current_value())}',
        manager=manager
    )

    width_quit_btn: int = 100
    height_quit_btn: int = 50
    
    x_quit_btn: int = int((SCREEN_WIDTH // 2) - (width_quit_btn // 2))
    y_quit_btn: int = int(SCREEN_HEIGHT * 0.8)

    quit_btn: UIButton = UIButton(
        relative_rect=pg.Rect((x_quit_btn, y_quit_btn), (width_quit_btn, height_quit_btn)),
        text='Quit',
        manager=manager
    )

    running: bool = True
    num_bars: int = 20

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == bars_slider:
                    bars_label.set_text(f'Bars: {int(bars_slider.get_current_value())}')

            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == start_btn:
                    algorithm = dropdown_algorithm.selected_option[0]
                    num_bars = int(bars_slider.get_current_value())
                    running = False
                    return (algorithm, num_bars, True)
                if event.ui_element == quit_btn:
                    algorithm = dropdown_algorithm.selected_option[0]
                    num_bars = int(bars_slider.get_current_value())
                    running = False
                    return (algorithm, num_bars, False)
            manager.process_events(event)

        manager.update(FRAMERATE)
        config_screen.fill((40, 40, 40))
        manager.draw_ui(config_screen)
        pg.display.update()
