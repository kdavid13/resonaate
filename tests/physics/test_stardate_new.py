
from datetime import datetime

import pytest

from resonaate.physics.time.stardate_new import DatetimeExt, DayFrac

test_values = [
    (datetime(1776, 7, 4), 2369915.5),
    (datetime(1970, 1, 1, 12), 2440588.0),
    (datetime(2011, 11, 11, 11, 11), 2455876.965972),
    (datetime(2024, 12, 31, 23, 59, 59), 2460676.499988),
    (datetime(2025, 8, 28, 20, 9, 56, 400000), 2460916.340236),
]
"""Retrieved values from <https://aa.usno.navy.mil/data/JulianDate>"""

@pytest.mark.parametrize(("test_dt", "test_jd"), test_values)
def test_datetimeToDayFrac(test_dt: datetime, test_jd: float):
    """Make sure :meth:`.DatetimeExt.toDayFrac()` gives same results as :meth:`.datetimeToJulianDate()`."""
    jd_calc = DatetimeExt(test_dt).toDayFrac()
    assert abs(jd_calc.days - test_jd) < 1e-6
