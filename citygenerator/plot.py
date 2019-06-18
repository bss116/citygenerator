import numpy as np
import math
import itertools
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
        vertices.append(list(itertools.product(x, y, z)))

    return vertices


def edges(blocks):

    edges = []
    for block in blocks:
        ed = []
        xlen = block[1] - block[0]
        ylen = block[3] - block[2]
        zlen = block[5] - block[4]
        verts = vertices([block])
        for s, e in itertools.combinations(np.array(verts[0]), 2):
            if np.sum(np.abs(s - e)) == xlen:
                edge = list(zip(s, e))
                ed.append(edge)
            elif np.sum(np.abs(s - e)) == ylen:
                edge = list(zip(s, e))
                ed.append(edge)
            elif np.sum(np.abs(s - e)) == zlen:
                edge = list(zip(s, e))
                ed.append(edge)
        edges.append(ed)

    return edges


def faces(blocks):

    verts = vertices(blocks)
    faces = []
    for v in verts:
        fac = [[v[0], v[1], v[3], v[2]],
               [v[2], v[3], v[7], v[6]],
               [v[6], v[7], v[5], v[4]],
               [v[4], v[5], v[1], v[0]],
               [v[1], v[3], v[7], v[5]],
               [v[0], v[2], v[6], v[4]]]
        faces.append(fac)
        
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

def layout(blocks, ax=None, limits=None, **kwargs):
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

    return ax


def blocks3d(blocks, ax=None, limits=None, **kwargs):
    
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

    return ax
