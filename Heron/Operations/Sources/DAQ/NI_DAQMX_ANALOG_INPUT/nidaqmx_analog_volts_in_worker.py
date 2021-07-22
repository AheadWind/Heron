
import sys
from os import path

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))

import threading
import numpy as np
from dearpygui.core import *
from dearpygui.simple import *
import nidaqmx
import cv2 as cv2
from Heron import general_utils as gu
from Heron.Operations.Sources.DAQ.NI_DAQMX_ANALOG_INPUT import nidaqmx_analog_volts_in_com
from Heron.communication.source_worker import SourceWorker

acquiring_on = False
buffer_size = 0
task: nidaqmx.Task
worker_object: SourceWorker
window_showing = False
channels: list
rate: int
sample_mode: int


def plot(data):
    global buffer_size
    global channels

    # updating plot data
    plot_datax = np.arange(buffer_size)
    plot_datay = data
    try:
        for i, n in enumerate(channels):
            add_data("plot_datax_{}".format(n), plot_datax)
            add_data("plot_datay_{}".format(n), plot_datay)
            # plotting new data
            add_line_series('Plot {}'.format(n), "Voltage of {}/ V".format(n), plot_datax, plot_datay[i, :], weight=2)
    except Exception as e:
        print(e)


def plot_callback():
    global worker_object
    global window_showing
    global channels

    window_showing = False

    if worker_object.visualisation_on:
        if not window_showing:
            show_item('Visualisation')
            for n in channels:
                show_item("Plot {}".format(n))
            window_showing = True
        if window_showing:
            try:
                if len(channels) == 1:
                    plot([worker_object.worker_result])
                else:
                    plot(worker_object.worker_result)
            except Exception as e:
                print(e)

    if not worker_object.visualisation_on:
        window_showing = False
        try:
            hide_item('Visualisation')
            for n in channels:
                hide_item('Plot {}'.format(n))
        except Exception as e:
            pass


def start_plotting_thread():
    global channels

    with window("Visualisation", width=500, height=700, show=False):
        for n in channels:
            add_plot("Plot {}".format(n), height=int(700/len(channels)), show=False)
            add_data("plot_datax_{}".format(n), [])
            add_data("plot_datay_{}".format(n), [])
    start_dearpygui(primary_window='Visualisation')


def acquire(_worker_object):
    global acquiring_on
    global task
    global buffer_size
    global worker_object
    global channels
    global rate
    global sample_mode

    worker_object = _worker_object

    worker_object.set_new_visualisation_loop(start_plotting_thread)

    while not acquiring_on:
        try:
            channels = worker_object.parameters[1].split(' ')
            rate = int(worker_object.parameters[2])
            sample_mode = worker_object.parameters[3]
            buffer_size = int(worker_object.parameters[4])

            if sample_mode == 'CONTINUOUS':
                sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS
            elif sample_mode == 'FINITE':
                sample_mode = nidaqmx.constants.AcquisitionType.FINITE
            elif sample_mode == 'HW_TIMED_SINGLE_POINT':
                sample_mode = nidaqmx.constants.AcquisitionType.HW_TIMED_SINGLE_POINT

            acquiring_on = True
            print('Got nidaqmx analog input parameters. Starting capture')
        except Exception as e:
            cv2.waitKey(10)

    task = nidaqmx.Task('Main')
    for n in channels:
        task.ai_channels.add_ai_voltage_chan(n)
    task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=sample_mode,
                                    samps_per_chan=buffer_size)
    task.start()

    while True:
        worker_object.worker_result = np.array(task.read(number_of_samples_per_channel=buffer_size))
        worker_object.socket_push_data.send_array(worker_object.worker_result, copy=False)
        plot_callback()
        try:
            worker_object.visualisation_on = worker_object.parameters[0]
        except:
            worker_object.visualisation_on = nidaqmx_analog_volts_in_com.ParametersDefaultValues[0]

        worker_object.visualisation_loop_init()


def on_end_of_life():
    global task
    global figure
    global acquiring_on

    acquiring_on = False
    try:
        task.stop()
        task.close()
        del task
        stop_dearpygui()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    gu.start_the_source_worker_process(acquire, on_end_of_life)