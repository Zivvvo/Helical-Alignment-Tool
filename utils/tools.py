import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

'''
Takes a pandas dataframe as input, outputs a list of dataframes, each representing the individual micrographs
'''
def separate_by_name(data):
    #subsetting the dataframe by micrograph name
    i = 0
    micrographs = []
    df1 = None
    name = data.loc[0]["MicrographName"]
    oldIndex = 0
    newIndex = 0
    while (i < data.shape[0]):
        if (data.loc[i]["MicrographName"] != name):
            micrographs.append(data.iloc[oldIndex:i,:])
            oldIndex = i
            name = data.loc[i]["MicrographName"]
        i = i+1
    return micrographs

def scatter(micrograph, dir):
   #select micrograph 1 as example, plotting it using matplotlib
    for (x,y) in list(zip(micrograph.X0, micrograph.Y0)):
        plt.scatter(x,y)
    plt.savefig(dir, format = "png")
    plt.close()

def psi_extrapolate(x,y, psi, inter_dist, direction):
    dx = math.cos(psi)*inter_dist
    dy = math.sin(psi)*inter_dist
    if (direction):
        #positive direction
        new_point = (x+dx, y+dy)
    else:
        new_point = (x-dx, y-dy)
    return new_point

def L2_dist(x,y, x1, y1):
    return math.sqrt(math.pow((x-x1),2)+math.pow((y-y1),2))

def post_shift_data(dataframe, binning_factor):
    df = dataframe.copy(deep = True)
    for i in range(df.shape[0]):
        df.iloc[i,0] = df.iloc[i,0]+binning_factor*df.iloc[i,4]
        df.iloc[i,1] = df.iloc[i,1]+binning_factor*df.iloc[i,5]
    return df


def plot_psi(dataframe):
    i = 1
    for Psi in list(dataframe.AnglePsi):
        plt.scatter(i, Psi)
        i = i + 1


def plot_psi_np(numpy_arr):
    for i in range(numpy_arr.shape[0]):
        plt.scatter(i + 1, numpy_arr[i][8])


def plot_rot(dataframe):
    i = 1
    for rot in list(dataframe.AngleRot):
        plt.scatter(i, rot)
        i = i + 1


def plot_tilt(dataframe):
    i = 1
    for tilt in list(dataframe.AngleTilt):
        plt.scatter(i, tilt)
        i = i + 1

def get_helices(data_matrix):
    return np.split(data_matrix, np.where(np.diff(data_matrix[:,2]))[0]+1)

def point_search(helix, point, xmin, xmax, ymin, ymax, dist, direction):
    helix = np.copy(helix)
    final_points = []
    rand_point = point
    while (True):
        theoretical_next = psi_extrapolate(rand_point[0], rand_point[1], -1 * math.radians(rand_point[8]), dist ,
                                           direction)
        # check the nearest points in data_matrix to these two points, if none are there, plot a temporary point and include it in the final points
        if (theoretical_next[0] > xmax or theoretical_next[1] > ymax or theoretical_next[0] < xmin or
                theoretical_next[1] < ymin):
            break
        i = 0
        point_found = False
        for point1, point2 in zip(helix[:, 0], helix[:, 1]):
            if L2_dist(theoretical_next[0], theoretical_next[1], point1, point2) < 15:
                final_points.append((point1, point2))
                rand_point = helix[i]
                helix = np.delete(helix, i, 0)
                point_found = True
                break
            i = i + 1
        if (point_found == False):
            final_points.append(theoretical_next)
            rand_point[0] = theoretical_next[0]
            rand_point[1] = theoretical_next[1]
    return final_points

def mad(arr):
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))*1.4826

def std_mad(arr):
    return (arr - np.median(arr))/mad(arr)

def adjust_psi(helix, standard_dev_coefficient):
    arr = std_mad(helix[:,8])
    new_arr = helix[:,8][np.abs(arr)<standard_dev_coefficient]
    mean_psi = np.mean(new_arr)

    for i in range(helix.shape[0]):
        if np.abs(arr[i]) > standard_dev_coefficient:
            helix[i,8] = mean_psi
    return


def get_Rand_Point(helix, n):
    if helix.shape[0] < n:
        return helix[random.randrange(0, helix.shape[0])]
    else:
        score_x_arr = avg_shiftx(helix, n)
        score_y_arr = avg_shifty(helix, n)
        score_combination_arr = score_x_arr + score_y_arr
        index = np.argmin(score_combination_arr)
        return helix[index]


def avg_shiftx(helix, n):
    min_dev = 1000
    score_arr = np.zeros(len(helix), )
    for i in range(n - 1, len(helix)):
        avg_dev = np.std(helix[i - (n - 1):i, 4])
        score_arr[i - int(n / 2)] = avg_dev
    return score_arr


def avg_shifty(helix, n):
    min_dev = 1000
    score_arr = np.zeros(len(helix), )
    for i in range(n - 1, len(helix)):
        avg_dev = np.std(helix[i - (n - 1):i, 5])
        score_arr[i - int(n / 2)] = avg_dev
    return score_arr

