from nautobot.apps import NautobotAppConfig


class TopologyViewsConfig(NautobotAppConfig):
    name = "nautobot_topology_views"
    verbose_name = "Topology Views"
    description = "A Nautobot App to render topology maps"
    version = "1.0.0"
    author = "Mattijs Vanhaverbeke"
    author_email = "author@example.com"
    base_url = "topology-views"
    required_settings = []
    default_settings = {
        "static_image_directory": "nautobot_topology_views/img",
        "allow_coordinates_saving": False,
        "always_save_coordinates": False,
    }
    docs_view_name = "plugins:nautobot_topology_views:docs"

    def ready(self):
        from . import signals

        super().ready()


config = TopologyViewsConfig
