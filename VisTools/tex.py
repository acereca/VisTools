import pandas as pd
import uncertainties as unc

def __form(x):
    #print(type(x))
    if type(x) == unc.Variable or type(x) == unc.AffineScalarFunc:
        return "${:.3fL}$".format(x)
    else:
        return x

def df_tolatex(table: pd.DataFrame, texfile: str, formatterfunc = __form):
    """
        takes a pandas DataFrame and creates a latex formatted table in the given file.
        (each column is evaluated by the formatter function in series)
        applicable inside table-environment
    """

    table.to_latex(texfile, escape=False, formatters=[formatterfunc]*len(table.columns), index = False, encoding='utf-8')


def unc_tolatex(value: unc.Variable, id: str,  texfile: str):
    """
        creates a texfile containing a command containing the uncertainty value
    """

    general1 = """\newcommand{\val}[2]{%
        \IfEqCase{#1}{%"""
    general2 = """}[\PackageError{unc_tolatex}{undefinded value: #1}{}]%
    }"""

    with open(texfile, 'r+') as f:
        content = f.read()

        if content.startswith(general1) and content.endswith(general2):
            vallines = content[len(general1):len(general2)]

        if 
