"""Platform for sensor integration."""

from __future__ import annotations
from datetime import timedelta
import logging
from .deskpro import Deskpro 

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.const import UnitOfTemperature, UnitOfSoundPressure
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_VERIFY_SSL, CONF_PASSWORD

logger = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""

    dp = Deskpro(
        hostname=config[CONF_HOST],
        username=config[CONF_USERNAME],
        password=config[CONF_PASSWORD],
    )

    dpx = DeskproXMLSensor( dp= dp)
    add_entities(
        [
            dpx,
            DeskproTemperature(dpx),
            AmbientNoiseLevel(dpx),
            CurrentSoundLevel(dpx),
            RoomInUse(dpx),
            AlarmDetected(dpx),
            PeopleCount(dpx),
            Humidity(dpx),
        ]
    )

#
# BUGBUG: how do I configure this from the UI?
# different deployments will have different tolerances.
#
SCAN_INTERVAL = timedelta(seconds=5)

class DeskproXMLSensor( SensorEntity ):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = True

    def __init__(self, dp: Deskpro ):
        self.dp = dp
        return

    def update(self) -> None:
        self.dp.update()
        self._attr_native_value = 0

    def get(self, key ) -> Optional[str]:
        return self.dp.status[key]

    pass

class DeskproSensor(SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = True

    def __init__(self, dp: DeskproXMLSensor, key):
        self.dp = dp
        self.key = key
        return

    def update(self) -> None:
        self._attr_native_value = self.dp.get( self.key )

    pass


class AudioLevel(DeskproSensor):
    """SoundLevel and AmbientNoiseLevel"""

    _attr_native_unit_of_measurement = UnitOfSoundPressure.DECIBEL
    _attr_device_class = SensorDeviceClass.SOUND_PRESSURE

    def __init__(self, dp: DeskproXMLSensor, key):
        super().__init__(dp, key)


class AmbientNoiseLevel(AudioLevel):
    _attr_name = "Deskpro Ambient Noise Level"
    _attr_unique_id = "DeskproAmbientNoiseLevel"

    def __init__(self, dp: DeskproXMLSensor):
        super().__init__(dp, "AmbientNoiseLevel")
        return

    pass


class CurrentSoundLevel(AudioLevel):
    _attr_name = "Deskpro level of noise in the room now"
    _attr_unique_id = "DeskproSoundLevel"

    def __init__(self, dp: DeskproXMLSensor):
        super().__init__(dp, "SoundLevel")
        return

    pass


class DeskproTemperature(DeskproSensor):
    """Representation of a Sensor."""

    _attr_name = "DeskPro Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_unique_id = "0xdeadbeef"

    def __init__(self, dp: DeskproXMLSensor):
        super().__init__(dp, "AmbientTemperature")
        return


class PeopleCount(DeskproSensor):
    _attr_name = "Deskpro people count"
    _attr_unique_id = "peoplecountzzzz"

    def __init__(self, dp: DeskproXMLSensor):
        super().__init__(dp, "PeopleCount")
        return

    pass

class DeskproBinarySensor(BinarySensorEntity):

    _attr_state_class = None
    _attr_should_poll = True
    # You must set name, uid, device class.

    def __init__(self, attr:str, dp:DeskproXMLSensor):
        self.dp = dp
        self.attr = attr
        return
    
    @property
    def name(self):
        return self._name
    
    @property
    def is_on(self) -> bool:

        logger.debug( f"Deskpro state: {self.dp.dp.status}")

        current = self.dp.get(self.attr)

        if current is None:
            # BUGBUG: how do I say "unavailable?"
            return False

        if current.lower() == "true":
            return True
        elif current.lower() == "false":
            return False
        else:
            raise Exception(f"Unexpected value for {attr}: " + current)
        return
    pass # class
    
    
class RoomInUse(DeskproBinarySensor):
    _attr_name = "Deskpro in use"
    _attr_unique_id = "dpinuse"
    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    def __init__(self, dp: DeskproXMLSensor):
        super().__init__(attr="RoomInUse", dp=dp )
        self._name = "Deskpro in use"
        return
    pass


class AlarmDetected(DeskproBinarySensor):
    _attr_name = "T3 Alarm Detected"
    _attr_unique_id = "dpt3detect"
    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def __init__(self, dp: DeskproXMLSensor):
        super().__init__(attr="T3AlarmDetected", dp=dp)
        self._name="T3 Alarm Detected"
        return

    pass


class Humidity(DeskproSensor):
    _attr_name = "Deskpro Humidity"
    _attr_unique_id = "deskprohumidity"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "RelativeHumidity")
        return

    pass
