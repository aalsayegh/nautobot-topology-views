from django import template

register = template.Library()

# Query params that are internal state, not user-visible filters
_SKIP_PARAMS = frozenset({"csrfmiddlewaretoken", "draw_init", "page", "per_page", "sort"})


def _resolve_display_value(field, raw_value):
    """Convert a raw query-param string to a human-readable label."""
    # ModelChoiceField / DynamicModelMultipleChoiceField → look up object name
    if hasattr(field, "queryset"):
        try:
            obj = field.queryset.get(pk=raw_value)
            return str(obj)
        except Exception:
            return raw_value

    # ChoiceField / MultipleChoiceField → match against choices list
    choices = getattr(field, "choices", None)
    if choices:
        for choice_value, choice_label in choices:
            if str(choice_value) == str(raw_value):
                return str(choice_label)

    # Boolean strings
    if str(raw_value).lower() == "true":
        return "Yes"
    if str(raw_value).lower() == "false":
        return "No"

    return raw_value


@register.inclusion_tag("nautobot_topology_views/inc/applied_filters.html")
def topology_applied_filters(filter_form, request):
    """
    Render a row of "applied filter" chips for all non-empty query parameters
    that correspond to fields on filter_form.  Each chip has an × link that
    removes that specific value from the current query string.
    """
    active_filters = []

    if not filter_form or not request.GET:
        return {"active_filters": active_filters}

    for field_name, field in filter_form.fields.items():
        if field_name in _SKIP_PARAMS:
            continue

        values = [v for v in request.GET.getlist(field_name) if v]
        if not values:
            continue

        label = str(field.label) if field.label else field_name.replace("_", " ").title()

        for value in values:
            display_value = _resolve_display_value(field, value)

            # Build the remove URL: current params minus this one value
            new_params = request.GET.copy()
            remaining = [v for v in new_params.getlist(field_name) if v != value]
            if remaining:
                new_params.setlist(field_name, remaining)
            else:
                try:
                    del new_params[field_name]
                except KeyError:
                    pass

            remove_url = ("?" + new_params.urlencode()) if new_params else "."

            active_filters.append(
                {
                    "label": label,
                    "value": display_value,
                    "remove_url": remove_url,
                }
            )

    return {"active_filters": active_filters}
