# GitHub Copilot Instructions — nautobot-topology-views

## Project Overview

This is **nautobot-topology-views**, a Nautobot App (plugin) that renders network topology maps. It was converted from the `netbox-topology-views` v4.5.1 NetBox plugin to target **Nautobot 3.1.3**, **Python 3.12**, **Django 5.2**, managed with **Poetry**.

The package is `nautobot_topology_views` (Python module) / `nautobot-topology-views` (PyPI/Poetry).

---

## Tech Stack

- **Runtime**: Python 3.12, Django 5.2, Nautobot 3.1.3
- **Package manager**: Poetry (`pyproject.toml`) — no `setup.py`
- **Linting/formatting**: `ruff` + `black` (line length 120)
- **Tests**: `pytest` + `pytest-django`
- **Shell**: Fish shell — use `.venv/bin/python` or `.venv/bin/nautobot-server` directly; do NOT `source .venv/bin/activate`

---

## Nautobot App Conventions

### App Config (`__init__.py`)
- Inherits `NautobotAppConfig` from `nautobot.apps`
- App name: `"nautobot_topology_views"`, base_url: `"topology-views"`

### Key Verified Import Paths (Nautobot 3.1.3)

| What | Import path |
|------|-------------|
| `Role` | `nautobot.extras.models` |
| `Tag` | `nautobot.extras.models` |
| `Device`, `DeviceType`, `Manufacturer`, `Platform`, `VirtualChassis` | `nautobot.dcim.models` |
| `Location`, `Rack`, `Cable`, `CableTermination`, `Interface`, `FrontPort`, `RearPort`, `PowerPort`, `PowerFeed`, `PowerPanel` | `nautobot.dcim.models` |
| `Circuit`, `CircuitTermination`, `ProviderNetwork` | `nautobot.circuits.models` |
| `NautobotAppConfig` | `nautobot.apps` |
| `NautobotModelForm`, `NautobotFilterForm`, `CSVModelForm`, `DynamicModelMultipleChoiceField`, `TagFilterField`, `add_blank_choice` | `nautobot.apps.forms` |
| `NautobotFilterSet`, `MultiValueCharFilter`, `MultiValueMACAddressFilter`, `TreeNodeMultipleChoiceFilter` | `nautobot.apps.filters` |
| `ObjectView`, `ObjectEditView`, `ObjectDeleteView`, `ObjectListView`, `BulkImportView` | `nautobot.apps.views` |
| `ObjectChangeLogView` | `nautobot.extras.views` (**not** `nautobot.apps.views`) |
| `BOOLEAN_WITH_BLANK_CHOICES` | `nautobot.core.forms` |
| `LocalContextFilterForm` | `nautobot.extras.forms` |
| `TenancyFilterForm` | `nautobot.tenancy.forms` |
| `TenancyModelFilterSetMixin` | `nautobot.tenancy.filter_mixins` |
| `LocatableModelFilterSetMixin` | `nautobot.dcim.filter_mixins` |
| `LocatableModelFilterFormMixin` | `nautobot.dcim.form_mixins` |
| `BaseTable` | `nautobot.apps.tables` |
| `NautobotModelViewSet` (API) | `nautobot.apps.api` |
| `NautobotModelSerializer` (API) | `nautobot.apps.api` |

### What Does NOT Exist in Nautobot 3.1.3

- `Site`, `SiteGroup`, `Region` → replaced by `Location` hierarchy (`nautobot.dcim.models.Location`)
- `WirelessLink` → not present
- `SavedFilter` → not present
- `ConfigTemplate` → not present
- `DeviceAirflowChoices` / `Device.airflow` field → not present
- `LocalConfigContextFilterSet` / `LocalConfigContextFilterForm` → replaced by `LocalContextFilterForm` from `nautobot.extras.forms`
- `ContactModelFilterSet` / `ContactModelFilterForm` → not present
- `TenancyFilterSet` → replaced by `TenancyModelFilterSetMixin` from `nautobot.tenancy.filter_mixins`
- `NautobotBulkImportForm` → replaced by `CSVModelForm` from `nautobot.apps.forms`
- `FieldSet` (from NetBox's `nautobot.utilities.forms.rendering`) → does not exist; use `field_order = [...]` plain lists on filter forms instead
- `nautobot.utilities.forms` → use `nautobot.apps.forms` or `nautobot.core.forms`

### Field/Model Changes from NetBox → Nautobot

- `Device.site` → `Device.location` (FK to `dcim.Location`)
- `PowerPanel.site` → `PowerPanel.location`
- `CircuitTermination._site_id` → `CircuitTermination.location_id`
- `CircuitTermination._provider_network` → `CircuitTermination.provider_network` (direct FK)
- `Device.objects.restrict(user, 'view')` — this **does** exist in Nautobot (via `nautobot.core.models.querysets`)
- Permission `"dcim.view_site"` → `"dcim.view_location"`
- FK target `'dcim.Role'` → `'extras.Role'`

### Form Patterns

- Filter forms: use `field_order = [...]` (plain list), NOT `fieldsets`
- Model forms: inherit `NautobotModelForm`; no `fieldsets` attribute needed
- Bulk import forms: inherit `CSVModelForm`

### URL Patterns

- All `path()` entries **must** have a `name=` argument — Nautobot sorts URL patterns by name at startup and crashes on `None`
- `ObjectChangeLogView` must be imported from `nautobot.extras.views`, not `nautobot.apps.views`

---

## Model Caveats

### `RoleImage.role_data` (was `role`)

The `RoleImage` model has a Python property named `role_data` (renamed from `role`). **Do not rename it back to `role`**. Nautobot's `RoleModelsQuery.list_subclasses()` in `nautobot.extras.utils` calls `model_class._meta.get_field("role")` on any model that `hasattr(model_class, "role")`. A Python property named `role` on a non-role model causes a `FieldDoesNotExist` crash at Django startup.

---

## Development Workflow

### Running makemigrations (without full dev stack)

Use the minimal migration config that avoids Redis and PostgreSQL:

```bash
.venv/bin/nautobot-server --config-path development/nautobot_config_migrations.py makemigrations nautobot_topology_views
```

`development/nautobot_config_migrations.py` uses SQLite in-memory + `constance.backends.memory.MemoryBackend`.

### Running with full dev stack

```bash
.venv/bin/nautobot-server --config-path development/nautobot_config.py <command>
```

Requires PostgreSQL and Redis running (see `development/docker-compose.postgres.yml`).

### Python environment

```bash
# Run nautobot-server
.venv/bin/nautobot-server --config-path development/nautobot_config.py shell

# Run tests
.venv/bin/pytest

# Lint
.venv/bin/ruff check nautobot_topology_views/
.venv/bin/black --check nautobot_topology_views/
```

---

## Migrations

- Old NetBox migrations (`0001_initial` through `0013_*`) were deleted during conversion
- A new `nautobot_topology_views/migrations/0001_initial.py` was generated for Nautobot 3.1.3
- Migration app label is `nautobot_topology_views`

---

## Static Assets & Frontend

- Built frontend assets live in `nautobot_topology_views/static/netbox_topology_views/`
- Source lives in `nautobot_topology_views/static_dev/` (JS/SCSS)
- Build entry point: `static_dev/bundle.js` (uses package.json)
