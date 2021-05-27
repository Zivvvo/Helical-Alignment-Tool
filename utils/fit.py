import concurrent.futures
import random

import numpy as np
from utils import tools

# fitting algorithm per micrograph

def fit_micrograph(helices):

    fitted_points = []

    # loop through each helix

    with concurrent.futures.ThreadPoolExecutor() as master_executor:
        futures = [master_executor.submit(fit_helix, fitted_points, helix) for helix in helices]
    return fitted_points

def fit_helix(fitted_points, helix):
    fitted_points_in_helix = []
    rand_point = helix[random.randrange(0, helix.shape[0])]

    max_x = np.amax(helix, axis=0)[0]
    max_y = np.amax(helix, axis=0)[1]

    min_x = np.amin(helix, axis=0)[0]
    min_y = np.amin(helix, axis=0)[1]

    # two thread process to compute positive extrapolation and negative extrapolation at the same time
    with concurrent.futures.ThreadPoolExecutor() as executor:
        parameters = [(helix, rand_point, min_x, max_x, min_y, max_y, 82.5, True),
                      (helix, rand_point, min_x, max_x, min_y, max_y, 82.5, False)]
        futures = [executor.submit(tools.point_search, param[0], param[1], param[2], param[3], param[4], param[5], param[6],
                                   param[7]) for param in parameters]
        return_values = [future.result() for future in futures]
        fitted_points_in_helix = [item for sublist in return_values for item in sublist]
    for x in fitted_points_in_helix:
        fitted_points.append(x)