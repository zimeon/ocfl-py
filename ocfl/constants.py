"""Constants for OCFL package."""

INVENTORY_FILENAME = "inventory.json"
"""str: filename of the inventory within OCFL object root and version directories."""

SPEC_VERSIONS_SUPPORTED = ("1.0", "1.1")
"""tuple of str: OCFL specification version numbers supported by ocfl-py."""

DEFAULT_SPEC_VERSION = "1.1"
"""str: OCFL specification version number to assume if none specified."""

DEFAULT_DIGEST_ALGORITHM = "sha512"
"""str: default digest algorithm to use for content addressing."""

DEFAULT_CONTENT_DIRECTORY = "content"
"""str: default content directy name if none is specified."""
