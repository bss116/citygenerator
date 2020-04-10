import os
import datetime
import time
import IPython
import matplotlib.pyplot as plt
from . import plot

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
# MAIN VIDEO FUNCTIONS

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
            plot.plot_2dlayout(blocks, ax=ax, limits=limits[:4], **kwargs)

        elif len(blocks[0]) == 6:  # a block in itblocks is 3D
            plt.clf()  # clear plot data
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            plot.plot_3dlayout(blocks, ax=ax, limits=limits, **kwargs)
            plot.plot_3dlayout(greenery, ax=ax, facecolor='g', limits=limits)
            ax.dist=11

        if save is True:
            save_image(savehere + "ULG", i)  
        if show is True:
            show_video(fig)

    plt.show()

    return
