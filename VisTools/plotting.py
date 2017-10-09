import uncertainties as unc
import uncertainties.unumpy as unp
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from typing import List, Callable, Union


def annotate_val(
        fig: mpl.figure.Figure,
        value: float,
        error: float,
        trailing = 3,
        name = "",
        data_pos = (0,0)
    ):

    """
        Annotate a value (and error) with name in scientific
        representation (Latex enabled)
    """

    if name != "":
        name = name + " = "

    fig.annotate(
        '${}{:.{trailing}e}\pm{:.{trailing}e}$'.format(
            name,
            value,
            error,
            trailing=trailing
        ),
        xy=data_pos,
        xycoords='data',
        xytext=(0, 0),
        textcoords='offset points',
        fontsize=14,
        bbox=dict(boxstyle="round",
        fc="1")
    )


def annotate_unc(
        fig: mpl.figure.Figure,
        value: unc.core.Variable,
        trailing=3,
        name="",
        data_pos=(0, 0)
    ):

    """
        Annotate an uncertain value (uncertainties.ufloat()) with name in scientific
        representation (Latex enabled)
    """

    if name != "":
        name = name + " = "

    fig.annotate(
        '${}{:.{trailing}eL}$'.format(name, value, trailing=trailing),
        xy=data_pos,
        xycoords='data',
        xytext=(0, 0),
        textcoords='offset points',
        fontsize=14,
        bbox=dict(boxstyle="round",
        fc="1")
    )


def annotate(fig: mpl.figure.Figure, value: str, data_pos=(0, 0)):
    """
        Annotate a str
    """
    fig.annotate(
        value,
        xy=data_pos,
        xycoords='data',
        xytext=(0, 0),
        textcoords='offset points',
        fontsize=14,
        bbox=dict(boxstyle="round",
        fc="1")
    )


def fit(data_x, data_y, fitfunc: Callable, init: Union[None, int, float, complex], sigma) -> List[unc.core.Variable]:

    """
        Take a set of data points and fit the fitfunc to these points
    """

    pfinal, pcov = opt.curve_fit(
        fitfunc,
        data_x,
        data_y,
        p0=init,
        sigma=sigma
    )

    return unp.uarray(pfinal, np.sqrt(np.diag(pcov)).tolist())


def fit_linear(data_x, data_y, p0, sigma) -> List[unc.core.Variable]:

    """
        Take a set of data points and fit these points with a linear function
    """

    ffunc = lambda x, m, c: x*m+c

    return fit(data_x, data_y, ffunc, p0, sigma)


if __name__ == "__main__":

    print()