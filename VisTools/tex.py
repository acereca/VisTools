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


def unc_tolatex(value: unc.core.Variable, identifier: str, texfile: str, name=''):
    """
        creates or appends a .tex-file creating or updating a command containing the uncertainty value
    """

    general1 = "\\newcommand{\\val}[2]{%\n\t\\IfEqCase{#1}{%\n"
    general2 = "\t}[\\PackageError{unc_tolatex}{undefinded value: #1}{}]%\n}"

    if name != '': name = name + " ="
    newentry = "\t\t{{ {id} }}{{ {name} \\SI{{ {nom}+-{std} }}{{ {unit} }}}}\n".format(id=identifier, name=name, nom=value.n, std=value.s, unit="")

    new = ""
    #content = ""

    with open(texfile, 'w+') as f:
        content = f.read()
        #content = content[40:-57]
        if content != "":
            content = content.splitlines(1)[2:-2]

    with open(texfile, 'w') as f:

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
