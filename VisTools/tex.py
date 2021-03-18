import pandas as pd
import uncertainties as unc


def __form(x):
    # print(type(x))
    if type(x) == unc.Variable or type(x) == unc.AffineScalarFunc:
        return "${:.3fL}$".format(x)
    else:
        return x


__uuid = -1


def __get_uuid():
    global __uuid
    __uuid += 1
    return __uuid


def df_tolatex(table: pd.DataFrame, texfile: str, formatterfunc=__form):
    """takes a pandas DataFrame and creates a latex formatted table
    in the given file.

    (each column is evaluated by the formatter function in series)
    applicable inside table-environment

    Args:
        table: DataFrame
        texfile: output File
        formatterfunc: function to be run on all table entries

    returns:
        Nothing
    """

    table.to_latex(
        texfile,
        escape=False,
        formatters=[formatterfunc]*len(table.columns),
        index=False,
        encoding='utf-8')


# def unc_tolatex(
#     value: unc.core.Variable,
#     identifier: str,
#     texfile: str,
#     name='',
#     unit='',
#     formatting='4f'
# ):
#     """
#         creates or appends a .tex-file creating or
#         updating a command containing the uncertainty value
#     """
#     if identifier is None:
#         identifier = str(__get_uuid())

#     general1 = "\\ExplSyntaxOn\n"
#     general1 += "\\newcommand{\\pyval}[1]{%\n\t\\str_case:nn{#1}{%\n"
#     general2 = "\t}\n}\n\\ExplSyntaxOff"

#     if name != '':
#         name = name + " ="
#     newentry = f"\t\t{{ {identifier} }}{{ {name} \\SI{{"
#     newentry2 = ("{:." + formatting + "}").format(value)
#     newentry2 = newentry2.replace('(', ' ').replace(')', ' ').replace('/', '')
#     newentry += newentry2
#     newentry += f"}}{{ {unit} }}}}\n"

#     new = ""
#     content = ""

#     try:
#         with open(texfile, 'r') as f:
#             content = f.read()
#             # content = content[40:-57]
#             if content != "":
#                 content = content.splitlines(1)[3:-3]
#     except FileNotFoundError as e:
#         pass

#     with open(texfile, 'w+') as f:

#         done = False

#         for l in content:
#             if l.split()[1] == identifier:
#                 new += newentry
#                 done = True
#             else:
#                 new += l

#         if not done:
#             new += newentry

#         f.write(general1 + new + general2)


class TexWriter:

    def __init__(self, texfile):
        self.__texfile = texfile
        self.__tex_pre = "\\ExplSyntaxOn\n"
        self.__tex_pre += "\\newcommand{\\pyval}[1]{%\n"
        self.__tex_pre += "\t\\str_case:nn{#1}{%\n"
        self.__tex_post = "\t}\n}\n\\ExplSyntaxOff"

        self.__entries = {}
        self.__uuid = -1
    
    def __get_uuid(self):
        self.__uuid += 1
        return self.__uuid

    def add(
        self,
        value: unc.core.Variable,
        unit: str = None,
        identifier: str = None,
        name: str = None
    ):
        if identifier is None:
            identifier = str(self.__get_uuid())

        self.__entries[identifier] = {
            "value": value
        }

        if unit is not None:
            self.__entries[identifier]['unit'] = unit

        if name is not None:
            self.__entries[identifier]['name'] = name + ' ='

    def save(self, formatting: str = '4f'):
        newentries = []

        content = ""
        try: 
            with open(self.__texfile, 'r') as f:
                content = f.read()

                if content != "":
                    content = content.splitlines(1)[3:-3]
        except FileNotFoundError as e:
            pass

        for i, e in self.__entries.items():
            for j in range(len(content)):
                oldline = content[j]
                if oldline.split()[1] == i:
                    oldline = ''

            newline = f"\t\t{{ {i} }}{{ {e.get('name', '')} \\SI{{"
            newval = ("{:." + formatting + "}").format(e['value'])
            newval = newval.replace('(', ' ').replace(')', ' ').replace('/', '')
            newline += newval
            newline += f"}}{{ {e.get('unit', '')} }}}}\n"
            newentries.append(newline)


        with open(self.__texfile, "w+") as f:
            f.write(
                self.__tex_pre +
                ''.join([s for s in newentries]) +
                ''.join([s for s in content]) +
                self.__tex_post
            )


if __name__ == "__main__":
    u = unc.ufloat(9, .5)
    # unc_tolatex(u, 'l_mu', '../testing/test_val.tex', '$\lambda_\mu$')

    w = TexWriter("../testing/test_val.tex")
    w.add(u, identifier="lmu", name="$\lambda\mu$")
    w.save()
