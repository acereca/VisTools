import uncertainties as unc


def unc_repr(name: str, unv: unc.core.Variable, unit='', formatting='e', aftercomma=2, addwidth=1, latex=True):
    """
        returning values given as uncertainties.ufloat, for jupyter notebook
    """
    width = aftercomma + addwidth + 1

    string = '{name} = ('.format(name=name)
    string += '{num:0{width}.{comma}{formatting}'
    if latex:
        string += 'L}'
    else:
        string += 'P}'

    string = string.format(num=unv, width=width, comma=aftercomma, formatting=formatting)
    string += ') ' + unit

    return string


def unc_pp(name: str, unv: unc.core.Variable, unit='', formatting='e', aftercomma=2, addwidth=1):
    print(unc_repr(name, unv, unit, formatting, aftercomma, addwidth, False))


def val_repr(name: str, nom: float, stdd=0, unit='', formatting='f', aftercomma=2, addwidth=1, latex=True):
    """
        pretty printing values given as seperate nominal and stddev values for jupyter notebook
    """
    width = aftercomma + addwidth + 1

    string = '{name} = '.format(name=name)

    if stdd != 0:
        string += '('

    string += '{num:0{width}.{comma}f}'.format(num=nom, width=width, comma=aftercomma)

    if stdd != 0:
        if latex:
            string += '\pm{num:0{width}.{comma}{fmt}})'.format(num=stdd, width=width, comma=aftercomma,
                                                               fmt=formatting)
            string += '\ '
        else:
            string += ' ± {num:0{width}.{comma}{fmt}})'.format(num=stdd, width=width, comma=aftercomma,
                                                             fmt=formatting)
            string += ' '

    string += unit
    return string


def val_pp(name: str, nom: float, stdd=0, unit='', formatting='f', aftercomma=2, addwidth=1):
    print(val_repr(name, nom, stdd, unit, formatting, aftercomma, addwidth, False))


if __name__ == "__main__":
    x = 102
    dx = 10.2

    xv = unc.ufloat(x, dx)

    val_pp("x", x, dx, 'cm')

    unc_pp("y", xv, 'm', formatting='f')
