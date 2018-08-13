import pandas as pd
import uncertainties as unc

def __form(x):
    #print(type(x))
    if type(x) == unc.Variable or type(x) == unc.AffineScalarFunc:
        return "${:.3fL}$".format(x)
    else:
        return x

__uuid = -1
def __get_uuid():
    global __uuid
    __uuid += 1
    return __uuid

def df_tolatex(table: pd.DataFrame, texfile: str, formatterfunc = __form):
    """takes a pandas DataFrame and creates a latex formatted table in the given file.

    (each column is evaluated by the formatter function in series)
    applicable inside table-environment

    Args:
        table: DataFrame
        texfile: output File
        formatterfunc: function to be run on all table entries
    
    returns:
        Nothing
    """

    table.to_latex(texfile, escape=False, formatters=[formatterfunc]*len(table.columns), index = False, encoding='utf-8')


def unc_tolatex(value: unc.core.Variable, identifier: str, texfile: str, name='', unit=''):
    """
        creates or appends a .tex-file creating or updating a command containing the uncertainty value
    """
    if identifier == None:
        identifier = str(__get_uuid())

    general1 = "\\ExplSyntaxOn\n\\newcommand{\\pyval}[1]{%\n\t\\str_case:nn{#1}{%\n"
    general2 = "\t}\n}\n\\ExplSyntaxOff"

    if name != '': name = name + " ="
    newentry = f"\t\t{{ {identifier} }}{{ {name} \\SI{{" + \
    "{:.4f}+-{:.4f}".format(value.n, value.s) + \
        f"}}{{ {unit} }}}}\n"

    new = ""
    content = ""

    try:
        with open(texfile, 'r') as f:
            content = f.read()
            #content = content[40:-57]
            if content != "":
                content = content.splitlines(1)[3:-3]
    except FileNotFoundError as e:
        pass

    with open(texfile, 'w+') as f:

        done = False

        for l in content:
            if l.split()[1] == identifier:
                new += newentry
                done = True
            else:
                new += l

        if not done:
            new += newentry

        f.write(general1 + new + general2)

if __name__ == "__main__":
    u = unc.ufloat(9,.4)
    unc_tolatex(u, 'l_mu', '../testing/test_val.tex', '$\lambda_\mu$')
