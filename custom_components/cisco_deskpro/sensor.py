"""Platform for sensor integration."""

from __future__ import annotations
from datetime import timedelta

from deskpro import Deskpro 

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, UnitOfSoundPressure
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_VERIFY_SSL, CONF_PASSWORD


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
    add_entities(
        [
            DeskproTemperature(dp),
            AmbientNoiseLevel(dp),
            CurrentSoundLevel(dp),
            # RoomInUse(dp),
            # AlarmDetected(dp),
            PeopleCount(dp),
            Humidity(dp),
        ]
    )


SCAN_INTERVAL = timedelta(seconds=30)


class DeskproSensor(SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = True

    def __init__(self, dp: Deskpro, key):
        self.dp = dp
        self.key = key
        return

    def update(self) -> None:
        self.dp.update()
        self._attr_native_value = self.dp.status[self.key]

    pass


class AudioLevel(DeskproSensor):
    """SoundLevel and AmbientNoiseLevel"""

    _attr_native_unit_of_measurement = UnitOfSoundPressure.DECIBEL
    _attr_device_class = SensorDeviceClass.SOUND_PRESSURE

    def __init__(self, dp: Deskpro, key):
        super().__init__(dp, key)


class AmbientNoiseLevel(AudioLevel):
    _attr_name = "Deskpro Ambient Noise Level"
    _attr_unique_id = "DeskproAmbientNoiseLevel"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "AmbientNoiseLevel")
        return

    pass


class CurrentSoundLevel(AudioLevel):
    _attr_name = "Deskpro level of noise in the room now"
    _attr_unique_id = "DeskproSoundLevel"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "SoundLevel")
        return

    pass


class DeskproTemperature(DeskproSensor):
    """Representation of a Sensor."""

    _attr_name = "DeskPro Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_unique_id = "0xdeadbeef"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "AmbientTemperature")
        return


class PeopleCount(DeskproSensor):
    _attr_name = "Deskpro people count"
    _attr_unique_id = "peoplecountzzzz"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "PeopleCount")
        return

    pass


class RoomInUse(DeskproSensor):
    _attr_name = "Deskpro in use"
    _attr_unique_id = "dpinuse"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "RoomInUse")
        return

    pass


class AlarmDetected(DeskproSensor):
    _attr_name = "T3 Alarm Detected"
    _attr_unique_id = "dpt3detect"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "T3AlarmDetected")
        return

    pass


class Humidity(DeskproSensor):
    _attr_name = "Deskpro Humidity"
    _attr_unique_id = "deskprohumidity"

    def __init__(self, dp: Deskpro):
        super().__init__(dp, "RelativeHumidity")
        return

    pass
