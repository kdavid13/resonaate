"""Defines a :class:`.Stardate` class to abstract an instant in time."""
from __future__ import annotations

# Standard Library Imports
from datetime import datetime
from enum import Enum

# Third Party Imports
import numpy as np

# Local Imports
from .. import constants as CONST

AD_OFFSET: float = 1721424.5
"""Number of days from _noon_ of Janurary 1, 4713 BC to _midnight_ of January 1, 1 AD."""


class DayFrac(float):
    """Number of elapsed days since _noon_ of January 1, 4713 BC."""

    def toDatetime(self) -> DatetimeExt:
        """Convert this :class:`.DayFrac` to a :class:`.DatetimeExt`."""
        mod_ad_jd = self - AD_OFFSET
        mod_ad_day = int(np.floor(mod_ad_jd))
        _date = datetime.fromordinal(mod_ad_day)
        day_frac = mod_ad_jd - mod_ad_day

        hour_remainder = day_frac * CONST.DAYS2HOUR
        hour = int(np.floor(hour_remainder))
        minute_remainder = (hour_remainder - hour) * CONST.HOUR2MINUTE
        minute = int(np.floor(minute_remainder))
        second_remainder = (minute_remainder - minute) * CONST.MINUTE2SEC
        second = int(np.floor(second_remainder))
        micro = int(np.round((second_remainder - second) * 1e6))
        return DatetimeExt(_date.year, _date.month, _date.day, hour, minute, second, micro)


class DatetimeExt(datetime):
    """Extended functionality encapsulated with a Python `datetime`."""

    @property
    def sec_frac(self) -> float:
        """Converts internal :attr:`.microsecond` value to floating point second fraction."""
        return self.microsecond * 1e-6

    def toDayFrac(self) -> DayFrac:
        """Convert this :class:`.DatetimeExt` to a :class:`.DayFrac`."""
        days = AD_OFFSET + self.toordinal()
        day_frac = (self.second + self.sec_frac) / CONST.DAYS2SEC
        day_frac += self.minute / (CONST.DAYS2HOUR * CONST.HOUR2MINUTE)
        day_frac += self.hour / CONST.DAYS2HOUR
        return DayFrac(days + day_frac)


class SecDelta:
    """Number of seconds since specified origin."""

    def __init__(self, sec: float, origin: Stardate):
        """Instantiate a :class:`.SecDelta` instance.

        Args:
            sec: Number of seconds that have passed since `origin`.
            origin: Specified instant in time to measure `sec` from.

        Todo:
            Would be nice to have an elegant way to generate an analagous `ScenarioTime` without
            needing to specify the origin...
        """
        self._sec = sec
        self._origin = origin


class TimeScale(Enum):
    """Enumeration of supported time scales."""

    TAI = "TAI"
    """International Atomic Time"""

    UT1 = "UT1"
    """Universal Time"""

    UTC = "UTC"
    """Coordinated Universal Time"""

    TT = "TT"
    """Terrestrial Time"""


class Stardate:
    """Abstracts an instant in time."""

    def __init__(self, time_val: DayFrac | SecDelta | datetime, scale: TimeScale):
        """Instantiate a :class:`.Stardate`.

        Args:
            time_val: The value of time being represented.
            scale: The scale of the `time_val`. Not all seconds are equal!
        """
        self._time_val = time_val
        if isinstance(self._time_val, datetime):
            self._time_val = DatetimeExt(self._time_val)
        self._scale = scale
