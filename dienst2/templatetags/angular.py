"""
jQuery templates use constructs like:
 
    {{if condition}} print something{{/if}}
 
This, of course, completely screws up Django templates,
because Django thinks {{ and }} mean something.
 
Wrap {% angular %} and {% endangular %} around those
blocks of jQuery templates and this will try its best
to output the contents with no changes.
"""

from django import template

register = template.Library()


class AngularNode(template.Node):
    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def angular(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endangular':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append('}}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('%}')
    return AngularNode(''.join(text))
