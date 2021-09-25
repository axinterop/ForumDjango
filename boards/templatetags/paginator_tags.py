from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    """
    'Paginator.get_elided_page_range' method doesn't work properly with a big amount of pages.
    It uses the default value of 'number' (1) every time regardless of the current page number,
    so I implemented custom tag to solve this problem.
    """
    # TODO: Remove tag when 'get_elided_page_range' will be fixed
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number,
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)
