import markdown
import nh3
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "del",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "ul",
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "code": {"class"},
}

ALLOWED_URL_SCHEMES = {"http", "https", "mailto"}


@register.filter
def render_markdown(text: str) -> str:
    rendered = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "extra"],
    )

    sanitized = nh3.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
        strip_comments=True,
    )

    return mark_safe(sanitized)
