from curses.ascii import isdigit
import dearpygui.dearpygui as dpg
from calc_state import CalcState
from helpers import get_calc_size, get_screen_center

from typings import ButtonPayload, PayloadType

calc_state = CalcState()

def button_callback(sender, app_data, user_data: ButtonPayload):
    error = calc_state.get_error()
    current_expression = calc_state.get_current_expression()
    result = ''

    math_operations = ['/', '*', '+', '-']

    if user_data.payload_type == PayloadType.OPERATION:
        if user_data.data in math_operations:
            current_expression += user_data.data
            error = ''
        elif user_data.data == 'C':
            current_expression = ''
            error = ''
        elif user_data.data == '=':
            try:
                result = eval(current_expression)
                current_expression = ''
            except:
                error = 'Invalid math expression!'
    else:
        error = ''
        current_expression += user_data.data

    calc_state.update_state(current_expression=current_expression, error=error, result=result)
    render()


dpg.create_context()

calc_dimensions = get_calc_size()
screen_center = get_screen_center()
dpg.create_viewport(title='Calc', width=calc_dimensions[0], height=calc_dimensions[1], x_pos=screen_center[0] - int(calc_dimensions[0] / 2), y_pos=screen_center[1] - int(calc_dimensions[1] / 2))    

def table(width, height):
    with dpg.table(header_row=False, height=height):
        buttons = calc_state.get_buttons()

        for i in buttons[0]:
            dpg.add_table_column(init_width_or_weight=0.25, width_stretch=True)

        button_width = int(width / len(buttons[0]))
        button_height = int(height / len(buttons))

        for row in buttons:
            with dpg.table_row():
                for button in row:
                    button_payload = ButtonPayload(PayloadType.NUMBER if isdigit(button) else PayloadType.OPERATION, button)
                    dpg.add_button(label=button, user_data=button_payload, callback=button_callback, width=button_width, height=button_height)
                
def result_window(height):
    with dpg.table(header_row=False, height=height):
        dpg.add_table_column(width_stretch=True)

        for i in range(3):
            with dpg.table_row():
                dpg.add_text('', tag=f'res{i}')
    dpg.add_separator()

def working_window(height):
    with dpg.table(header_row=False, height=height):
        dpg.add_table_column(width_stretch=True)

        with dpg.table_row():
            dpg.add_text('', tag='ww')
        with dpg.table_row():
            dpg.add_text('', tag='error')

def build():
    result_window(int(calc_dimensions[1] / 4))
    # почему тут -40? без этих 40 пикселей появляется скролл, который, я так и не разобрался, как убрать)0))
    working_window(int(calc_dimensions[1] / 4) - 40)
    table(calc_dimensions[0], int(calc_dimensions[1] / 2))

def render(): 
    dpg.set_value('ww', calc_state.get_current_expression())
    dpg.set_value('error', calc_state.get_error())

    for i, result in enumerate(calc_state.get_results()): 
        dpg.set_value(f'res{i}', result)

with dpg.window() as calc_workspace:
    build()


dpg.set_primary_window(calc_workspace, True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()