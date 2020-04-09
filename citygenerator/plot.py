import numpy as np
import math
import datetime
import time
import os
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# SUPPORT FUNCTIONS FOR 3D BLOCK PLOTS
# -----------

def vertices(blocks):
    vertices = []
    for block in blocks:
        x = block[0:2]
        y = block[2:4]
        z = block[4:6]
        verts = [[x[0], y[0], z[0]], 
                [x[0], y[0], z[1]],
                [x[0], y[1], z[0]],
                [x[0], y[1], z[1]], 
                [x[1], y[0], z[0]],
                [x[1], y[0], z[1]],
                [x[1], y[1], z[0]], 
                [x[1], y[1], z[1]]]
        vertices.append(verts)

    return vertices


def faces(blocks):

    verts = vertices(blocks)
    faces = []
    for v in verts:
        face = [[v[0], v[1], v[3], v[2]],
               [v[2], v[3], v[7], v[6]],
               [v[6], v[7], v[5], v[4]],
               [v[4], v[5], v[1], v[0]],
               [v[1], v[3], v[7], v[5]],
               [v[0], v[2], v[6], v[4]]]
        faces.append(face)
        
    return faces


# SUPPORT FUNCTIONS FOR VIDEOS
# ------------------------------------------

def save_path(path):
    # create directory to save plots
    today = datetime.datetime.now()
    timestamp = today.strftime('%Y-%m-%d-%H%M')
    savedir = path
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    savehere = os.path.join(savedir, timestamp, '')
    if not os.path.exists(savehere):
        os.mkdir(savehere)
    return savehere
        
        
def save_image(path, i, **save_kwargs):
    plt.savefig("%s-%03d" % (path, int(i)), 
                **save_kwargs)
    return


def show_video(fig):
    IPython.display.display(fig)
    IPython.display.clear_output(wait=True)
    time.sleep(0.1)
    return

# -----------
# MAIN PLOTTING FUNCTIONS

def plot_2dlayout(blocks, ax=None, limits=None, **kwargs):
    # block in blocks has form [xmin, xmax, ymin, ymax, ...]
    # limits are plot limits and has form [xmin, xmax, ymin, ymax]
    
    if ax is None:
        ax = plt.axes()

    for block in blocks:
        start = tuple([block[0], block[2]])  # xmin, ymin
        width = block[1] - block[0]  # xmax - xmin
        height = block[3] - block[2]  # ymax - ymin
        p = patches.Rectangle(start, width, height, **kwargs)
        ax.add_patch(p)

    if limits is None:
        ax.autoscale()
    else:
        ax.set_xlim(limits[0:2])
        ax.set_ylim(limits[2:4])
        ax.set_xticks(np.linspace(*limits[0:2], 5))
        ax.set_yticks(np.linspace(*limits[2:4], 5))
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')

    return


def plot_3dlayout(blocks, ax=None, limits=None, **kwargs):
    
    if ax is None:
        ax = plt.axes(projection='3d')
        
    if limits is None:  # need to set some limits otherwise we cannot see anything
        xmax = np.amax([block[1] for block in blocks])
        ymax = np.amax([block[3] for block in blocks])
        zmax = np.amax([block[5] for block in blocks])
        limits = [0, xmax, 0, ymax, 0, 3*zmax]
        
    fas = faces(blocks)

    for sides in fas:
        collection = Poly3DCollection(sides, **kwargs)
        ax.add_collection3d(collection)
    
    ax.set_xlim(limits[0:2])
    ax.set_ylim(limits[2:4])
    ax.set_zlim(limits[4:6])        
    ax.xaxis.set_ticks(np.linspace(*limits[0:2], 5))
    ax.yaxis.set_ticks(np.linspace(*limits[2:4], 5))
    ax.zaxis.set_ticks(np.linspace(*limits[4:6], 4))
        
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.05))

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    ax.set_aspect('equal')
    ax.view_init(25, 235)
    
    plt.gca().patch.set_facecolor('none')  # set figure background

    return


def video_layout(blockgeneration, greenery=[], fig=None, ax=None, limits=None, show=True, save=False, path="./", **kwargs):

    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(1, 1, 1)

    # create directory to save plots
    if save is True:
        savehere = save_path(path)

    for i, blocks in enumerate(blockgeneration):

        if len(blocks[0]) == 4:  # a block in itblocks is 2D
            ax.clear()  # clear data from axis
            plot_2dlayout(blocks, ax=ax, limits=limits[:4], **kwargs)

        elif len(blocks[0]) == 6:  # a block in itblocks is 3D
            plt.clf()  # clear plot data
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            plot_3dlayout(blocks, ax=ax, limits=limits, **kwargs)
            plot_3dlayout(greenery, ax=ax, facecolor='g', limits=limits)
            ax.dist=11

        if save is True:
            save_image(savehere + "ULG", i)  
        if show is True:
            show_video(fig)

    plt.show()

    return
