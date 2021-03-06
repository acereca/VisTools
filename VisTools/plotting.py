import uncertainties as unc
import uncertainties.unumpy as unp
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import pandas as pd
from typing import List, Callable, Union, Iterable


def annotate_val(
        fig: mpl.figure.Figure,
        value: float,
        error: float,
        trailing = 3,
        name = "",
        data_pos = (0,0),
        formatting = "e",
        unit = ""
    ):

    """
        Annotate a value (and error) with name in scientific
        representation (Latex enabled)
    """

    if name != "":
        name = name + " = "
    if unit != "":
        unit = " $" + unit + "$"

    fig.annotate(
        '${}{:.{trailing}{format}}\pm{:.{trailing}{format}}${unit}'.format(
            name,
            value,
            error,
            trailing=trailing,
            format=formatting,
            unit=unit
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
        data_pos=(0, 0),
        formatting = "e",
        unit = "",
        bbox_ec= '1',
        **kwargs
    ):

    """
        Annotate an uncertain value (uncertainties.ufloat()) with name in scientific
        representation (Latex enabled)
    """

    if name != "":
        name = name + " = "
    if unit != "":
        unit = " $" + unit + "$"

    fig.annotate(
        '${}{:.{trailing}{format}L}${unit}'.format(
            name,
            value,
            trailing=trailing,
            format=formatting,
            unit=unit
        ),
        xy=data_pos,
        xycoords='data',
        xytext=(0, 0),
        textcoords='offset points',
        fontsize=14,
        bbox={
            'boxstyle':"round",
            'fc':"1",
            'ec':bbox_ec
        },
        **kwargs
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


def fit(
    data_x, 
    data_y, 
    fitfunc: Callable, 
    init: Union[None, int, float, complex], 
    sigma=None, 
    fitlabel='fitted', 
    fig=None,
    c=None
) -> List[unc.core.Variable]:

    """
        Take a set of data points and fit the fitfunc to these points
    """

    pfinal, pcov = opt.curve_fit(
        fitfunc,
        data_x,
        data_y,
        p0=init,
        sigma=sigma,
        #absolute_sigma = True
    )

    if fig != None:
        xdata_gen = np.linspace(np.min(data_x), np.max(data_x), 101)
        fig.plot(
            xdata_gen,
            fitfunc(xdata_gen, *pfinal),
            label=fitlabel.format(m=pfinal[0], c=pfinal[1]),
            color = c,
            antialiased=True
        )

    return unp.uarray(pfinal, np.sqrt(np.diag(pcov)).tolist())


def fit_linear(
    data_x, 
    data_y, 
    p0, 
    sigma=None, 
    fitlabel='linear fit', 
    fig=None,
    c=None,
    **kwargs
) -> List[unc.core.Variable]:

    """
        Take a set of data points and fit these points with a linear function
    """

    ffunc = lambda x, m, c: x*m+c

    return fit(data_x, data_y, ffunc, p0, sigma, fitlabel, fig, c, **kwargs)

def lm_plot(
    data: pd.DataFrame, 
    x: str, 
    y: str, 
    xerr: str, 
    yerr: str,
    fitlabel: str,
    fig = plt,
    color = None
) -> List[unc.core.Variable]:

    """
        Takes set of data points, plots them and does a fit_linear() call using it
    """

    ffunc = lambda x, m, c: x*m+c

    if yerr != None:
        sigma = data[yerr]
    else:
        sigma = None

    ret = fit_linear(
        data[x], 
        data[y],
        (0, 0),
        sigma,
        fitlabel,
        fig,
        color
    )

    fig.fill_between(
        data[x], 
        ffunc(data[x], *(unp.nominal_values(ret) + unp.std_devs(ret))),
        ffunc(data[x], *(unp.nominal_values(ret) - unp.std_devs(ret))),
        color = color, 
        alpha = 0.2, 
        label = None#'68% CI'
    )

    print("lm fit:\n\ty = m * x + c\n\n\tm: {:.3eP}\n\tc: {:.3eP}\n".format(*ret))

    return ret

def fit_polynomial(
        data_x: Union[np.ndarray, Iterable],
        data_y: Union[np.ndarray, Iterable],
        deg: int,
        residuals=False
) -> List[unc.core.Variable]:

    """
        Take a set of data points and fit these points with a polynomial of a given degree
        :return: polynomial coefficients in order of highest to lowest degree
    """
    pcoef, pcov = np.polyfit(data_x, data_y, deg, full = residuals, cov=(not residuals))

    if not residuals:
        print()
    else:
        print()

    return unp.uarray(pcoef, np.sqrt(np.diag(pcov)).tolist())

if __name__ == "__main__":

    print()
