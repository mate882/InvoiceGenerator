from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'TRY': '₺',
}

@register.filter
def currency_symbol(code):
    return CURRENCY_SYMBOLS.get(code, '')
