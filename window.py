import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar

window = tk.Tk()

window.title("Helical_Alignment_Tool")

frame = tk.Frame(master=window, width=100, height=100)
frame.pack()

path_label = tk.Label(text="Enter the path to data:", master=frame)

path_entry = tk.Entry(master=frame)

distance_label = tk.Label(text="Enter the inter-particle distance (float):", master=frame)

distance_entry = tk.Entry(master=frame)

binning_factor = tk.Label(text="Enter the binning factor (float):", master=frame)

binning_entry = tk.Entry(master=frame)

progress = Progressbar(window, orient=tk.HORIZONTAL,
                       length=100, mode='determinate')


def action():
    path = path_entry.get()
    distance = float(distance_entry.get())
    bin = float(binning_entry.get())

    if (len(path) == 0):
        return

    from utils import tools
    from utils import fit
    import pandas as pd
    import matplotlib.pyplot as plt

    from utils import fit

    data = pd.read_csv(path, delim_whitespace=True)
    newlist = tools.separate_by_name(data)
    i = 1
    for item in newlist:
        post_shift_df = tools.post_shift_data(item, bin)
        data_matrix = post_shift_df.to_numpy()

        helices = tools.get_helices(data_matrix)

        for helix in helices:
            tools.adjust_psi(helix, 0.5)

        fitted_points = fit.fit_micrograph(helices)

        # select micrograph 1 as example, plotting it using matplotlib
        for (x, y) in fitted_points:
            plt.scatter(x, y)
            plt.savefig("aligned_micrograph" + str(i)+".png", format="png")
            plt.close()
        progress['value'] += 100 / len(newlist)
        i += 1


button = tk.Button(window, text="submit", command=action)

path_label.pack()
path_entry.pack()
distance_label.pack()
distance_entry.pack()
binning_factor.pack()
binning_entry.pack()
button.pack()
progress.pack(pady=10)

window.mainloop()
