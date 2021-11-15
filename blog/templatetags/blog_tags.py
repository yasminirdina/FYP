from django import template
import math
register = template.Library()

@register.filter
def divide(value, arg):
    result = 0

    if value % arg == 0:
        return int(value / arg)
    else:
        return math.ceil(value / arg)
    """ try:
        return int(int(value) / int(arg))
    except (ValueError, ZeroDivisionError):
        return None """