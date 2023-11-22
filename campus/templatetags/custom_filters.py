from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter(name='custom_timesince')
def custom_timesince_filter(value):
    """ 
        This is function returns the value of time past since a scheduled lecture to the current date. If the time past is in: 
            - minutes, return 'm',
            - hours, return 'h', 
            - days, return 'd',
            - weeks, return 'w',
        
        If all the above conditions are false, i.e. time past is less than a minute, then return 'Just now'.

        - My main aim was to mimic how Instagram displays time past since a logged in user uploaded his/her post to their News Feed.
    """
    
    time_diff = timesince(value)    # time difference

    (time_diff := time_diff.split(',')[0])  # split time and access the first value.

    if 'minute' in time_diff:
        return f"{time_diff[:2]}m"     # get the first 2 items in the str. value
    
    elif 'hour' in time_diff:
        return f"{time_diff[:2]}h"
    
    elif 'day' in time_diff:
        return f"{time_diff[:2]}d"
    
    elif 'week' in time_diff:
        return f"{time_diff[:2]}w"
    
    else:
        return 'Just now'