import numpy as np
from scipy.stats import norm, skewnorm
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Arc
from cycler import cycler

np.random.seed(42)


plt.rcParams['axes.prop_cycle'] = cycler(
    'color',
    ['#5f9bfc', '#3fff66', '#45e0cb', '#e262fc', '#ffe311', '#b2b2b2'],
)


def trans2xy(trans, delta, cog_x, cog_y):
    trans = np.asanyarray(trans)
    x = cog_x - trans * np.sin(delta)
    y = cog_y + trans * np.cos(delta)
    return x, y


def long2xy(longitudinal, delta, cog_x, cog_y):
    longitudinal = np.asanyarray(longitudinal)
    x = cog_x + longitudinal * np.cos(delta)
    y = cog_y + longitudinal * np.sin(delta)
    return x, y


def generate_shower(cog_x, cog_y, width, length, size, delta, skewness):

    photons_long = skewnorm(skewness, 0, length).rvs(size)
    photons_trans = norm(0, width).rvs(size)

    photons_x = np.cos(delta) * photons_long + np.sin(delta) * photons_trans
    photons_y = - np.sin(delta) * photons_long + np.cos(delta) * photons_trans

    photons_x += cog_x
    photons_y += cog_y

    return photons_x, photons_y, photons_long, photons_trans


def add_hillas_annotations(cog_x, cog_y, width, length, delta, ax):
    ax.annotate(
        r'\texttt{length}',
        xy=long2xy(-length/2, delta, cog_x, cog_y),
        xytext=(-15, 15),
        textcoords='offset points',
        color='C1',
        va='center',
        ha='center',
        rotation=np.rad2deg(delta)
    )
    ax.annotate(
        r'\texttt{width}',
        xy=trans2xy(-width, delta, cog_x, cog_y),
        xytext=(0, -15),
        textcoords='offset points',
        color='C2',
        va='center',
        ha='left',
        rotation=np.rad2deg(delta - np.pi/2)
    )
    ax.annotate(
        r'\texttt{cog}',
        xy=(cog_x, cog_y), xytext=(-2, 5),
        textcoords='offset points',
        color='white'
    )
    ax.plot(
        *long2xy([-length, -4*length], delta, cog_x, cog_y),
        linestyle=':',
        color='white',
    )
    x, y = long2xy(-4 * length, delta, cog_x, cog_y)
    ax.plot([x, x + 80], [y, y], 'white')

    x, y = long2xy(-4 * length, delta, cog_x, cog_y)
    arc = Arc((x, y), 40, 40, 0, 0, np.rad2deg(delta), color='C3')
    ax.annotate(
        'delta', xy=(x, y), xytext=(25, 7),
        color='C3', textcoords='offset points',
    )
    ax.add_artist(arc)


def add_hillas_params(cog_x, cog_y, width, length, delta, ax):
    eps = Ellipse(
        (np.mean(px), np.mean(py)),
        width=2 * length,
        height=2*width,
        angle=np.rad2deg(delta),
        facecolor='none',
        edgecolor='C0',
        zorder=2
    )
    ax.add_artist(eps)
    ax.plot(*long2xy([0, -length], delta, cog_x, cog_y), color='C1')
    ax.plot(
        *trans2xy([0, -width], delta, cog_x, cog_y),
        color='C2',
    )
    ax.plot(cog_x, cog_y, marker='o', mew=0)


def calc_hillas(photon_x, photon_y):

    cog_x = np.mean(photon_x)
    cog_y = np.mean(photon_y)

    cov = np.cov(photon_x, photon_y)

    eig_vals, eig_vecs = np.linalg.eigh(cov)

    width, length = np.sqrt(eig_vals)

    delta = np.arctan(eig_vecs[1, 1] / eig_vecs[1, 0])

    return cog_x, cog_y, width, length, delta


def add_image(photons_x, photons_y, ax):
    img = ax.hexbin(
        px, py,
        gridsize=21,
        extent=[-10, 200, -10, 200],
        cmap='inferno',
        linewidth=0.2,
    )
    return img


def reset(ax):
    ax.cla()
    ax.set_axis_off()
    ax.set_aspect(1)
    ax.set_xlim(-20, 210)
    ax.set_ylim(-20, 210)


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_axes([0, 0.11, 0.78, 0.78])
    cax = fig.add_axes([0.8, 0.11, 0.05, 0.78])

    reset(ax)

    width = 15
    length = 45
    cog_x = 100
    cog_y = 100
    delta = np.deg2rad(-40)
    size = 500

    px, py, pl, pt = generate_shower(
        cog_x=cog_x,
        cog_y=cog_y,
        width=width,
        length=length,
        size=size,
        delta=delta,
        skewness=2,
    )

    img = add_image(px, py, ax)
    fig.colorbar(img, cax=cax, label='Number of Photons')
    # fig.savefig('Plots/hillas_1.pdf')

    cog_x, cog_y, width, length, delta = calc_hillas(px, py)

    add_hillas_params(cog_x, cog_y, width, length, delta, ax)
    add_hillas_annotations(cog_x, cog_y, width, length, delta, ax)

    fig.savefig('Plots/hillas.pdf')

    for sign, num in zip([1, -1], [5, 4]):
        reset(ax)
        img = add_image(px, py, ax)
        fig.colorbar(img, cax=cax, label='Number of Photons')
        add_hillas_params(cog_x, cog_y, width, length, delta, ax)

        ax.plot(30, 5, '*', mew=0, markersize=10, color='C4', zorder=3)
        ax.annotate(
            '$\mathrm{\gamma}$-Source',
            xy=(30, 5),
            xytext=(10, 0),
            textcoords='offset points',
            color='C4',
            va='top',
            ha='left',
        )

        # fig.savefig('Plots/hillas_3.pdf')

        ax.plot(
            *long2xy([0, sign * 3 * length], delta, cog_x, cog_y),
            linestyle=':',
            color='C5',
        )

        ax.plot(*long2xy(sign * 3 * length, delta, cog_x, cog_y), '*', mew=0, markersize=10, color='C5', zorder=3)
        ax.annotate(
            'Est. source position',
            xy=long2xy(sign * 3 * length, delta, cog_x, cog_y),
            xytext=(10 if sign < 0 else -10, 0),
            textcoords='offset points',
            color='C5',
            va='center',
            ha='left' if sign < 0 else 'right',
        )

        ax.annotate(
            r'\texttt{disp}' if sign < 0 else r'-\texttt{disp}',
            xy=long2xy(sign * 1.5 * length, delta, cog_x, cog_y),
            xytext=(-5, 5),
            textcoords='offset points',
            color='C5',
            va='bottom',
            ha='right'
        )

        fig.savefig(f'Plots/hillas_{num}.pdf')

    x, y = long2xy(sign * 3 * length, delta, cog_x, cog_y)
    ax.plot([x, 30], [y, 5], 'C6')

    x = np.mean([x, 30])
    y = np.mean([y, 5])
    ax.annotate(r'\texttt{theta}', xy=[x, y], xytext=(5, -5), textcoords='offset points', color='C6')
    fig.savefig('Plots/hillas_disp.pdf')
