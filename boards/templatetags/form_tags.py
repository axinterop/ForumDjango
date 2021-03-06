from django import template

register = template.Library()


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = "is-invalid"
        elif bound_field.widget_type != 'password':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)
