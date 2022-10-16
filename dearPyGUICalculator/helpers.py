from screeninfo import get_monitors


# defining calculator size
def get_calc_size():
    monitor = get_monitors()[0]

    screen_width = monitor.width
    screen_height = monitor.height

    max_dimension = 'width' if screen_width >= screen_height else 'height'

    calc_width = 0
    calc_height = 0

    if max_dimension == 'width':
        calc_width = screen_width / 5
        calc_height = screen_height / 3
    else:
        calc_width = screen_width / 3
        calc_height = screen_height / 5

    return (int(calc_width), int(calc_height))

# calculating screen center to position calculator
def get_screen_center():
    monitor = get_monitors()[0]

    screen_width = monitor.width
    screen_height = monitor.height

    return (int(screen_width / 2), int(screen_height / 2))