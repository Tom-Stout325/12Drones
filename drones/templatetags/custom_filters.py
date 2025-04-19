import os
from django import template

register = template.Library()

@register.filter
def is_pdf(file_url):
    return str(file_url).lower().endswith('.pdf')


# @register.filter
# def is_pdf(url):
#     return url.lower().endswith('.pdf')


@register.filter
def file_icon(file_url):
    ext = os.path.splitext(file_url)[1].lower()
    return {
        '.pdf': '📄',
        '.doc': '📝',
        '.docx': '📝',
        '.xls': '📊',
        '.xlsx': '📊',
        '.jpg': '🖼️',
        '.jpeg': '🖼️',
        '.png': '🖼️'
    }.get(ext, '📁')
