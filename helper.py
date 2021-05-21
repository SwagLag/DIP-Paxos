"""Helper functions"""

def determinenumdepth(num:int or float):
    """Recursively determines the significance of a given number before
    the dot."""
    if num >= 1:
        return 1 + determinenumdepth(num/10)
    else:
        return 0