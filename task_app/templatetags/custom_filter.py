from django import template

register = template.Library()


@register.filter(name='relative_page_list')
def relative_page_list(paginator, page_range):
    page_number = paginator.number
    last_page_number = paginator.paginator.page_range[-1]
    page_range = int(page_range)
    page_min = page_number - page_range
    page_max = page_number + page_range
    if page_min < 0:
        page_min = 0
    if page_max > last_page_number:
        page_max = last_page_number
    return list(list(paginator.paginator.page_range)[page_min:page_max])

