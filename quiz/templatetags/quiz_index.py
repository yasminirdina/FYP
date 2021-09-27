from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    if minutes != 0 and seconds != 0:
        return '{} minit {} saat'.format(minutes, seconds)
    elif minutes == 0:
        return '{} saat'.format(seconds)
    elif seconds == 0:
        return '{} minit'.format(minutes)