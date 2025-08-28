"""Defines a :class:`.Stardate` class to abstract an instant in time."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

import numpy as np

from .. import constants as CONST

AD_OFFSET: float = 1721424.5
"""Number of days from _noon_ of Janurary 1, 4713 BC to _midnight_ of January 1, 1 AD."""


class DayFrac:
    """Number of elapsed days since _noon_ of January 1, 4713 BC."""

    def __init__(self, days_a: float, days_b: float = 0.0):
        """Instantiate a :class:`.DayFrac` instance from a two-part Julian day number.

        Args:
            days_a: Portion (or whole part) of Julian day number being represented.
            days_b: Portion (or whole part) of Julian day number being represented.
        """
        self._days_a = days_a
        self._days_b = days_b

    @property
    def days(self) -> float:
        """Returns the sum of the specified two-part Julian day number."""
        return self._days_a + self._days_b

    def toDatetime(self) -> DatetimeExt:
        """Convert this :class:`.DayFrac` to a :class:`.DatetimeExt`."""
        mod_ad_jd = self.days - AD_OFFSET
        mod_ad_day = int(np.floor(mod_ad_jd))
        dt = datetime.fromordinal(mod_ad_day)
        day_frac = mod_ad_jd - mod_ad_day

        hour_remainder = day_frac * CONST.DAYS2HOUR
        hour = int(np.floor(hour_remainder))
        minute_remainder = (hour_remainder - hour) * CONST.HOUR2MINUTE
        minute = int(np.floor(minute_remainder))
        second_remainder = (minute_remainder - minute) * CONST.MINUTE2SEC
        second = int(np.floor(second_remainder))
        micro = int(np.round((second_remainder - second) * 1e6))
        dt = dt.replace(hour=hour, minute=minute, second=second, microsecond=micro)
        return DatetimeExt(dt)


class DatetimeExt:
    """Extended functionality encapsulated with a Python `datetime`."""

    def __init__(self, dt: datetime):
        """Instantiate a :class:`.DatetimeExt` from specified `datetime`.

        Args:
            dt: Specified Python `datetime` object.
        """
        self._dt = dt

    @property
    def year(self) -> int:
        return self._dt.year

    @property
    def month(self) -> int:
        return self._dt.month

    @property
    def day(self) -> int:
        return self._dt.day

    @property
    def hour(self) -> int:
        return self._dt.hour

    @property
    def minute(self) -> int:
        return self._dt.minute

    @property
    def second(self) -> float:
        return self._dt.second + self._dt.microsecond * 1e-6

    def toDayFrac(self) -> DayFrac:
        """Convert this :class:`.DatetimeExt` to a :class:`.DayFrac`."""
        days = AD_OFFSET + self._dt.toordinal()
        day_frac = self.second / CONST.DAYS2SEC
        day_frac += self.minute / (CONST.DAYS2HOUR * CONST.HOUR2MINUTE)
        day_frac += self.hour / CONST.DAYS2HOUR
        return DayFrac(days, day_frac)


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
