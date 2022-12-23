import itertools
import dearpygui.dearpygui as dpg
from enum import Enum
import numpy as np
import math
import time
from queue import Queue

dpg.create_context()
dpg.create_viewport(title='Volt Meter', width=400, height=500)
dpg.set_viewport_vsync(True)
dpg.setup_dearpygui()
dpg.show_viewport()

MIN_VOLTMETER_VALUE = 0
MAX_VOLTMETER_VALUE = 10
VOLTMETER_UPDATE_INTERVAL = 50
MEAN_UPDATE_INTERVAL = 500


class Colors(Enum):
    RED = [170, 15, 35],
    WHITE = [255, 255, 255],


class MeasurementInterval(Enum):
    ONE_SECOND = "1 second",
    TEN_SECONDS = "10 seconds",
    HALF_MINUTE = "half minute",
    MINUTE = "minute",


class VoltmeterValue:
    def __init__(self, value, time) -> None:
        self.value = value
        self.time = time


MEASUREMENT_INTERVAL = MeasurementInterval.ONE_SECOND

current_voltmeter_value = np.random.normal(5, 0.1)
last_time_voltmeter_updated = int(time.time() * 1000)
last_time_mean_updated = int(time.time() * 1000)

VOLTMETER_VALUES = Queue()


def choose_interval(_, app_data):
    global MEASUREMENT_INTERVAL

    if app_data == MeasurementInterval.ONE_SECOND.value[0]:
        MEASUREMENT_INTERVAL = MeasurementInterval.ONE_SECOND
    elif app_data == MeasurementInterval.TEN_SECONDS.value[0]:
        MEASUREMENT_INTERVAL = MeasurementInterval.TEN_SECONDS
    elif app_data == MeasurementInterval.HALF_MINUTE.value[0]:
        MEASUREMENT_INTERVAL = MeasurementInterval.HALF_MINUTE
    else:
        MEASUREMENT_INTERVAL = MeasurementInterval.MINUTE


def draw_analog():
    with dpg.drawlist(width=350, height=350, parent="voltmeter_group"):
        with dpg.draw_node(tag="draw_node"):
            dpg.draw_circle([300, 300], 30, color=Colors.RED.value[0],
                            fill=Colors.RED.value[0])

            dpg.draw_text([10, 10], "V", size=40)

            angle_step = 90 / 20
            text_step = (MAX_VOLTMETER_VALUE - MIN_VOLTMETER_VALUE) / 20

            for i in range(21):
                outer_radius = 300 if i % 2 == 0 else 295
                inner_radius = 280 if i % 2 == 0 else 285
                line_color = Colors.WHITE.value[0] if i % 2 != 0 else Colors.RED.value[0]
                text_value = int(text_step * i)
                thickness = 3 if i % 2 == 0 else 1

                line_angle = 180 - i * angle_step

                start_x = 300 - round(
                    abs(math.cos(math.radians(line_angle)) * outer_radius))
                start_y = 300 - round(
                    abs(math.sin(math.radians(line_angle)) * outer_radius))

                end_x = 300 - round(
                    abs(math.cos(math.radians(line_angle)) * inner_radius))
                end_y = 300 - round(
                    abs(math.sin(math.radians(line_angle)) * inner_radius))

                text_x = 300 - round(
                    abs(math.cos(math.radians(line_angle)) * 270))
                text_y = 300 - round(
                    abs(math.sin(math.radians(line_angle)) * 270))

                dpg.draw_line((start_x, start_y), (end_x, end_y),
                              color=line_color, thickness=thickness)

                if i % 2 == 0:
                    dpg.draw_text([text_x, text_y], text_value, size=16)


with dpg.window(width=400, height=500, no_collapse=True, no_title_bar=True, no_move=True, tag="main_window"):
    with dpg.group(pos=[25, 20], tag='voltmeter_group'):
        draw_analog()

    dpg.add_combo([MeasurementInterval.ONE_SECOND.value[0], MeasurementInterval.TEN_SECONDS.value[0], MeasurementInterval.HALF_MINUTE.value[0], MeasurementInterval.MINUTE.value[0]], pos=[
                  25, 390], callback=choose_interval, label="Measurement interval", width=200, default_value=MEASUREMENT_INTERVAL.value[0])
    dpg.add_text(
        "Mean voltage calculated for chosen measurement interval", pos=[25, 420], wrap=350)
    dpg.add_text(str(np.round(current_voltmeter_value, 3)),
                 pos=[25, 460], tag="mean_voltage")


def draw_arrow():
    dpg.delete_item("voltmeter_arrow")
    arrow_angle = 180 - ((current_voltmeter_value * 10) *
                         (90 / ((MAX_VOLTMETER_VALUE - MIN_VOLTMETER_VALUE) * 10)))
    arrow_start_x = 300 - \
        round(abs(math.cos(math.radians(arrow_angle)) * 250))
    arrow_start_y = 300 - \
        round(abs(math.sin(math.radians(arrow_angle)) * 250))

    dpg.draw_line((arrow_start_x, arrow_start_y), (300, 300),
                  color=Colors.RED.value[0], thickness=7, parent="draw_node", tag="voltmeter_arrow")


def show_stats(current_time):
    last_index = -1
    time_difference = -1

    if MEASUREMENT_INTERVAL == MeasurementInterval.ONE_SECOND:
        time_difference = 1000
    elif MEASUREMENT_INTERVAL == MeasurementInterval.TEN_SECONDS:
        time_difference = 10000
    elif MEASUREMENT_INTERVAL == MeasurementInterval.HALF_MINUTE:
        time_difference = 30000
    else:
        time_difference = 60000

    for i in range(VOLTMETER_VALUES.qsize() - 1, 0, -1):
        measurement_time = VOLTMETER_VALUES.queue[i].time

        if current_time - measurement_time > time_difference or i == 0:
            last_index = i
            break

    if last_index >= 0:
        mean = np.mean(list(map(lambda x: x.value, itertools.islice(
            VOLTMETER_VALUES.queue, last_index, VOLTMETER_VALUES.qsize() - 1))))

        dpg.set_value("mean_voltage", np.round(mean, 3))


while dpg.is_dearpygui_running():
    current_time = int(time.time() * 1000)

    if current_time - last_time_voltmeter_updated > VOLTMETER_UPDATE_INTERVAL:
        draw_arrow()
        last_time_voltmeter_updated = current_time

    if current_time - last_time_mean_updated > MEAN_UPDATE_INTERVAL:
        show_stats(current_time)
        last_time_mean_updated = current_time

    current_voltmeter_value = np.random.normal(5, 0.5)

    if VOLTMETER_VALUES.qsize() > 0:
        if current_time - VOLTMETER_VALUES.queue[0].time >= 60000:
            VOLTMETER_VALUES.get()
    VOLTMETER_VALUES.put(VoltmeterValue(current_voltmeter_value, current_time))

    dpg.render_dearpygui_frame()

dpg.destroy_context()
