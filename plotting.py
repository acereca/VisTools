import uncertainties
import matplotlib as mpl

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
        unc: uncertainties.unumpy,
        trailing = 3,
        name = "",
        data_pos = (0,0)
    ):

    """
        Annotate an uncertain value (unumpy.ufloat) with name in scientific
        representation (Latex enabled)
    """

    if name != "":
        name = name + " = "

    fig.annotate(
        '${}{:.{trailing}eL}$'.format(name, unc, trailing=trailing),
        xy=data_pos,
        xycoords='data',
        xytext=(0, 0),
        textcoords='offset points',
        fontsize=14,
        bbox=dict(boxstyle="round",
        fc="1")
    )

def annotate(fig: mpl.figure.Figure, value: str, data_pos=(0,0)):
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
