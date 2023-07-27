from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

fontsize = 20
font = {'family': 'sans', 'color':  'black', 'weight': 'normal', 'size': fontsize}
myblue = [0/ 255, 150/255, 177/ 255]
lightgray = [0.1, 0.1, 0.1]
darkgray = [0.9, 0.9, 0.9]

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})


def complete_panel(ax, xlabel, ylabel, cancel_x=False, cancel_y=False, color=lightgray, font=font, fontsize=fontsize, linewidth=2, tickwidth1=2.5, tickwidth2=2, legend=True, ncol=1, locator_x = 2, locator_y = 2):
    
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontdict=font)
        if cancel_x:
            ax.set_xticklabels([])
    else:
        ax.set_xticklabels([])

    if ylabel is not None:
        ax.set_ylabel(ylabel, fontdict=font)
        if cancel_y:
            ax.set_yticklabels([])  
    else:
        ax.set_yticklabels([])

    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax.yaxis.offsetText.set_fontsize(20)
    ax.minorticks_on()

    ax.tick_params('both', length=10, width=tickwidth1, which='major', direction='in')
    ax.tick_params('both', length=6, width=tickwidth2, which='minor', direction='in')
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

    # border of graph
    ax.spines["top"].set_linewidth(linewidth)
    ax.spines["bottom"].set_linewidth(linewidth)
    ax.spines["left"].set_linewidth(linewidth)
    ax.spines["right"].set_linewidth(linewidth)

    minor_locator_x = AutoMinorLocator(locator_x)
    ax.xaxis.set_minor_locator(minor_locator_x)
    minor_locator_y = AutoMinorLocator(locator_y)
    ax.yaxis.set_minor_locator(minor_locator_y)

    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    ax.spines['left'].set_color(color)
    ax.spines['top'].set_color(color)
    ax.spines['bottom'].set_color(color)
    ax.spines['right'].set_color(color)
    ax.tick_params(axis='y', which='both', colors=color)
    ax.tick_params(axis='x', which='both', colors=color)

    if legend:
        ax.legend(frameon=False, fontsize=fontsize, 
                loc='best', handletextpad=0.5, ncol=ncol,
                handlelength = 0.86, borderpad = 0.3, 
                labelspacing=0.3)
        