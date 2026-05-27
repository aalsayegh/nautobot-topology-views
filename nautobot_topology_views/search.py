"""Search indexes for Nautobot Topology Views."""

from nautobot.apps.search import SearchFilterSet

from .models import Coordinate, CoordinateGroup


class CoordinateGroupSearchFilterSet(SearchFilterSet):
    """Search filter set for CoordinateGroup model."""

    class Meta:
        model = CoordinateGroup
        fields = ["name", "description"]


class CoordinateSearchFilterSet(SearchFilterSet):
    """Search filter set for Coordinate model."""

    class Meta:
        model = Coordinate
        fields = ["group", "device"]
