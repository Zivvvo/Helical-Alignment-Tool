from utils import tools
from utils import fit
import pandas as pd
import matplotlib.pyplot as plt

from utils import fit

data = pd.read_csv('data.txt', delim_whitespace=True)
newlist = tools.separate_by_name(data)

post_shift_df = tools.post_shift_data(newlist[0], 1.7448 / 1.37)
data_matrix = post_shift_df.to_numpy()



helices = tools.get_helices(data_matrix)

for helix in helices:
    tools.adjust_psi(helix, 0.5)

fitted_points = fit.fit_micrograph(helices)

# select micrograph 1 as example, plotting it using matplotlib
for (x, y) in fitted_points:
    plt.scatter(x, y)
    plt.savefig("aligned_micrograph_1_multithread.png", format= "png")
