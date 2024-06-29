import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def load_and_plot_file():
    # Ask the user to select a file
    file_path = askopenfilename(title="Select an XDF file", filetypes=[("XDF files", "*.xdf")])

    if not file_path:
        print("No file selected. Exiting.")
        return

    data, header = pyxdf.load_xdf(file_path)

    plt.clf()  # Clear the current figure

    for stream in data:
        y = stream['time_series']

        if isinstance(y, list):
            # list of strings, draw one vertical line for each marker
            for timestamp, marker in zip(stream['time_stamps'], y):
                plt.axvline(x=timestamp)
                print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
        elif isinstance(y, np.ndarray):
            # numeric data, draw as lines
            plt.plot(stream['time_stamps'], y)
        else:
            raise RuntimeError('Unknown stream format')

    plt.draw()  # Redraw the current figure

def on_key(event):
    if event.key == 'ctrl+r':
        load_and_plot_file()

# Hide the main tkinter window
Tk().withdraw()

# Load and plot the initial file
load_and_plot_file()

# Connect the key press event handler
fig = plt.gcf()
fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()
