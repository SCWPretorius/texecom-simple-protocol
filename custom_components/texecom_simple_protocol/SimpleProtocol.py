"""The SimpleProtocol integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant

class SimpleProtocol:
    """SimpleProtocol class."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the SimpleProtocol class."""
        self._hass = hass
