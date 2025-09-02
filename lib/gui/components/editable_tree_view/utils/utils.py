import os
def rreal_size(args):
    return real_size(args, _round=True)

def real_size(args, _round=False):
    """
    This function is used to calculate the real size of the GUI elements
    :param args:
    :param _round:
    :return:
    """
    # get the dpi_ratio from the enviroment
    dpi_ratio = float(os.environ.get('DPI_RATIO', 0))
    if not dpi_ratio:
        dpi_ratio = 1

    elif isinstance(args, tuple):
        if _round:
            return tuple([round(arg * dpi_ratio) for arg in args])
        return tuple([arg * dpi_ratio for arg in args])
    elif isinstance(args, (int, float)):
        if _round:
            return round(args * dpi_ratio)
        return args * dpi_ratio
    else:
        raise ValueError(f"Invalid type: {type(args)}")