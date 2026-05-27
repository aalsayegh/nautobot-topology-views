from nautobot.apps.ui import DistinctViewTab, TemplateExtension


class LocationTopologyTab(TemplateExtension):
    """Inject a Topology tab into the Location detail page."""

    model = "dcim.location"

    object_detail_tabs = (
        DistinctViewTab(
            tab_id="topology",
            label="Topology",
            url_name="plugins:nautobot_topology_views:location_topology",
            weight=1000,
        ),
    )


template_extensions = [LocationTopologyTab]
