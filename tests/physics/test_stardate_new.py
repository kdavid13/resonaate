
# Standard Library Imports
from datetime import datetime

# Third Party Imports
import pytest

# RESONAATE Imports
from resonaate.physics.time.stardate_new import DatetimeExt, DayFrac

test_values = [
    (datetime(1776, 7, 4), 2369915.5),
    (datetime(1970, 1, 1, 12), 2440588.0),
    (datetime(2011, 11, 11, 11, 11), 2455876.9659722224),
    (datetime(2024, 12, 31, 23, 59, 59), 2460676.499988426),
    (datetime(2025, 8, 28, 20, 9, 56, 654321), 2460916.3402390545),
]
"""Computed values using pyerfa@2.0.1.5 :: ``dtf2d()``"""

@pytest.mark.parametrize(("test_dt", "test_jd"), test_values)
def test_datetimeToDayFrac(test_dt: datetime, test_jd: float):
    """Verify that :meth:`.DatetimeExt.toDayFrac()` results in the expected value."""
    jd_calc = DatetimeExt.combine(test_dt.date(), test_dt.time()).toDayFrac()
    assert jd_calc == test_jd

@pytest.mark.parametrize(("test_dt", "test_jd"), test_values)
def test_dayFracToDatetime(test_dt: datetime, test_jd: float):
    """Verify that :meth:`.DayFrac.toDatetime()` results in the expected value."""
    jd_calc = DayFrac(test_jd)
    dt_calc = jd_calc.toDatetime()

    assert abs((dt_calc - test_dt).total_seconds()) < jd_calc.sec_tol
