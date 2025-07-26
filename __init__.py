import logging
import re
import asyncio

_LOGGER = logging.getLogger(__name__)

DOMAIN = "came_watchdog"

PATTERN_DOWN = re.compile(r"Server goes offline\.", re.I)
PATTERN_UP = re.compile(r"Successful authorization\.", re.I)

def safe_restart(hass):
    _LOGGER.warning("♻️ Watchdog: Invio richiesta riavvio tramite servizio homeassistant.restart")
    hass.loop.call_soon_threadsafe(
        lambda: hass.async_create_task(
            hass.services.async_call("homeassistant", "restart")
        )
    )


class CameLogHandler(logging.Handler):
    """Handler che intercetta solo i log di CAME Manager."""

    def __init__(self, hass):
        super().__init__()
        self.hass = hass
        self.state_offline = False

    def emit(self, record):
        logger_name = record.name
        if "custom_components.came.pycame.came_manager" not in logger_name:
            return
        try:
            msg = self.format(record)
        except Exception:
            return

        if PATTERN_DOWN.search(msg):
            _LOGGER.warning("🛑 Watchdog: ETI Domo DOWN rilevato")
            self.state_offline = True

        elif PATTERN_UP.search(msg) and self.state_offline:
            _LOGGER.warning("✅ Watchdog: ETI Domo UP rilevato, riavvio Home Assistant")
            self.state_offline = False
            safe_restart(self.hass)

async def async_setup(hass, config):
    """Setup asincrono del componente."""
    handler = CameLogHandler(hass)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logging.getLogger("custom_components.came.pycame.came_manager").addHandler(handler)

    _LOGGER.info("🐶 Watchdog CAME inizializzato e in ascolto SOLO dei log di came_manager.")
    return True

