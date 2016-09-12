# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar

try:
    # Needed in Python 2.6 or assertRaisesRegex
    import unittest2 as unittest
except ImportError:
    import unittest

from six import assertRaisesRegex, PY3

from datetime import *

from dateutil.relativedelta import *
from dateutil.parser import *
from dateutil.easter import *
from dateutil.rrule import *

from dateutil.tz import tzoffset

class RelativeDeltaTest(unittest.TestCase):
    now = datetime(2003, 9, 17, 20, 54, 47, 282310)
    today = date(2003, 9, 17)

    def testInheritance(self):
        # Ensure that relativedelta is inheritance-friendly.
        class rdChildClass(relativedelta):
            pass

        ccRD = rdChildClass(years=1, months=1, days=1, leapdays=1, weeks=1,
                            hours=1, minutes=1, seconds=1, microseconds=1)

        rd = relativedelta(years=1, months=1, days=1, leapdays=1, weeks=1,
                           hours=1, minutes=1, seconds=1, microseconds=1)

        self.assertEqual(type(ccRD + rd), type(ccRD),
                         msg='Addition does not inherit type.')

        self.assertEqual(type(ccRD - rd), type(ccRD),
                         msg='Subtraction does not inherit type.')

        self.assertEqual(type(-ccRD), type(ccRD),
                         msg='Negation does not inherit type.')

        self.assertEqual(type(ccRD * 5.0), type(ccRD),
                         msg='Multiplication does not inherit type.')
        
        self.assertEqual(type(ccRD / 5.0), type(ccRD),
                         msg='Division does not inherit type.')


    def testNextMonth(self):
        self.assertEqual(self.now+relativedelta(months=+1),
                         datetime(2003, 10, 17, 20, 54, 47, 282310))

    def testNextMonthPlusOneWeek(self):
        self.assertEqual(self.now+relativedelta(months=+1, weeks=+1),
                         datetime(2003, 10, 24, 20, 54, 47, 282310))

    def testNextMonthPlusOneWeek10am(self):
        self.assertEqual(self.today +
                         relativedelta(months=+1, weeks=+1, hour=10),
                         datetime(2003, 10, 24, 10, 0))

    def testNextMonthPlusOneWeek10amDiff(self):
        self.assertEqual(relativedelta(datetime(2003, 10, 24, 10, 0),
                                       self.today),
                         relativedelta(months=+1, days=+7, hours=+10))

    def testOneMonthBeforeOneYear(self):
        self.assertEqual(self.now+relativedelta(years=+1, months=-1),
                         datetime(2004, 8, 17, 20, 54, 47, 282310))

    def testMonthsOfDiffNumOfDays(self):
        self.assertEqual(date(2003, 1, 27)+relativedelta(months=+1),
                         date(2003, 2, 27))
        self.assertEqual(date(2003, 1, 31)+relativedelta(months=+1),
                         date(2003, 2, 28))
        self.assertEqual(date(2003, 1, 31)+relativedelta(months=+2),
                         date(2003, 3, 31))

    def testMonthsOfDiffNumOfDaysWithYears(self):
        self.assertEqual(date(2000, 2, 28)+relativedelta(years=+1),
                         date(2001, 2, 28))
        self.assertEqual(date(2000, 2, 29)+relativedelta(years=+1),
                         date(2001, 2, 28))

        self.assertEqual(date(1999, 2, 28)+relativedelta(years=+1),
                         date(2000, 2, 28))
        self.assertEqual(date(1999, 3, 1)+relativedelta(years=+1),
                         date(2000, 3, 1))
        self.assertEqual(date(1999, 3, 1)+relativedelta(years=+1),
                         date(2000, 3, 1))

        self.assertEqual(date(2001, 2, 28)+relativedelta(years=-1),
                         date(2000, 2, 28))
        self.assertEqual(date(2001, 3, 1)+relativedelta(years=-1),
                         date(2000, 3, 1))

    def testNextFriday(self):
        self.assertEqual(self.today+relativedelta(weekday=FR),
                         date(2003, 9, 19))

    def testNextFridayInt(self):
        self.assertEqual(self.today+relativedelta(weekday=calendar.FRIDAY),
                         date(2003, 9, 19))

    def testLastFridayInThisMonth(self):
        self.assertEqual(self.today+relativedelta(day=31, weekday=FR(-1)),
                         date(2003, 9, 26))

    def testNextWednesdayIsToday(self):
        self.assertEqual(self.today+relativedelta(weekday=WE),
                         date(2003, 9, 17))

    def testNextWenesdayNotToday(self):
        self.assertEqual(self.today+relativedelta(days=+1, weekday=WE),
                         date(2003, 9, 24))

    def test15thISOYearWeek(self):
        self.assertEqual(date(2003, 1, 1) +
                         relativedelta(day=4, weeks=+14, weekday=MO(-1)),
                         date(2003, 4, 7))

    def testMillenniumAge(self):
        self.assertEqual(relativedelta(self.now, date(2001, 1, 1)),
                         relativedelta(years=+2, months=+8, days=+16,
                                       hours=+20, minutes=+54, seconds=+47,
                                       microseconds=+282310))

    def testJohnAge(self):
        self.assertEqual(relativedelta(self.now,
                                       datetime(1978, 4, 5, 12, 0)),
                         relativedelta(years=+25, months=+5, days=+12,
                                       hours=+8, minutes=+54, seconds=+47,
                                       microseconds=+282310))

    def testJohnAgeWithDate(self):
        self.assertEqual(relativedelta(self.today,
                                       datetime(1978, 4, 5, 12, 0)),
                         relativedelta(years=+25, months=+5, days=+11,
                                       hours=+12))

    def testYearDay(self):
        self.assertEqual(date(2003, 1, 1)+relativedelta(yearday=260),
                         date(2003, 9, 17))
        self.assertEqual(date(2002, 1, 1)+relativedelta(yearday=260),
                         date(2002, 9, 17))
        self.assertEqual(date(2000, 1, 1)+relativedelta(yearday=260),
                         date(2000, 9, 16))
        self.assertEqual(self.today+relativedelta(yearday=261),
                         date(2003, 9, 18))

    def testYearDayBug(self):
        # Tests a problem reported by Adam Ryan.
        self.assertEqual(date(2010, 1, 1)+relativedelta(yearday=15),
                         date(2010, 1, 15))

    def testNonLeapYearDay(self):
        self.assertEqual(date(2003, 1, 1)+relativedelta(nlyearday=260),
                         date(2003, 9, 17))
        self.assertEqual(date(2002, 1, 1)+relativedelta(nlyearday=260),
                         date(2002, 9, 17))
        self.assertEqual(date(2000, 1, 1)+relativedelta(nlyearday=260),
                         date(2000, 9, 17))
        self.assertEqual(self.today+relativedelta(yearday=261),
                         date(2003, 9, 18))

    def testAddition(self):
        self.assertEqual(relativedelta(days=10) +
                         relativedelta(years=1, months=2, days=3, hours=4,
                                       minutes=5, microseconds=6),
                         relativedelta(years=1, months=2, days=13, hours=4,
                                       minutes=5, microseconds=6))

    def testAdditionToDatetime(self):
        self.assertEqual(datetime(2000, 1, 1) + relativedelta(days=1),
                         datetime(2000, 1, 2))

    def testRightAdditionToDatetime(self):
        self.assertEqual(relativedelta(days=1) + datetime(2000, 1, 1),
                         datetime(2000, 1, 2))

    def testSubtraction(self):
        self.assertEqual(relativedelta(days=10) -
                         relativedelta(years=1, months=2, days=3, hours=4,
                                       minutes=5, microseconds=6),
                         relativedelta(years=-1, months=-2, days=7, hours=-4,
                                       minutes=-5, microseconds=-6))

    def testRightSubtractionFromDatetime(self):
        self.assertEqual(datetime(2000, 1, 2) - relativedelta(days=1),
                         datetime(2000, 1, 1))

    def testSubractionWithDatetime(self):
        self.assertRaises(TypeError, lambda x, y: x - y,
                          (relativedelta(days=1), datetime(2000, 1, 1)))

    def testMultiplication(self):
        self.assertEqual(datetime(2000, 1, 1) + relativedelta(days=1) * 28,
                         datetime(2000, 1, 29))
        self.assertEqual(datetime(2000, 1, 1) + 28 * relativedelta(days=1),
                         datetime(2000, 1, 29))

    def testDivision(self):
        self.assertEqual(datetime(2000, 1, 1) + relativedelta(days=28) / 28,
                         datetime(2000, 1, 2))

    def testBoolean(self):
        self.assertFalse(relativedelta(days=0))
        self.assertTrue(relativedelta(days=1))

    def testComparison(self):
        d1 = relativedelta(years=1, months=1, days=1, leapdays=0, hours=1, 
                           minutes=1, seconds=1, microseconds=1)
        d2 = relativedelta(years=1, months=1, days=1, leapdays=0, hours=1, 
                           minutes=1, seconds=1, microseconds=1)
        d3 = relativedelta(years=1, months=1, days=1, leapdays=0, hours=1, 
                           minutes=1, seconds=1, microseconds=2)

        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def testWeeks(self):
        # Test that the weeks property is working properly.
        rd = relativedelta(years=4, months=2, weeks=8, days=6)
        self.assertEqual((rd.weeks, rd.days), (8, 8 * 7 + 6))
        
        rd.weeks = 3
        self.assertEqual((rd.weeks, rd.days), (3, 3 * 7 + 6))


class RRuleTest(unittest.TestCase):
    def _rrulestr_reverse_test(self, rule):
        """
        Call with an `rrule` and it will test that `str(rrule)` generates a
        string which generates the same `rrule` as the input when passed to
        `rrulestr()`
        """
        rr_str = str(rule)
        rrulestr_rrule = rrulestr(rr_str)

        self.assertEqual(list(rule), list(rrulestr_rrule))

    def testYearly(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testYearlyInterval(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0),
                          datetime(2001, 9, 2, 9, 0)])

    def testYearlyIntervalLarge(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              interval=100,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(2097, 9, 2, 9, 0),
                          datetime(2197, 9, 2, 9, 0)])

    def testYearlyByMonth(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 2, 9, 0),
                          datetime(1998, 3, 2, 9, 0),
                          datetime(1999, 1, 2, 9, 0)])

    def testYearlyByMonthDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 10, 1, 9, 0),
                          datetime(1997, 10, 3, 9, 0)])

    def testYearlyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 9, 0),
                          datetime(1998, 1, 7, 9, 0),
                          datetime(1998, 3, 5, 9, 0)])

    def testYearlyByWeekDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testYearlyByNWeekDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 25, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 12, 31, 9, 0)])

    def testYearlyByNWeekDayLarge(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 11, 9, 0),
                          datetime(1998, 1, 20, 9, 0),
                          datetime(1998, 12, 17, 9, 0)])

    def testYearlyByMonthAndWeekDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 8, 9, 0)])

    def testYearlyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 29, 9, 0),
                          datetime(1998, 3, 3, 9, 0)])

    def testYearlyByMonthAndNWeekDayLarge(self):
        # This is interesting because the TH(-3) ends up before
        # the TU(3).
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 15, 9, 0),
                          datetime(1998, 1, 20, 9, 0),
                          datetime(1998, 3, 12, 9, 0)])

    def testYearlyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 2, 3, 9, 0),
                          datetime(1998, 3, 3, 9, 0)])

    def testYearlyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 3, 3, 9, 0),
                          datetime(2001, 3, 1, 9, 0)])

    def testYearlyByYearDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testYearlyByYearDayNeg(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testYearlyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 4, 10, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testYearlyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 4, 10, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testYearlyByWeekNo(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 9, 0),
                          datetime(1998, 5, 12, 9, 0),
                          datetime(1998, 5, 13, 9, 0)])

    def testYearlyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 9, 0),
                          datetime(1999, 1, 4, 9, 0),
                          datetime(2000, 1, 3, 9, 0)])

    def testYearlyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1998, 12, 27, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testYearlyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1999, 1, 3, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testYearlyByEaster(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 9, 0),
                          datetime(1999, 4, 4, 9, 0),
                          datetime(2000, 4, 23, 9, 0)])

    def testYearlyByEasterPos(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 9, 0),
                          datetime(1999, 4, 5, 9, 0),
                          datetime(2000, 4, 24, 9, 0)])

    def testYearlyByEasterNeg(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 9, 0),
                          datetime(1999, 4, 3, 9, 0),
                          datetime(2000, 4, 22, 9, 0)])

    def testYearlyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 9, 0),
                          datetime(2004, 12, 27, 9, 0),
                          datetime(2009, 12, 28, 9, 0)])

    def testYearlyByHour(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1998, 9, 2, 6, 0),
                          datetime(1998, 9, 2, 18, 0)])

    def testYearlyByMinute(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6),
                          datetime(1997, 9, 2, 9, 18),
                          datetime(1998, 9, 2, 9, 6)])

    def testYearlyBySecond(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1998, 9, 2, 9, 0, 6)])

    def testYearlyByHourAndMinute(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6),
                          datetime(1997, 9, 2, 18, 18),
                          datetime(1998, 9, 2, 6, 6)])

    def testYearlyByHourAndSecond(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1998, 9, 2, 6, 0, 6)])

    def testYearlyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testYearlyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testYearlyBySetPos(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonthday=15,
                              byhour=(6, 18),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 11, 15, 18, 0),
                          datetime(1998, 2, 15, 6, 0),
                          datetime(1998, 11, 15, 18, 0)])

    def testMonthly(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 10, 2, 9, 0),
                          datetime(1997, 11, 2, 9, 0)])

    def testMonthlyInterval(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 11, 2, 9, 0),
                          datetime(1998, 1, 2, 9, 0)])

    def testMonthlyIntervalLarge(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              interval=18,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1999, 3, 2, 9, 0),
                          datetime(2000, 9, 2, 9, 0)])

    def testMonthlyByMonth(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 2, 9, 0),
                          datetime(1998, 3, 2, 9, 0),
                          datetime(1999, 1, 2, 9, 0)])

    def testMonthlyByMonthDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 10, 1, 9, 0),
                          datetime(1997, 10, 3, 9, 0)])

    def testMonthlyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 9, 0),
                          datetime(1998, 1, 7, 9, 0),
                          datetime(1998, 3, 5, 9, 0)])

    def testMonthlyByWeekDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

        # Third Monday of the month
        self.assertEqual(rrule(MONTHLY,
                         byweekday=(MO(+3)),
                         dtstart=datetime(1997, 9, 1)).between(datetime(1997, 9, 1),
                                                               datetime(1997, 12, 1)),
                         [datetime(1997, 9, 15, 0, 0),
                          datetime(1997, 10, 20, 0, 0),
                          datetime(1997, 11, 17, 0, 0)])

    def testMonthlyByNWeekDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 25, 9, 0),
                          datetime(1997, 10, 7, 9, 0)])

    def testMonthlyByNWeekDayLarge(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 11, 9, 0),
                          datetime(1997, 9, 16, 9, 0),
                          datetime(1997, 10, 16, 9, 0)])

    def testMonthlyByMonthAndWeekDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 8, 9, 0)])

    def testMonthlyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 29, 9, 0),
                          datetime(1998, 3, 3, 9, 0)])

    def testMonthlyByMonthAndNWeekDayLarge(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 15, 9, 0),
                          datetime(1998, 1, 20, 9, 0),
                          datetime(1998, 3, 12, 9, 0)])

    def testMonthlyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 2, 3, 9, 0),
                          datetime(1998, 3, 3, 9, 0)])

    def testMonthlyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 3, 3, 9, 0),
                          datetime(2001, 3, 1, 9, 0)])

    def testMonthlyByYearDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testMonthlyByYearDayNeg(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testMonthlyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 4, 10, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testMonthlyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 4, 10, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testMonthlyByWeekNo(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 9, 0),
                          datetime(1998, 5, 12, 9, 0),
                          datetime(1998, 5, 13, 9, 0)])

    def testMonthlyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 9, 0),
                          datetime(1999, 1, 4, 9, 0),
                          datetime(2000, 1, 3, 9, 0)])

    def testMonthlyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1998, 12, 27, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testMonthlyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1999, 1, 3, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testMonthlyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 9, 0),
                          datetime(2004, 12, 27, 9, 0),
                          datetime(2009, 12, 28, 9, 0)])

    def testMonthlyByEaster(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 9, 0),
                          datetime(1999, 4, 4, 9, 0),
                          datetime(2000, 4, 23, 9, 0)])

    def testMonthlyByEasterPos(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 9, 0),
                          datetime(1999, 4, 5, 9, 0),
                          datetime(2000, 4, 24, 9, 0)])

    def testMonthlyByEasterNeg(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 9, 0),
                          datetime(1999, 4, 3, 9, 0),
                          datetime(2000, 4, 22, 9, 0)])

    def testMonthlyByHour(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1997, 10, 2, 6, 0),
                          datetime(1997, 10, 2, 18, 0)])

    def testMonthlyByMinute(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6),
                          datetime(1997, 9, 2, 9, 18),
                          datetime(1997, 10, 2, 9, 6)])

    def testMonthlyBySecond(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1997, 10, 2, 9, 0, 6)])

    def testMonthlyByHourAndMinute(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6),
                          datetime(1997, 9, 2, 18, 18),
                          datetime(1997, 10, 2, 6, 6)])

    def testMonthlyByHourAndSecond(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1997, 10, 2, 6, 0, 6)])

    def testMonthlyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testMonthlyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testMonthlyBySetPos(self):
        self.assertEqual(list(rrule(MONTHLY,
                              count=3,
                              bymonthday=(13, 17),
                              byhour=(6, 18),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 13, 18, 0),
                          datetime(1997, 9, 17, 6, 0),
                          datetime(1997, 10, 13, 18, 0)])

    def testWeekly(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testWeeklyInterval(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 16, 9, 0),
                          datetime(1997, 9, 30, 9, 0)])

    def testWeeklyIntervalLarge(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              interval=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 1, 20, 9, 0),
                          datetime(1998, 6, 9, 9, 0)])

    def testWeeklyByMonth(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 13, 9, 0),
                          datetime(1998, 1, 20, 9, 0)])

    def testWeeklyByMonthDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 10, 1, 9, 0),
                          datetime(1997, 10, 3, 9, 0)])

    def testWeeklyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 9, 0),
                          datetime(1998, 1, 7, 9, 0),
                          datetime(1998, 3, 5, 9, 0)])

    def testWeeklyByWeekDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testWeeklyByNWeekDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testWeeklyByMonthAndWeekDay(self):
        # This test is interesting, because it crosses the year
        # boundary in a weekly period to find day '1' as a
        # valid recurrence.
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 8, 9, 0)])

    def testWeeklyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 8, 9, 0)])

    def testWeeklyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 2, 3, 9, 0),
                          datetime(1998, 3, 3, 9, 0)])

    def testWeeklyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 3, 3, 9, 0),
                          datetime(2001, 3, 1, 9, 0)])

    def testWeeklyByYearDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testWeeklyByYearDayNeg(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testWeeklyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 1, 1, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testWeeklyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 1, 1, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testWeeklyByWeekNo(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 9, 0),
                          datetime(1998, 5, 12, 9, 0),
                          datetime(1998, 5, 13, 9, 0)])

    def testWeeklyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 9, 0),
                          datetime(1999, 1, 4, 9, 0),
                          datetime(2000, 1, 3, 9, 0)])

    def testWeeklyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1998, 12, 27, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testWeeklyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1999, 1, 3, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testWeeklyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 9, 0),
                          datetime(2004, 12, 27, 9, 0),
                          datetime(2009, 12, 28, 9, 0)])

    def testWeeklyByEaster(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 9, 0),
                          datetime(1999, 4, 4, 9, 0),
                          datetime(2000, 4, 23, 9, 0)])

    def testWeeklyByEasterPos(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 9, 0),
                          datetime(1999, 4, 5, 9, 0),
                          datetime(2000, 4, 24, 9, 0)])

    def testWeeklyByEasterNeg(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 9, 0),
                          datetime(1999, 4, 3, 9, 0),
                          datetime(2000, 4, 22, 9, 0)])

    def testWeeklyByHour(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1997, 9, 9, 6, 0),
                          datetime(1997, 9, 9, 18, 0)])

    def testWeeklyByMinute(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6),
                          datetime(1997, 9, 2, 9, 18),
                          datetime(1997, 9, 9, 9, 6)])

    def testWeeklyBySecond(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1997, 9, 9, 9, 0, 6)])

    def testWeeklyByHourAndMinute(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6),
                          datetime(1997, 9, 2, 18, 18),
                          datetime(1997, 9, 9, 6, 6)])

    def testWeeklyByHourAndSecond(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1997, 9, 9, 6, 0, 6)])

    def testWeeklyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testWeeklyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testWeeklyBySetPos(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              byweekday=(TU, TH),
                              byhour=(6, 18),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1997, 9, 4, 6, 0),
                          datetime(1997, 9, 9, 18, 0)])

    def testDaily(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0)])

    def testDailyInterval(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 6, 9, 0)])

    def testDailyIntervalLarge(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              interval=92,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 12, 3, 9, 0),
                          datetime(1998, 3, 5, 9, 0)])

    def testDailyByMonth(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 2, 9, 0),
                          datetime(1998, 1, 3, 9, 0)])

    def testDailyByMonthDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 10, 1, 9, 0),
                          datetime(1997, 10, 3, 9, 0)])

    def testDailyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 9, 0),
                          datetime(1998, 1, 7, 9, 0),
                          datetime(1998, 3, 5, 9, 0)])

    def testDailyByWeekDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testDailyByNWeekDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testDailyByMonthAndWeekDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 8, 9, 0)])

    def testDailyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 1, 8, 9, 0)])

    def testDailyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 2, 3, 9, 0),
                          datetime(1998, 3, 3, 9, 0)])

    def testDailyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 3, 3, 9, 0),
                          datetime(2001, 3, 1, 9, 0)])

    def testDailyByYearDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testDailyByYearDayNeg(self):
        self.assertEqual(list(rrule(DAILY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 9, 0),
                          datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 4, 10, 9, 0),
                          datetime(1998, 7, 19, 9, 0)])

    def testDailyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(DAILY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 1, 1, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testDailyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(DAILY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 9, 0),
                          datetime(1998, 7, 19, 9, 0),
                          datetime(1999, 1, 1, 9, 0),
                          datetime(1999, 7, 19, 9, 0)])

    def testDailyByWeekNo(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 9, 0),
                          datetime(1998, 5, 12, 9, 0),
                          datetime(1998, 5, 13, 9, 0)])

    def testDailyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 9, 0),
                          datetime(1999, 1, 4, 9, 0),
                          datetime(2000, 1, 3, 9, 0)])

    def testDailyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1998, 12, 27, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testDailyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 9, 0),
                          datetime(1999, 1, 3, 9, 0),
                          datetime(2000, 1, 2, 9, 0)])

    def testDailyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 9, 0),
                          datetime(2004, 12, 27, 9, 0),
                          datetime(2009, 12, 28, 9, 0)])

    def testDailyByEaster(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 9, 0),
                          datetime(1999, 4, 4, 9, 0),
                          datetime(2000, 4, 23, 9, 0)])

    def testDailyByEasterPos(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 9, 0),
                          datetime(1999, 4, 5, 9, 0),
                          datetime(2000, 4, 24, 9, 0)])

    def testDailyByEasterNeg(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 9, 0),
                          datetime(1999, 4, 3, 9, 0),
                          datetime(2000, 4, 22, 9, 0)])

    def testDailyByHour(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1997, 9, 3, 6, 0),
                          datetime(1997, 9, 3, 18, 0)])

    def testDailyByMinute(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6),
                          datetime(1997, 9, 2, 9, 18),
                          datetime(1997, 9, 3, 9, 6)])

    def testDailyBySecond(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1997, 9, 3, 9, 0, 6)])

    def testDailyByHourAndMinute(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6),
                          datetime(1997, 9, 2, 18, 18),
                          datetime(1997, 9, 3, 6, 6)])

    def testDailyByHourAndSecond(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1997, 9, 3, 6, 0, 6)])

    def testDailyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testDailyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testDailyBySetPos(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(15, 45),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 15),
                          datetime(1997, 9, 3, 6, 45),
                          datetime(1997, 9, 3, 18, 15)])

    def testHourly(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 10, 0),
                          datetime(1997, 9, 2, 11, 0)])

    def testHourlyInterval(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 11, 0),
                          datetime(1997, 9, 2, 13, 0)])

    def testHourlyIntervalLarge(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              interval=769,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 10, 4, 10, 0),
                          datetime(1997, 11, 5, 11, 0)])

    def testHourlyByMonth(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 1, 0),
                          datetime(1998, 1, 1, 2, 0)])

    def testHourlyByMonthDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 0, 0),
                          datetime(1997, 9, 3, 1, 0),
                          datetime(1997, 9, 3, 2, 0)])

    def testHourlyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 0, 0),
                          datetime(1998, 1, 5, 1, 0),
                          datetime(1998, 1, 5, 2, 0)])

    def testHourlyByWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 10, 0),
                          datetime(1997, 9, 2, 11, 0)])

    def testHourlyByNWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 10, 0),
                          datetime(1997, 9, 2, 11, 0)])

    def testHourlyByMonthAndWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 1, 0),
                          datetime(1998, 1, 1, 2, 0)])

    def testHourlyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 1, 0),
                          datetime(1998, 1, 1, 2, 0)])

    def testHourlyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 1, 0),
                          datetime(1998, 1, 1, 2, 0)])

    def testHourlyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 1, 0),
                          datetime(1998, 1, 1, 2, 0)])

    def testHourlyByYearDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 0, 0),
                          datetime(1997, 12, 31, 1, 0),
                          datetime(1997, 12, 31, 2, 0),
                          datetime(1997, 12, 31, 3, 0)])

    def testHourlyByYearDayNeg(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 0, 0),
                          datetime(1997, 12, 31, 1, 0),
                          datetime(1997, 12, 31, 2, 0),
                          datetime(1997, 12, 31, 3, 0)])

    def testHourlyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 0, 0),
                          datetime(1998, 4, 10, 1, 0),
                          datetime(1998, 4, 10, 2, 0),
                          datetime(1998, 4, 10, 3, 0)])

    def testHourlyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 0, 0),
                          datetime(1998, 4, 10, 1, 0),
                          datetime(1998, 4, 10, 2, 0),
                          datetime(1998, 4, 10, 3, 0)])

    def testHourlyByWeekNo(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 0, 0),
                          datetime(1998, 5, 11, 1, 0),
                          datetime(1998, 5, 11, 2, 0)])

    def testHourlyByWeekNoAndWeekDay(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 0, 0),
                          datetime(1997, 12, 29, 1, 0),
                          datetime(1997, 12, 29, 2, 0)])

    def testHourlyByWeekNoAndWeekDayLarge(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 0, 0),
                          datetime(1997, 12, 28, 1, 0),
                          datetime(1997, 12, 28, 2, 0)])

    def testHourlyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 0, 0),
                          datetime(1997, 12, 28, 1, 0),
                          datetime(1997, 12, 28, 2, 0)])

    def testHourlyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 0, 0),
                          datetime(1998, 12, 28, 1, 0),
                          datetime(1998, 12, 28, 2, 0)])

    def testHourlyByEaster(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 0, 0),
                          datetime(1998, 4, 12, 1, 0),
                          datetime(1998, 4, 12, 2, 0)])

    def testHourlyByEasterPos(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 0, 0),
                          datetime(1998, 4, 13, 1, 0),
                          datetime(1998, 4, 13, 2, 0)])

    def testHourlyByEasterNeg(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 0, 0),
                          datetime(1998, 4, 11, 1, 0),
                          datetime(1998, 4, 11, 2, 0)])

    def testHourlyByHour(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1997, 9, 3, 6, 0),
                          datetime(1997, 9, 3, 18, 0)])

    def testHourlyByMinute(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6),
                          datetime(1997, 9, 2, 9, 18),
                          datetime(1997, 9, 2, 10, 6)])

    def testHourlyBySecond(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1997, 9, 2, 10, 0, 6)])

    def testHourlyByHourAndMinute(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6),
                          datetime(1997, 9, 2, 18, 18),
                          datetime(1997, 9, 3, 6, 6)])

    def testHourlyByHourAndSecond(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1997, 9, 3, 6, 0, 6)])

    def testHourlyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testHourlyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testHourlyBySetPos(self):
        self.assertEqual(list(rrule(HOURLY,
                              count=3,
                              byminute=(15, 45),
                              bysecond=(15, 45),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 15, 45),
                          datetime(1997, 9, 2, 9, 45, 15),
                          datetime(1997, 9, 2, 10, 15, 45)])

    def testMinutely(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 9, 1),
                          datetime(1997, 9, 2, 9, 2)])

    def testMinutelyInterval(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 9, 2),
                          datetime(1997, 9, 2, 9, 4)])

    def testMinutelyIntervalLarge(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              interval=1501,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 10, 1),
                          datetime(1997, 9, 4, 11, 2)])

    def testMinutelyByMonth(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 0, 1),
                          datetime(1998, 1, 1, 0, 2)])

    def testMinutelyByMonthDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 0, 0),
                          datetime(1997, 9, 3, 0, 1),
                          datetime(1997, 9, 3, 0, 2)])

    def testMinutelyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 0, 0),
                          datetime(1998, 1, 5, 0, 1),
                          datetime(1998, 1, 5, 0, 2)])

    def testMinutelyByWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 9, 1),
                          datetime(1997, 9, 2, 9, 2)])

    def testMinutelyByNWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 2, 9, 1),
                          datetime(1997, 9, 2, 9, 2)])

    def testMinutelyByMonthAndWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 0, 1),
                          datetime(1998, 1, 1, 0, 2)])

    def testMinutelyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 0, 1),
                          datetime(1998, 1, 1, 0, 2)])

    def testMinutelyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 0, 1),
                          datetime(1998, 1, 1, 0, 2)])

    def testMinutelyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0),
                          datetime(1998, 1, 1, 0, 1),
                          datetime(1998, 1, 1, 0, 2)])

    def testMinutelyByYearDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 0, 0),
                          datetime(1997, 12, 31, 0, 1),
                          datetime(1997, 12, 31, 0, 2),
                          datetime(1997, 12, 31, 0, 3)])

    def testMinutelyByYearDayNeg(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 0, 0),
                          datetime(1997, 12, 31, 0, 1),
                          datetime(1997, 12, 31, 0, 2),
                          datetime(1997, 12, 31, 0, 3)])

    def testMinutelyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 0, 0),
                          datetime(1998, 4, 10, 0, 1),
                          datetime(1998, 4, 10, 0, 2),
                          datetime(1998, 4, 10, 0, 3)])

    def testMinutelyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 0, 0),
                          datetime(1998, 4, 10, 0, 1),
                          datetime(1998, 4, 10, 0, 2),
                          datetime(1998, 4, 10, 0, 3)])

    def testMinutelyByWeekNo(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 0, 0),
                          datetime(1998, 5, 11, 0, 1),
                          datetime(1998, 5, 11, 0, 2)])

    def testMinutelyByWeekNoAndWeekDay(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 0, 0),
                          datetime(1997, 12, 29, 0, 1),
                          datetime(1997, 12, 29, 0, 2)])

    def testMinutelyByWeekNoAndWeekDayLarge(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 0, 0),
                          datetime(1997, 12, 28, 0, 1),
                          datetime(1997, 12, 28, 0, 2)])

    def testMinutelyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 0, 0),
                          datetime(1997, 12, 28, 0, 1),
                          datetime(1997, 12, 28, 0, 2)])

    def testMinutelyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 0, 0),
                          datetime(1998, 12, 28, 0, 1),
                          datetime(1998, 12, 28, 0, 2)])

    def testMinutelyByEaster(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 0, 0),
                          datetime(1998, 4, 12, 0, 1),
                          datetime(1998, 4, 12, 0, 2)])

    def testMinutelyByEasterPos(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 0, 0),
                          datetime(1998, 4, 13, 0, 1),
                          datetime(1998, 4, 13, 0, 2)])

    def testMinutelyByEasterNeg(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 0, 0),
                          datetime(1998, 4, 11, 0, 1),
                          datetime(1998, 4, 11, 0, 2)])

    def testMinutelyByHour(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0),
                          datetime(1997, 9, 2, 18, 1),
                          datetime(1997, 9, 2, 18, 2)])

    def testMinutelyByMinute(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6),
                          datetime(1997, 9, 2, 9, 18),
                          datetime(1997, 9, 2, 10, 6)])

    def testMinutelyBySecond(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1997, 9, 2, 9, 1, 6)])

    def testMinutelyByHourAndMinute(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6),
                          datetime(1997, 9, 2, 18, 18),
                          datetime(1997, 9, 3, 6, 6)])

    def testMinutelyByHourAndSecond(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1997, 9, 2, 18, 1, 6)])

    def testMinutelyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testMinutelyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testMinutelyBySetPos(self):
        self.assertEqual(list(rrule(MINUTELY,
                              count=3,
                              bysecond=(15, 30, 45),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 15),
                          datetime(1997, 9, 2, 9, 0, 45),
                          datetime(1997, 9, 2, 9, 1, 15)])

    def testSecondly(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 0),
                          datetime(1997, 9, 2, 9, 0, 1),
                          datetime(1997, 9, 2, 9, 0, 2)])

    def testSecondlyInterval(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 0),
                          datetime(1997, 9, 2, 9, 0, 2),
                          datetime(1997, 9, 2, 9, 0, 4)])

    def testSecondlyIntervalLarge(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              interval=90061,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 0),
                          datetime(1997, 9, 3, 10, 1, 1),
                          datetime(1997, 9, 4, 11, 2, 2)])

    def testSecondlyByMonth(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0, 0),
                          datetime(1998, 1, 1, 0, 0, 1),
                          datetime(1998, 1, 1, 0, 0, 2)])

    def testSecondlyByMonthDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 3, 0, 0, 0),
                          datetime(1997, 9, 3, 0, 0, 1),
                          datetime(1997, 9, 3, 0, 0, 2)])

    def testSecondlyByMonthAndMonthDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 5, 0, 0, 0),
                          datetime(1998, 1, 5, 0, 0, 1),
                          datetime(1998, 1, 5, 0, 0, 2)])

    def testSecondlyByWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 0),
                          datetime(1997, 9, 2, 9, 0, 1),
                          datetime(1997, 9, 2, 9, 0, 2)])

    def testSecondlyByNWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 0),
                          datetime(1997, 9, 2, 9, 0, 1),
                          datetime(1997, 9, 2, 9, 0, 2)])

    def testSecondlyByMonthAndWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0, 0),
                          datetime(1998, 1, 1, 0, 0, 1),
                          datetime(1998, 1, 1, 0, 0, 2)])

    def testSecondlyByMonthAndNWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0, 0),
                          datetime(1998, 1, 1, 0, 0, 1),
                          datetime(1998, 1, 1, 0, 0, 2)])

    def testSecondlyByMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0, 0),
                          datetime(1998, 1, 1, 0, 0, 1),
                          datetime(1998, 1, 1, 0, 0, 2)])

    def testSecondlyByMonthAndMonthDayAndWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 1, 1, 0, 0, 0),
                          datetime(1998, 1, 1, 0, 0, 1),
                          datetime(1998, 1, 1, 0, 0, 2)])

    def testSecondlyByYearDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 0, 0, 0),
                          datetime(1997, 12, 31, 0, 0, 1),
                          datetime(1997, 12, 31, 0, 0, 2),
                          datetime(1997, 12, 31, 0, 0, 3)])

    def testSecondlyByYearDayNeg(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 31, 0, 0, 0),
                          datetime(1997, 12, 31, 0, 0, 1),
                          datetime(1997, 12, 31, 0, 0, 2),
                          datetime(1997, 12, 31, 0, 0, 3)])

    def testSecondlyByMonthAndYearDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 0, 0, 0),
                          datetime(1998, 4, 10, 0, 0, 1),
                          datetime(1998, 4, 10, 0, 0, 2),
                          datetime(1998, 4, 10, 0, 0, 3)])

    def testSecondlyByMonthAndYearDayNeg(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 10, 0, 0, 0),
                          datetime(1998, 4, 10, 0, 0, 1),
                          datetime(1998, 4, 10, 0, 0, 2),
                          datetime(1998, 4, 10, 0, 0, 3)])

    def testSecondlyByWeekNo(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 5, 11, 0, 0, 0),
                          datetime(1998, 5, 11, 0, 0, 1),
                          datetime(1998, 5, 11, 0, 0, 2)])

    def testSecondlyByWeekNoAndWeekDay(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 29, 0, 0, 0),
                          datetime(1997, 12, 29, 0, 0, 1),
                          datetime(1997, 12, 29, 0, 0, 2)])

    def testSecondlyByWeekNoAndWeekDayLarge(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 0, 0, 0),
                          datetime(1997, 12, 28, 0, 0, 1),
                          datetime(1997, 12, 28, 0, 0, 2)])

    def testSecondlyByWeekNoAndWeekDayLast(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 12, 28, 0, 0, 0),
                          datetime(1997, 12, 28, 0, 0, 1),
                          datetime(1997, 12, 28, 0, 0, 2)])

    def testSecondlyByWeekNoAndWeekDay53(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 12, 28, 0, 0, 0),
                          datetime(1998, 12, 28, 0, 0, 1),
                          datetime(1998, 12, 28, 0, 0, 2)])

    def testSecondlyByEaster(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 12, 0, 0, 0),
                          datetime(1998, 4, 12, 0, 0, 1),
                          datetime(1998, 4, 12, 0, 0, 2)])

    def testSecondlyByEasterPos(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 13, 0, 0, 0),
                          datetime(1998, 4, 13, 0, 0, 1),
                          datetime(1998, 4, 13, 0, 0, 2)])

    def testSecondlyByEasterNeg(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1998, 4, 11, 0, 0, 0),
                          datetime(1998, 4, 11, 0, 0, 1),
                          datetime(1998, 4, 11, 0, 0, 2)])

    def testSecondlyByHour(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 0),
                          datetime(1997, 9, 2, 18, 0, 1),
                          datetime(1997, 9, 2, 18, 0, 2)])

    def testSecondlyByMinute(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 0),
                          datetime(1997, 9, 2, 9, 6, 1),
                          datetime(1997, 9, 2, 9, 6, 2)])

    def testSecondlyBySecond(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0, 6),
                          datetime(1997, 9, 2, 9, 0, 18),
                          datetime(1997, 9, 2, 9, 1, 6)])

    def testSecondlyByHourAndMinute(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 0),
                          datetime(1997, 9, 2, 18, 6, 1),
                          datetime(1997, 9, 2, 18, 6, 2)])

    def testSecondlyByHourAndSecond(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 0, 6),
                          datetime(1997, 9, 2, 18, 0, 18),
                          datetime(1997, 9, 2, 18, 1, 6)])

    def testSecondlyByMinuteAndSecond(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 6, 6),
                          datetime(1997, 9, 2, 9, 6, 18),
                          datetime(1997, 9, 2, 9, 18, 6)])

    def testSecondlyByHourAndMinuteAndSecond(self):
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 18, 6, 6),
                          datetime(1997, 9, 2, 18, 6, 18),
                          datetime(1997, 9, 2, 18, 18, 6)])

    def testSecondlyByHourAndMinuteAndSecondBug(self):
        # This explores a bug found by Mathieu Bridon.
        self.assertEqual(list(rrule(SECONDLY,
                              count=3,
                              bysecond=(0,),
                              byminute=(1,),
                              dtstart=datetime(2010, 3, 22, 12, 1))),
                         [datetime(2010, 3, 22, 12, 1),
                          datetime(2010, 3, 22, 13, 1),
                          datetime(2010, 3, 22, 14, 1)])

    def testLongIntegers(self):
        if not PY3:  # There is no longs in python3
            self.assertEqual(list(rrule(MINUTELY,
                                  count=long(2),
                                  interval=long(2),
                                  bymonth=long(2),
                                  byweekday=long(3),
                                  byhour=long(6),
                                  byminute=long(6),
                                  bysecond=long(6),
                                  dtstart=datetime(1997, 9, 2, 9, 0))),
                             [datetime(1998, 2, 5, 6, 6, 6),
                              datetime(1998, 2, 12, 6, 6, 6)])
            self.assertEqual(list(rrule(YEARLY,
                                  count=long(2),
                                  bymonthday=long(5),
                                  byweekno=long(2),
                                  dtstart=datetime(1997, 9, 2, 9, 0))),
                             [datetime(1998, 1, 5, 9, 0),
                              datetime(2004, 1, 5, 9, 0)])

    def testHourlyBadRRule(self):
        """
        When `byhour` is specified with `freq=HOURLY`, there are certain
        combinations of `dtstart` and `byhour` which result in an rrule with no
        valid values.

        See https://github.com/dateutil/dateutil/issues/4
        """

        self.assertRaises(ValueError, rrule, HOURLY,
                          **dict(interval=4, byhour=(7, 11, 15, 19),
                                 dtstart=datetime(1997, 9, 2, 9, 0)))

    def testMinutelyBadRRule(self):
        """
        See :func:`testHourlyBadRRule` for details.
        """

        self.assertRaises(ValueError, rrule, MINUTELY,
                          **dict(interval=12, byminute=(10, 11, 25, 39, 50),
                                 dtstart=datetime(1997, 9, 2, 9, 0)))

    def testSecondlyBadRRule(self):
        """
        See :func:`testHourlyBadRRule` for details.
        """

        self.assertRaises(ValueError, rrule, SECONDLY,
                          **dict(interval=10, bysecond=(2, 15, 37, 42, 59),
                                 dtstart=datetime(1997, 9, 2, 9, 0)))

    def testMinutelyBadComboRRule(self):
        """
        Certain values of :param:`interval` in :class:`rrule`, when combined
        with certain values of :param:`byhour` create rules which apply to no
        valid dates. The library should detect this case in the iterator and
        raise a :exception:`ValueError`.
        """

        # In Python 2.7 you can use a context manager for this.
        def make_bad_rrule():
            list(rrule(MINUTELY, interval=120, byhour=(10, 12, 14, 16),
                 count=2, dtstart=datetime(1997, 9, 2, 9, 0)))

        self.assertRaises(ValueError, make_bad_rrule)

    def testSecondlyBadComboRRule(self):
        """
        See :func:`testMinutelyBadComboRRule' for details.
        """

        # In Python 2.7 you can use a context manager for this.
        def make_bad_minute_rrule():
            list(rrule(SECONDLY, interval=360, byminute=(10, 28, 49),
                 count=4, dtstart=datetime(1997, 9, 2, 9, 0)))

        def make_bad_hour_rrule():
            list(rrule(SECONDLY, interval=43200, byhour=(2, 10, 18, 23),
                 count=4, dtstart=datetime(1997, 9, 2, 9, 0)))

        self.assertRaises(ValueError, make_bad_minute_rrule)
        self.assertRaises(ValueError, make_bad_hour_rrule)

    def testUntilNotMatching(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0),
                              until=datetime(1997, 9, 5, 8, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0)])

    def testUntilMatching(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0),
                              until=datetime(1997, 9, 4, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0)])

    def testUntilSingle(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0),
                              until=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0)])

    def testUntilEmpty(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0),
                              until=datetime(1997, 9, 1, 9, 0))),
                         [])

    def testUntilWithDate(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0),
                              until=date(1997, 9, 5))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0)])

    def testWkStIntervalMO(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              interval=2,
                              byweekday=(TU, SU),
                              wkst=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 7, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testWkStIntervalSU(self):
        self.assertEqual(list(rrule(WEEKLY,
                              count=3,
                              interval=2,
                              byweekday=(TU, SU),
                              wkst=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 14, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testDTStartIsDate(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=date(1997, 9, 2))),
                         [datetime(1997, 9, 2, 0, 0),
                          datetime(1997, 9, 3, 0, 0),
                          datetime(1997, 9, 4, 0, 0)])

    def testDTStartWithMicroseconds(self):
        self.assertEqual(list(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0, 0, 500000))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0)])

    def testMaxYear(self):
        self.assertEqual(list(rrule(YEARLY,
                              count=3,
                              bymonth=2,
                              bymonthday=31,
                              dtstart=datetime(9997, 9, 2, 9, 0, 0))),
                         [])

    def testGetItem(self):
        self.assertEqual(rrule(DAILY,
                               count=3,
                               dtstart=datetime(1997, 9, 2, 9, 0))[0],
                         datetime(1997, 9, 2, 9, 0))

    def testGetItemNeg(self):
        self.assertEqual(rrule(DAILY,
                               count=3,
                               dtstart=datetime(1997, 9, 2, 9, 0))[-1],
                         datetime(1997, 9, 4, 9, 0))

    def testGetItemSlice(self):
        self.assertEqual(rrule(DAILY,
                               # count=3,
                               dtstart=datetime(1997, 9, 2, 9, 0))[1:2],
                         [datetime(1997, 9, 3, 9, 0)])

    def testGetItemSliceEmpty(self):
        self.assertEqual(rrule(DAILY,
                               count=3,
                               dtstart=datetime(1997, 9, 2, 9, 0))[:],
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0)])

    def testGetItemSliceStep(self):
        self.assertEqual(rrule(DAILY,
                               count=3,
                               dtstart=datetime(1997, 9, 2, 9, 0))[::-2],
                         [datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 2, 9, 0)])

    def testCount(self):
        self.assertEqual(rrule(DAILY,
                               count=3,
                               dtstart=datetime(1997, 9, 2, 9, 0)).count(),
                         3)

    def testContains(self):
        rr = rrule(DAILY, count=3, dtstart=datetime(1997, 9, 2, 9, 0))
        self.assertEqual(datetime(1997, 9, 3, 9, 0) in rr, True)

    def testContainsNot(self):
        rr = rrule(DAILY, count=3, dtstart=datetime(1997, 9, 2, 9, 0))
        self.assertEqual(datetime(1997, 9, 3, 9, 0) not in rr, False)

    def testBefore(self):
        self.assertEqual(rrule(DAILY,  # count=5
            dtstart=datetime(1997, 9, 2, 9, 0)).before(datetime(1997, 9, 5, 9, 0)),
                         datetime(1997, 9, 4, 9, 0))

    def testBeforeInc(self):
        self.assertEqual(rrule(DAILY,
                               #count=5,
                               dtstart=datetime(1997, 9, 2, 9, 0))
                               .before(datetime(1997, 9, 5, 9, 0), inc=True),
                         datetime(1997, 9, 5, 9, 0))

    def testAfter(self):
        self.assertEqual(rrule(DAILY,
                               #count=5,
                               dtstart=datetime(1997, 9, 2, 9, 0))
                               .after(datetime(1997, 9, 4, 9, 0)),
                         datetime(1997, 9, 5, 9, 0))

    def testAfterInc(self):
        self.assertEqual(rrule(DAILY,
                               #count=5,
                               dtstart=datetime(1997, 9, 2, 9, 0))
                               .after(datetime(1997, 9, 4, 9, 0), inc=True),
                         datetime(1997, 9, 4, 9, 0))

    def testXAfter(self):
        self.assertEqual(list(rrule(DAILY,
                                    dtstart=datetime(1997, 9, 2, 9, 0))
                                    .xafter(datetime(1997, 9, 8, 9, 0), count=12)),
                                    [datetime(1997, 9, 9, 9, 0),
                                     datetime(1997, 9, 10, 9, 0),
                                     datetime(1997, 9, 11, 9, 0),
                                     datetime(1997, 9, 12, 9, 0),
                                     datetime(1997, 9, 13, 9, 0),
                                     datetime(1997, 9, 14, 9, 0),
                                     datetime(1997, 9, 15, 9, 0),
                                     datetime(1997, 9, 16, 9, 0),
                                     datetime(1997, 9, 17, 9, 0),
                                     datetime(1997, 9, 18, 9, 0),
                                     datetime(1997, 9, 19, 9, 0),
                                     datetime(1997, 9, 20, 9, 0)])

    def testXAfterInc(self):
        self.assertEqual(list(rrule(DAILY,
                                    dtstart=datetime(1997, 9, 2, 9, 0))
                                    .xafter(datetime(1997, 9, 8, 9, 0), count=12, inc=True)),
                                    [datetime(1997, 9, 8, 9, 0),
                                     datetime(1997, 9, 9, 9, 0),
                                     datetime(1997, 9, 10, 9, 0),
                                     datetime(1997, 9, 11, 9, 0),
                                     datetime(1997, 9, 12, 9, 0),
                                     datetime(1997, 9, 13, 9, 0),
                                     datetime(1997, 9, 14, 9, 0),
                                     datetime(1997, 9, 15, 9, 0),
                                     datetime(1997, 9, 16, 9, 0),
                                     datetime(1997, 9, 17, 9, 0),
                                     datetime(1997, 9, 18, 9, 0),
                                     datetime(1997, 9, 19, 9, 0)])

    def testBetween(self):
        self.assertEqual(rrule(DAILY,
                               #count=5,
                               dtstart=datetime(1997, 9, 2, 9, 0))
                               .between(datetime(1997, 9, 2, 9, 0),
                                        datetime(1997, 9, 6, 9, 0)),
                         [datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 5, 9, 0)])

    def testBetweenInc(self):
        self.assertEqual(rrule(DAILY,
                               #count=5,
                               dtstart=datetime(1997, 9, 2, 9, 0))
                               .between(datetime(1997, 9, 2, 9, 0),
                                        datetime(1997, 9, 6, 9, 0), inc=True),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 5, 9, 0),
                          datetime(1997, 9, 6, 9, 0)])

    def testCachePre(self):
        rr = rrule(DAILY, count=15, cache=True,
                   dtstart=datetime(1997, 9, 2, 9, 0))
        self.assertEqual(list(rr),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 5, 9, 0),
                          datetime(1997, 9, 6, 9, 0),
                          datetime(1997, 9, 7, 9, 0),
                          datetime(1997, 9, 8, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 10, 9, 0),
                          datetime(1997, 9, 11, 9, 0),
                          datetime(1997, 9, 12, 9, 0),
                          datetime(1997, 9, 13, 9, 0),
                          datetime(1997, 9, 14, 9, 0),
                          datetime(1997, 9, 15, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testCachePost(self):
        rr = rrule(DAILY, count=15, cache=True,
                   dtstart=datetime(1997, 9, 2, 9, 0))
        for x in rr: pass
        self.assertEqual(list(rr),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 5, 9, 0),
                          datetime(1997, 9, 6, 9, 0),
                          datetime(1997, 9, 7, 9, 0),
                          datetime(1997, 9, 8, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 10, 9, 0),
                          datetime(1997, 9, 11, 9, 0),
                          datetime(1997, 9, 12, 9, 0),
                          datetime(1997, 9, 13, 9, 0),
                          datetime(1997, 9, 14, 9, 0),
                          datetime(1997, 9, 15, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testCachePostInternal(self):
        rr = rrule(DAILY, count=15, cache=True,
                   dtstart=datetime(1997, 9, 2, 9, 0))
        for x in rr: pass
        self.assertEqual(rr._cache,
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 3, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 5, 9, 0),
                          datetime(1997, 9, 6, 9, 0),
                          datetime(1997, 9, 7, 9, 0),
                          datetime(1997, 9, 8, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 10, 9, 0),
                          datetime(1997, 9, 11, 9, 0),
                          datetime(1997, 9, 12, 9, 0),
                          datetime(1997, 9, 13, 9, 0),
                          datetime(1997, 9, 14, 9, 0),
                          datetime(1997, 9, 15, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testCachePreContains(self):
        rr = rrule(DAILY, count=3, cache=True,
                   dtstart=datetime(1997, 9, 2, 9, 0))
        self.assertEqual(datetime(1997, 9, 3, 9, 0) in rr, True)

    def testCachePostContains(self):
        rr = rrule(DAILY, count=3, cache=True,
                   dtstart=datetime(1997, 9, 2, 9, 0))
        for x in rr: pass
        self.assertEqual(datetime(1997, 9, 3, 9, 0) in rr, True)

    def testSet(self):
        set = rruleset()
        set.rrule(rrule(YEARLY, count=2, byweekday=TU,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.rrule(rrule(YEARLY, count=1, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testSetDate(self):
        set = rruleset()
        set.rrule(rrule(YEARLY, count=1, byweekday=TU,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.rdate(datetime(1997, 9, 4, 9))
        set.rdate(datetime(1997, 9, 9, 9))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testSetExRule(self):
        set = rruleset()
        set.rrule(rrule(YEARLY, count=6, byweekday=(TU, TH),
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.exrule(rrule(YEARLY, count=3, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testSetExDate(self):
        set = rruleset()
        set.rrule(rrule(YEARLY, count=6, byweekday=(TU, TH),
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.exdate(datetime(1997, 9, 4, 9))
        set.exdate(datetime(1997, 9, 11, 9))
        set.exdate(datetime(1997, 9, 18, 9))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testSetExDateRevOrder(self):
        set = rruleset()
        set.rrule(rrule(MONTHLY, count=5, bymonthday=10,
                        dtstart=datetime(2004, 1, 1, 9, 0)))
        set.exdate(datetime(2004, 4, 10, 9, 0))
        set.exdate(datetime(2004, 2, 10, 9, 0))
        self.assertEqual(list(set),
                         [datetime(2004, 1, 10, 9, 0),
                          datetime(2004, 3, 10, 9, 0),
                          datetime(2004, 5, 10, 9, 0)])

    def testSetDateAndExDate(self):
        set = rruleset()
        set.rdate(datetime(1997, 9, 2, 9))
        set.rdate(datetime(1997, 9, 4, 9))
        set.rdate(datetime(1997, 9, 9, 9))
        set.rdate(datetime(1997, 9, 11, 9))
        set.rdate(datetime(1997, 9, 16, 9))
        set.rdate(datetime(1997, 9, 18, 9))
        set.exdate(datetime(1997, 9, 4, 9))
        set.exdate(datetime(1997, 9, 11, 9))
        set.exdate(datetime(1997, 9, 18, 9))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testSetDateAndExRule(self):
        set = rruleset()
        set.rdate(datetime(1997, 9, 2, 9))
        set.rdate(datetime(1997, 9, 4, 9))
        set.rdate(datetime(1997, 9, 9, 9))
        set.rdate(datetime(1997, 9, 11, 9))
        set.rdate(datetime(1997, 9, 16, 9))
        set.rdate(datetime(1997, 9, 18, 9))
        set.exrule(rrule(YEARLY, count=3, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testSetCount(self):
        set = rruleset()
        set.rrule(rrule(YEARLY, count=6, byweekday=(TU, TH),
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.exrule(rrule(YEARLY, count=3, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        self.assertEqual(set.count(), 3)

    def testSetCachePre(self):
        set = rruleset()
        set.rrule(rrule(YEARLY, count=2, byweekday=TU,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.rrule(rrule(YEARLY, count=1, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testSetCachePost(self):
        set = rruleset(cache=True)
        set.rrule(rrule(YEARLY, count=2, byweekday=TU,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.rrule(rrule(YEARLY, count=1, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        for x in set: pass
        self.assertEqual(list(set),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testSetCachePostInternal(self):
        set = rruleset(cache=True)
        set.rrule(rrule(YEARLY, count=2, byweekday=TU,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        set.rrule(rrule(YEARLY, count=1, byweekday=TH,
                        dtstart=datetime(1997, 9, 2, 9, 0)))
        for x in set: pass
        self.assertEqual(list(set._cache),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testStr(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=3\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrType(self):
        self.assertEqual(isinstance(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=3\n"
                              ), rrule), True)

    def testStrForceSetType(self):
        self.assertEqual(isinstance(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=3\n"
                              , forceset=True), rruleset), True)

    def testStrSetType(self):
        self.assertEqual(isinstance(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=2;BYDAY=TU\n"
                              "RRULE:FREQ=YEARLY;COUNT=1;BYDAY=TH\n"
                              ), rruleset), True)

    def testStrCase(self):
        self.assertEqual(list(rrulestr(
                              "dtstart:19970902T090000\n"
                              "rrule:freq=yearly;count=3\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrSpaces(self):
        self.assertEqual(list(rrulestr(
                              " DTSTART:19970902T090000 "
                              " RRULE:FREQ=YEARLY;COUNT=3 "
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrSpacesAndLines(self):
        self.assertEqual(list(rrulestr(
                              " DTSTART:19970902T090000 \n"
                              " \n"
                              " RRULE:FREQ=YEARLY;COUNT=3 \n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrNoDTStart(self):
        self.assertEqual(list(rrulestr(
                              "RRULE:FREQ=YEARLY;COUNT=3\n"
                              , dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrValueOnly(self):
        self.assertEqual(list(rrulestr(
                              "FREQ=YEARLY;COUNT=3\n"
                              , dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrUnfold(self):
        self.assertEqual(list(rrulestr(
                              "FREQ=YEA\n RLY;COUNT=3\n", unfold=True,
                              dtstart=datetime(1997, 9, 2, 9, 0))),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1998, 9, 2, 9, 0),
                          datetime(1999, 9, 2, 9, 0)])

    def testStrSet(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=2;BYDAY=TU\n"
                              "RRULE:FREQ=YEARLY;COUNT=1;BYDAY=TH\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testStrSetDate(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=1;BYDAY=TU\n"
                              "RDATE:19970904T090000\n"
                              "RDATE:19970909T090000\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 4, 9, 0),
                          datetime(1997, 9, 9, 9, 0)])

    def testStrSetExRule(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=6;BYDAY=TU,TH\n"
                              "EXRULE:FREQ=YEARLY;COUNT=3;BYDAY=TH\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testStrSetExDate(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=6;BYDAY=TU,TH\n"
                              "EXDATE:19970904T090000\n"
                              "EXDATE:19970911T090000\n"
                              "EXDATE:19970918T090000\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testStrSetDateAndExDate(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RDATE:19970902T090000\n"
                              "RDATE:19970904T090000\n"
                              "RDATE:19970909T090000\n"
                              "RDATE:19970911T090000\n"
                              "RDATE:19970916T090000\n"
                              "RDATE:19970918T090000\n"
                              "EXDATE:19970904T090000\n"
                              "EXDATE:19970911T090000\n"
                              "EXDATE:19970918T090000\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testStrSetDateAndExRule(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RDATE:19970902T090000\n"
                              "RDATE:19970904T090000\n"
                              "RDATE:19970909T090000\n"
                              "RDATE:19970911T090000\n"
                              "RDATE:19970916T090000\n"
                              "RDATE:19970918T090000\n"
                              "EXRULE:FREQ=YEARLY;COUNT=3;BYDAY=TH\n"
                              )),
                         [datetime(1997, 9, 2, 9, 0),
                          datetime(1997, 9, 9, 9, 0),
                          datetime(1997, 9, 16, 9, 0)])

    def testStrKeywords(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=3;INTERVAL=3;"
                                    "BYMONTH=3;BYWEEKDAY=TH;BYMONTHDAY=3;"
                                    "BYHOUR=3;BYMINUTE=3;BYSECOND=3\n"
                              )),
                         [datetime(2033, 3, 3, 3, 3, 3),
                          datetime(2039, 3, 3, 3, 3, 3),
                          datetime(2072, 3, 3, 3, 3, 3)])

    def testStrNWeekDay(self):
        self.assertEqual(list(rrulestr(
                              "DTSTART:19970902T090000\n"
                              "RRULE:FREQ=YEARLY;COUNT=3;BYDAY=1TU,-1TH\n"
                              )),
                         [datetime(1997, 12, 25, 9, 0),
                          datetime(1998, 1, 6, 9, 0),
                          datetime(1998, 12, 31, 9, 0)])

    def testBadBySetPos(self):
        self.assertRaises(ValueError,
                          rrule, MONTHLY,
                                 count=1,
                                 bysetpos=0,
                                 dtstart=datetime(1997, 9, 2, 9, 0))

    def testBadBySetPosMany(self):
        self.assertRaises(ValueError,
                          rrule, MONTHLY,
                                 count=1,
                                 bysetpos=(-1, 0, 1),
                                 dtstart=datetime(1997, 9, 2, 9, 0))

    # Tests to ensure that str(rrule) works
    def testToStrYearly(self):
        rule = rrule(YEARLY, count=3, dtstart=datetime(1997, 9, 2, 9, 0))
        self._rrulestr_reverse_test(rule)

    def testToStrYearlyInterval(self):
        rule = rrule(YEARLY, count=3, interval=2,
                     dtstart=datetime(1997, 9, 2, 9, 0))
        self._rrulestr_reverse_test(rule)

    def testToStrYearlyByMonth(self):
        rule = rrule(YEARLY, count=3, bymonth=(1, 3),
                     dtstart=datetime(1997, 9, 2, 9, 0))

        self._rrulestr_reverse_test(rule)

    def testToStrYearlyByMonth(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                                          count=3,
                                          bymonth=(1, 3),
                                          dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                                          count=3,
                                          bymonthday=(1, 3),
                                          dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                                          count=3,
                                          bymonth=(1, 3),
                                          bymonthday=(5, 7),
                                          dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                                          count=3,
                                          byweekday=(TU, TH),
                                          dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                                          count=3,
                                          byweekday=(TU(1), TH(-1)),
                                          dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByNWeekDayLarge(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndNWeekDayLarge(self):
        # This is interesting because the TH(-3) ends up before
        # the TU(3).
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByYearDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByEaster(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByHour(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMinute(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyBySecond(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrYearlyBySetPos(self):
        self._rrulestr_reverse_test(rrule(YEARLY,
                              count=3,
                              bymonthday=15,
                              byhour=(6, 18),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthly(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyInterval(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyIntervalLarge(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              interval=18,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonth(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

        # Third Monday of the month
        self.assertEqual(rrule(MONTHLY,
                         byweekday=(MO(+3)),
                         dtstart=datetime(1997, 9, 1)).between(datetime(1997,
                                                                        9,
                                                                        1),
                                                               datetime(1997,
                                                                        12,
                                                                        1)),
                         [datetime(1997, 9, 15, 0, 0),
                          datetime(1997, 10, 20, 0, 0),
                          datetime(1997, 11, 17, 0, 0)])

    def testToStrMonthlyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByNWeekDayLarge(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndNWeekDayLarge(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(3), TH(-3)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByYearDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByEaster(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByHour(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMinute(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyBySecond(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMonthlyBySetPos(self):
        self._rrulestr_reverse_test(rrule(MONTHLY,
                              count=3,
                              bymonthday=(13, 17),
                              byhour=(6, 18),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeekly(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyInterval(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyIntervalLarge(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              interval=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonth(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthAndWeekDay(self):
        # This test is interesting, because it crosses the year
        # boundary in a weekly period to find day '1' as a
        # valid recurrence.
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByYearDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByEaster(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByHour(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMinute(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyBySecond(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrWeeklyBySetPos(self):
        self._rrulestr_reverse_test(rrule(WEEKLY,
                              count=3,
                              byweekday=(TU, TH),
                              byhour=(6, 18),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDaily(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyInterval(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyIntervalLarge(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              interval=92,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonth(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByYearDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=4,
                              bymonth=(1, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByWeekNoAndWeekDay(self):
        # That's a nice one. The first days of week number one
        # may be in the last year.
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByWeekNoAndWeekDayLarge(self):
        # Another nice test. The last days of week number 52/53
        # may be in the next year.
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByEaster(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByHour(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMinute(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyBySecond(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrDailyBySetPos(self):
        self._rrulestr_reverse_test(rrule(DAILY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(15, 45),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourly(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyInterval(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyIntervalLarge(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              interval=769,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonth(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByYearDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByWeekNoAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByWeekNoAndWeekDayLarge(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByEaster(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByHour(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMinute(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyBySecond(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrHourlyBySetPos(self):
        self._rrulestr_reverse_test(rrule(HOURLY,
                              count=3,
                              byminute=(15, 45),
                              bysecond=(15, 45),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutely(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyInterval(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyIntervalLarge(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              interval=1501,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonth(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByYearDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByWeekNoAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByWeekNoAndWeekDayLarge(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByEaster(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByHour(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMinute(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyBySecond(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrMinutelyBySetPos(self):
        self._rrulestr_reverse_test(rrule(MINUTELY,
                              count=3,
                              bysecond=(15, 30, 45),
                              bysetpos=(3, -3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondly(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyInterval(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              interval=2,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyIntervalLarge(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              interval=90061,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonth(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonthday=(1, 3),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthAndMonthDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(5, 7),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByNWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthAndNWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              byweekday=(TU(1), TH(-1)),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthAndMonthDayAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bymonth=(1, 3),
                              bymonthday=(1, 3),
                              byweekday=(TU, TH),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByYearDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=4,
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=4,
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthAndYearDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(1, 100, 200, 365),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMonthAndYearDayNeg(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=4,
                              bymonth=(4, 7),
                              byyearday=(-365, -266, -166, -1),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByWeekNo(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekno=20,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByWeekNoAndWeekDay(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekno=1,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByWeekNoAndWeekDayLarge(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekno=52,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByWeekNoAndWeekDayLast(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekno=-1,
                              byweekday=SU,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByWeekNoAndWeekDay53(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byweekno=53,
                              byweekday=MO,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByEaster(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byeaster=0,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByEasterPos(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byeaster=1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByEasterNeg(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byeaster=-1,
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByHour(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMinute(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyBySecond(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByHourAndMinute(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByHourAndSecond(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByHourAndMinuteAndSecond(self):
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              byhour=(6, 18),
                              byminute=(6, 18),
                              bysecond=(6, 18),
                              dtstart=datetime(1997, 9, 2, 9, 0)))

    def testToStrSecondlyByHourAndMinuteAndSecondBug(self):
        # This explores a bug found by Mathieu Bridon.
        self._rrulestr_reverse_test(rrule(SECONDLY,
                              count=3,
                              bysecond=(0,),
                              byminute=(1,),
                              dtstart=datetime(2010, 3, 22, 12, 1)))

    def testToStrLongIntegers(self):
        if not PY3:  # There is no longs in python3
            self._rrulestr_reverse_test(rrule(MINUTELY,
                                  count=long(2),
                                  interval=long(2),
                                  bymonth=long(2),
                                  byweekday=long(3),
                                  byhour=long(6),
                                  byminute=long(6),
                                  bysecond=long(6),
                                  dtstart=datetime(1997, 9, 2, 9, 0)))
            
            self._rrulestr_reverse_test(rrule(YEARLY,
                                  count=long(2),
                                  bymonthday=long(5),
                                  byweekno=long(2),
                                  dtstart=datetime(1997, 9, 2, 9, 0)))


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.tzinfos = {"BRST": -10800}
        self.brsttz = tzoffset("BRST", -10800)
        self.default = datetime(2003, 9, 25)

        # Parser should be able to handle bytestring and unicode
        base_str = '2014-05-01 08:00:00'
        try:
            # Python 2.x
            self.uni_str = unicode(base_str)
            self.str_str = str(base_str)
        except NameError:
            self.uni_str = str(base_str)
            self.str_str = bytes(base_str.encode())

    def testDateCommandFormat(self):
        self.assertEqual(parse("Thu Sep 25 10:36:28 BRST 2003",
                               tzinfos=self.tzinfos),
                         datetime(2003, 9, 25, 10, 36, 28,
                                  tzinfo=self.brsttz))

    def testDateCommandFormatUnicode(self):
        self.assertEqual(parse("Thu Sep 25 10:36:28 BRST 2003",
                               tzinfos=self.tzinfos),
                         datetime(2003, 9, 25, 10, 36, 28,
                                  tzinfo=self.brsttz))


    def testDateCommandFormatReversed(self):
        self.assertEqual(parse("2003 10:36:28 BRST 25 Sep Thu",
                               tzinfos=self.tzinfos),
                         datetime(2003, 9, 25, 10, 36, 28,
                                  tzinfo=self.brsttz))

    def testDateCommandFormatWithLong(self):
        if not PY3:
            self.assertEqual(parse("Thu Sep 25 10:36:28 BRST 2003",
                                   tzinfos={"BRST": long(-10800)}),
                             datetime(2003, 9, 25, 10, 36, 28,
                                      tzinfo=self.brsttz))
    def testDateCommandFormatIgnoreTz(self):
        self.assertEqual(parse("Thu Sep 25 10:36:28 BRST 2003",
                               ignoretz=True),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip1(self):
        self.assertEqual(parse("Thu Sep 25 10:36:28 2003"),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip2(self):
        self.assertEqual(parse("Thu Sep 25 10:36:28", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip3(self):
        self.assertEqual(parse("Thu Sep 10:36:28", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip4(self):
        self.assertEqual(parse("Thu 10:36:28", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip5(self):
        self.assertEqual(parse("Sep 10:36:28", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip6(self):
        self.assertEqual(parse("10:36:28", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testDateCommandFormatStrip7(self):
        self.assertEqual(parse("10:36", default=self.default),
                         datetime(2003, 9, 25, 10, 36))

    def testDateCommandFormatStrip8(self):
        self.assertEqual(parse("Thu Sep 25 2003"),
                         datetime(2003, 9, 25))

    def testDateCommandFormatStrip9(self):
        self.assertEqual(parse("Sep 25 2003"),
                         datetime(2003, 9, 25))

    def testDateCommandFormatStrip10(self):
        self.assertEqual(parse("Sep 2003", default=self.default),
                         datetime(2003, 9, 25))

    def testDateCommandFormatStrip11(self):
        self.assertEqual(parse("Sep", default=self.default),
                         datetime(2003, 9, 25))

    def testDateCommandFormatStrip12(self):
        self.assertEqual(parse("2003", default=self.default),
                         datetime(2003, 9, 25))

    def testDateRCommandFormat(self):
        self.assertEqual(parse("Thu, 25 Sep 2003 10:49:41 -0300"),
                         datetime(2003, 9, 25, 10, 49, 41,
                                  tzinfo=self.brsttz))

    def testISOFormat(self):
        self.assertEqual(parse("2003-09-25T10:49:41.5-03:00"),
                         datetime(2003, 9, 25, 10, 49, 41, 500000,
                                  tzinfo=self.brsttz))

    def testISOFormatStrip1(self):
        self.assertEqual(parse("2003-09-25T10:49:41-03:00"),
                         datetime(2003, 9, 25, 10, 49, 41,
                                  tzinfo=self.brsttz))

    def testISOFormatStrip2(self):
        self.assertEqual(parse("2003-09-25T10:49:41"),
                         datetime(2003, 9, 25, 10, 49, 41))

    def testISOFormatStrip3(self):
        self.assertEqual(parse("2003-09-25T10:49"),
                         datetime(2003, 9, 25, 10, 49))

    def testISOFormatStrip4(self):
        self.assertEqual(parse("2003-09-25T10"),
                         datetime(2003, 9, 25, 10))

    def testISOFormatStrip5(self):
        self.assertEqual(parse("2003-09-25"),
                         datetime(2003, 9, 25))

    def testISOStrippedFormat(self):
        self.assertEqual(parse("20030925T104941.5-0300"),
                         datetime(2003, 9, 25, 10, 49, 41, 500000,
                                  tzinfo=self.brsttz))

    def testISOStrippedFormatStrip1(self):
        self.assertEqual(parse("20030925T104941-0300"),
                         datetime(2003, 9, 25, 10, 49, 41,
                                  tzinfo=self.brsttz))

    def testISOStrippedFormatStrip2(self):
        self.assertEqual(parse("20030925T104941"),
                         datetime(2003, 9, 25, 10, 49, 41))

    def testISOStrippedFormatStrip3(self):
        self.assertEqual(parse("20030925T1049"),
                         datetime(2003, 9, 25, 10, 49, 0))

    def testISOStrippedFormatStrip4(self):
        self.assertEqual(parse("20030925T10"),
                         datetime(2003, 9, 25, 10))

    def testISOStrippedFormatStrip5(self):
        self.assertEqual(parse("20030925"),
                         datetime(2003, 9, 25))

    def testPythonLoggerFormat(self):
        self.assertEqual(parse("2003-09-25 10:49:41,502"),
                         datetime(2003, 9, 25, 10, 49, 41, 502000))

    def testNoSeparator1(self):
        self.assertEqual(parse("199709020908"),
                         datetime(1997, 9, 2, 9, 8))

    def testNoSeparator2(self):
        self.assertEqual(parse("19970902090807"),
                         datetime(1997, 9, 2, 9, 8, 7))

    def testDateWithDash1(self):
        self.assertEqual(parse("2003-09-25"),
                         datetime(2003, 9, 25))

    def testDateWithDash2(self):
        self.assertEqual(parse("2003-Sep-25"),
                         datetime(2003, 9, 25))

    def testDateWithDash3(self):
        self.assertEqual(parse("25-Sep-2003"),
                         datetime(2003, 9, 25))

    def testDateWithDash4(self):
        self.assertEqual(parse("25-Sep-2003"),
                         datetime(2003, 9, 25))

    def testDateWithDash5(self):
        self.assertEqual(parse("Sep-25-2003"),
                         datetime(2003, 9, 25))

    def testDateWithDash6(self):
        self.assertEqual(parse("09-25-2003"),
                         datetime(2003, 9, 25))

    def testDateWithDash7(self):
        self.assertEqual(parse("25-09-2003"),
                         datetime(2003, 9, 25))

    def testDateWithDash8(self):
        self.assertEqual(parse("10-09-2003", dayfirst=True),
                         datetime(2003, 9, 10))

    def testDateWithDash9(self):
        self.assertEqual(parse("10-09-2003"),
                         datetime(2003, 10, 9))

    def testDateWithDash10(self):
        self.assertEqual(parse("10-09-03"),
                         datetime(2003, 10, 9))

    def testDateWithDash11(self):
        self.assertEqual(parse("10-09-03", yearfirst=True),
                         datetime(2010, 9, 3))

    def testDateWithDot1(self):
        self.assertEqual(parse("2003.09.25"),
                         datetime(2003, 9, 25))

    def testDateWithDot2(self):
        self.assertEqual(parse("2003.Sep.25"),
                         datetime(2003, 9, 25))

    def testDateWithDot3(self):
        self.assertEqual(parse("25.Sep.2003"),
                         datetime(2003, 9, 25))

    def testDateWithDot4(self):
        self.assertEqual(parse("25.Sep.2003"),
                         datetime(2003, 9, 25))

    def testDateWithDot5(self):
        self.assertEqual(parse("Sep.25.2003"),
                         datetime(2003, 9, 25))

    def testDateWithDot6(self):
        self.assertEqual(parse("09.25.2003"),
                         datetime(2003, 9, 25))

    def testDateWithDot7(self):
        self.assertEqual(parse("25.09.2003"),
                         datetime(2003, 9, 25))

    def testDateWithDot8(self):
        self.assertEqual(parse("10.09.2003", dayfirst=True),
                         datetime(2003, 9, 10))

    def testDateWithDot9(self):
        self.assertEqual(parse("10.09.2003"),
                         datetime(2003, 10, 9))

    def testDateWithDot10(self):
        self.assertEqual(parse("10.09.03"),
                         datetime(2003, 10, 9))

    def testDateWithDot11(self):
        self.assertEqual(parse("10.09.03", yearfirst=True),
                         datetime(2010, 9, 3))

    def testDateWithSlash1(self):
        self.assertEqual(parse("2003/09/25"),
                         datetime(2003, 9, 25))

    def testDateWithSlash2(self):
        self.assertEqual(parse("2003/Sep/25"),
                         datetime(2003, 9, 25))

    def testDateWithSlash3(self):
        self.assertEqual(parse("25/Sep/2003"),
                         datetime(2003, 9, 25))

    def testDateWithSlash4(self):
        self.assertEqual(parse("25/Sep/2003"),
                         datetime(2003, 9, 25))

    def testDateWithSlash5(self):
        self.assertEqual(parse("Sep/25/2003"),
                         datetime(2003, 9, 25))

    def testDateWithSlash6(self):
        self.assertEqual(parse("09/25/2003"),
                         datetime(2003, 9, 25))

    def testDateWithSlash7(self):
        self.assertEqual(parse("25/09/2003"),
                         datetime(2003, 9, 25))

    def testDateWithSlash8(self):
        self.assertEqual(parse("10/09/2003", dayfirst=True),
                         datetime(2003, 9, 10))

    def testDateWithSlash9(self):
        self.assertEqual(parse("10/09/2003"),
                         datetime(2003, 10, 9))

    def testDateWithSlash10(self):
        self.assertEqual(parse("10/09/03"),
                         datetime(2003, 10, 9))

    def testDateWithSlash11(self):
        self.assertEqual(parse("10/09/03", yearfirst=True),
                         datetime(2010, 9, 3))

    def testDateWithSpace1(self):
        self.assertEqual(parse("2003 09 25"),
                         datetime(2003, 9, 25))

    def testDateWithSpace2(self):
        self.assertEqual(parse("2003 Sep 25"),
                         datetime(2003, 9, 25))

    def testDateWithSpace3(self):
        self.assertEqual(parse("25 Sep 2003"),
                         datetime(2003, 9, 25))

    def testDateWithSpace4(self):
        self.assertEqual(parse("25 Sep 2003"),
                         datetime(2003, 9, 25))

    def testDateWithSpace5(self):
        self.assertEqual(parse("Sep 25 2003"),
                         datetime(2003, 9, 25))

    def testDateWithSpace6(self):
        self.assertEqual(parse("09 25 2003"),
                         datetime(2003, 9, 25))

    def testDateWithSpace7(self):
        self.assertEqual(parse("25 09 2003"),
                         datetime(2003, 9, 25))

    def testDateWithSpace8(self):
        self.assertEqual(parse("10 09 2003", dayfirst=True),
                         datetime(2003, 9, 10))

    def testDateWithSpace9(self):
        self.assertEqual(parse("10 09 2003"),
                         datetime(2003, 10, 9))

    def testDateWithSpace10(self):
        self.assertEqual(parse("10 09 03"),
                         datetime(2003, 10, 9))

    def testDateWithSpace11(self):
        self.assertEqual(parse("10 09 03", yearfirst=True),
                         datetime(2010, 9, 3))

    def testDateWithSpace12(self):
        self.assertEqual(parse("25 09 03"),
                         datetime(2003, 9, 25))

    def testStrangelyOrderedDate1(self):
        self.assertEqual(parse("03 25 Sep"),
                         datetime(2003, 9, 25))

    def testStrangelyOrderedDate2(self):
        self.assertEqual(parse("2003 25 Sep"),
                         datetime(2003, 9, 25))

    def testStrangelyOrderedDate3(self):
        self.assertEqual(parse("25 03 Sep"),
                         datetime(2025, 9, 3))

    def testHourWithLetters(self):
        self.assertEqual(parse("10h36m28.5s", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28, 500000))

    def testHourWithLettersStrip1(self):
        self.assertEqual(parse("10h36m28s", default=self.default),
                         datetime(2003, 9, 25, 10, 36, 28))

    def testHourWithLettersStrip2(self):
        self.assertEqual(parse("10h36m", default=self.default),
                         datetime(2003, 9, 25, 10, 36))

    def testHourWithLettersStrip3(self):
        self.assertEqual(parse("10h", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourWithLettersStrip4(self):
        self.assertEqual(parse("10 h 36", default=self.default),
                         datetime(2003, 9, 25, 10, 36))

    def testHourAmPm1(self):
        self.assertEqual(parse("10h am", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourAmPm2(self):
        self.assertEqual(parse("10h pm", default=self.default),
                         datetime(2003, 9, 25, 22))

    def testHourAmPm3(self):
        self.assertEqual(parse("10am", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourAmPm4(self):
        self.assertEqual(parse("10pm", default=self.default),
                         datetime(2003, 9, 25, 22))

    def testHourAmPm5(self):
        self.assertEqual(parse("10:00 am", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourAmPm6(self):
        self.assertEqual(parse("10:00 pm", default=self.default),
                         datetime(2003, 9, 25, 22))

    def testHourAmPm7(self):
        self.assertEqual(parse("10:00am", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourAmPm8(self):
        self.assertEqual(parse("10:00pm", default=self.default),
                         datetime(2003, 9, 25, 22))

    def testHourAmPm9(self):
        self.assertEqual(parse("10:00a.m", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourAmPm10(self):
        self.assertEqual(parse("10:00p.m", default=self.default),
                         datetime(2003, 9, 25, 22))

    def testHourAmPm11(self):
        self.assertEqual(parse("10:00a.m.", default=self.default),
                         datetime(2003, 9, 25, 10))

    def testHourAmPm12(self):
        self.assertEqual(parse("10:00p.m.", default=self.default),
                         datetime(2003, 9, 25, 22))

    def testPertain(self):
        self.assertEqual(parse("Sep 03", default=self.default),
                         datetime(2003, 9, 3))
        self.assertEqual(parse("Sep of 03", default=self.default),
                         datetime(2003, 9, 25))

    def testWeekdayAlone(self):
        self.assertEqual(parse("Wed", default=self.default),
                         datetime(2003, 10, 1))

    def testLongWeekday(self):
        self.assertEqual(parse("Wednesday", default=self.default),
                         datetime(2003, 10, 1))

    def testLongMonth(self):
        self.assertEqual(parse("October", default=self.default),
                         datetime(2003, 10, 25))

    def testZeroYear(self):
        self.assertEqual(parse("31-Dec-00", default=self.default),
                         datetime(2000, 12, 31))

    def testFuzzy(self):
        s = "Today is 25 of September of 2003, exactly " \
            "at 10:49:41 with timezone -03:00."
        self.assertEqual(parse(s, fuzzy=True),
                         datetime(2003, 9, 25, 10, 49, 41,
                                  tzinfo=self.brsttz))

    def testFuzzyWithTokens(self):
        s = "Today is 25 of September of 2003, exactly " \
            "at 10:49:41 with timezone -03:00."
        self.assertEqual(parse(s, fuzzy_with_tokens=True),
                         (datetime(2003, 9, 25, 10, 49, 41,
                                   tzinfo=self.brsttz),
                         ('Today is ', 'of ', ', exactly at ',
                          ' with timezone ', '.')))

    def testFuzzyAMPMProblem(self):
        # Sometimes fuzzy parsing results in AM/PM flag being set without
        # hours - if it's fuzzy it should ignore that.
        s1 = "I have a meeting on March 1, 1974."
        s2 = "On June 8th, 2020, I am going to be the first man on Mars"

        # Also don't want any erroneous AM or PMs changing the parsed time
        s3 = "Meet me at the AM/PM on Sunset at 3:00 AM on December 3rd, 2003"
        s4 = "Meet me at 3:00AM on December 3rd, 2003 at the AM/PM on Sunset"

        self.assertEqual(parse(s1, fuzzy=True), datetime(1974, 3, 1))
        self.assertEqual(parse(s2, fuzzy=True), datetime(2020, 6, 8))
        self.assertEqual(parse(s3, fuzzy=True), datetime(2003, 12, 3, 3))
        self.assertEqual(parse(s4, fuzzy=True), datetime(2003, 12, 3, 3))

    def testExtraSpace(self):
        self.assertEqual(parse("  July   4 ,  1976   12:01:02   am  "),
                         datetime(1976, 7, 4, 0, 1, 2))

    def testRandomFormat1(self):
        self.assertEqual(parse("Wed, July 10, '96"),
                         datetime(1996, 7, 10, 0, 0))

    def testRandomFormat2(self):
        self.assertEqual(parse("1996.07.10 AD at 15:08:56 PDT",
                               ignoretz=True),
                         datetime(1996, 7, 10, 15, 8, 56))

    def testRandomFormat3(self):
        self.assertEqual(parse("1996.July.10 AD 12:08 PM"),
                         datetime(1996, 7, 10, 12, 8))

    def testRandomFormat4(self):
        self.assertEqual(parse("Tuesday, April 12, 1952 AD 3:30:42pm PST",
                               ignoretz=True),
                         datetime(1952, 4, 12, 15, 30, 42))

    def testRandomFormat5(self):
        self.assertEqual(parse("November 5, 1994, 8:15:30 am EST",
                               ignoretz=True),
                         datetime(1994, 11, 5, 8, 15, 30))

    def testRandomFormat6(self):
        self.assertEqual(parse("1994-11-05T08:15:30-05:00",
                               ignoretz=True),
                         datetime(1994, 11, 5, 8, 15, 30))

    def testRandomFormat7(self):
        self.assertEqual(parse("1994-11-05T08:15:30Z",
                               ignoretz=True),
                         datetime(1994, 11, 5, 8, 15, 30))

    def testRandomFormat8(self):
        self.assertEqual(parse("July 4, 1976"), datetime(1976, 7, 4))

    def testRandomFormat9(self):
        self.assertEqual(parse("7 4 1976"), datetime(1976, 7, 4))

    def testRandomFormat10(self):
        self.assertEqual(parse("4 jul 1976"), datetime(1976, 7, 4))

    def testRandomFormat11(self):
        self.assertEqual(parse("7-4-76"), datetime(1976, 7, 4))

    def testRandomFormat12(self):
        self.assertEqual(parse("19760704"), datetime(1976, 7, 4))

    def testRandomFormat13(self):
        self.assertEqual(parse("0:01:02", default=self.default),
                         datetime(2003, 9, 25, 0, 1, 2))

    def testRandomFormat14(self):
        self.assertEqual(parse("12h 01m02s am", default=self.default),
                         datetime(2003, 9, 25, 0, 1, 2))

    def testRandomFormat15(self):
        self.assertEqual(parse("0:01:02 on July 4, 1976"),
                         datetime(1976, 7, 4, 0, 1, 2))

    def testRandomFormat16(self):
        self.assertEqual(parse("0:01:02 on July 4, 1976"),
                         datetime(1976, 7, 4, 0, 1, 2))

    def testRandomFormat17(self):
        self.assertEqual(parse("1976-07-04T00:01:02Z", ignoretz=True),
                         datetime(1976, 7, 4, 0, 1, 2))

    def testRandomFormat18(self):
        self.assertEqual(parse("July 4, 1976 12:01:02 am"),
                         datetime(1976, 7, 4, 0, 1, 2))

    def testRandomFormat19(self):
        self.assertEqual(parse("Mon Jan  2 04:24:27 1995"),
                         datetime(1995, 1, 2, 4, 24, 27))

    def testRandomFormat20(self):
        self.assertEqual(parse("Tue Apr 4 00:22:12 PDT 1995", ignoretz=True),
                         datetime(1995, 4, 4, 0, 22, 12))

    def testRandomFormat21(self):
        self.assertEqual(parse("04.04.95 00:22"),
                         datetime(1995, 4, 4, 0, 22))

    def testRandomFormat22(self):
        self.assertEqual(parse("Jan 1 1999 11:23:34.578"),
                         datetime(1999, 1, 1, 11, 23, 34, 578000))

    def testRandomFormat23(self):
        self.assertEqual(parse("950404 122212"),
                         datetime(1995, 4, 4, 12, 22, 12))

    def testRandomFormat24(self):
        self.assertEqual(parse("0:00 PM, PST", default=self.default,
                               ignoretz=True),
                         datetime(2003, 9, 25, 12, 0))

    def testRandomFormat25(self):
        self.assertEqual(parse("12:08 PM", default=self.default),
                         datetime(2003, 9, 25, 12, 8))

    def testRandomFormat26(self):
        self.assertEqual(parse("5:50 A.M. on June 13, 1990"),
                         datetime(1990, 6, 13, 5, 50))

    def testRandomFormat27(self):
        self.assertEqual(parse("3rd of May 2001"), datetime(2001, 5, 3))

    def testRandomFormat28(self):
        self.assertEqual(parse("5th of March 2001"), datetime(2001, 3, 5))

    def testRandomFormat29(self):
        self.assertEqual(parse("1st of May 2003"), datetime(2003, 5, 1))

    def testRandomFormat30(self):
        self.assertEqual(parse("01h02m03", default=self.default),
                         datetime(2003, 9, 25, 1, 2, 3))

    def testRandomFormat31(self):
        self.assertEqual(parse("01h02", default=self.default),
                         datetime(2003, 9, 25, 1, 2))

    def testRandomFormat32(self):
        self.assertEqual(parse("01h02s", default=self.default),
                         datetime(2003, 9, 25, 1, 0, 2))

    def testRandomFormat33(self):
        self.assertEqual(parse("01m02", default=self.default),
                         datetime(2003, 9, 25, 0, 1, 2))

    def testRandomFormat34(self):
        self.assertEqual(parse("01m02h", default=self.default),
                         datetime(2003, 9, 25, 2, 1))

    def testRandomFormat35(self):
        self.assertEqual(parse("2004 10 Apr 11h30m", default=self.default),
                         datetime(2004, 4, 10, 11, 30))

    # Test that if a year is omitted, we use the most recent matching value
    def testSmartDefaultsNoYearMonthEarlier(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 5, 1),
                               smart_defaults=True), 
                         datetime(2013, 8, 3))

    def testSmartDefaultsNoYearDayEarlier(self):        
        self.assertEqual(parse("August 3", default=datetime(2014, 8, 1),
                               smart_defaults=True), 
                         datetime(2013, 8, 3))

    def testSmartDefaultsNoYearSameDay(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 8, 3),
                               smart_defaults=True), 
                         datetime(2014, 8, 3))

    def testSmartDefaultsNoYearDayLater(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 8, 4),
                               smart_defaults=True), 
                         datetime(2014, 8, 3))
    
    def testSmartDefaultsNoYearMonthLater(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 12, 19),
                               smart_defaults=True), 
                         datetime(2014, 8, 3))

    def testSmartDefaultsNoYearFeb29(self):
        self.assertEqual(parse("February 29", default=datetime(2014, 12, 19),
                               date_in_future=False, smart_defaults=True),
                         datetime(2012, 2, 29))

    def testSmartDefaultsNoYearFeb29Y2100(self):
        # Year 2000 was not a leap year.
        self.assertEqual(parse("February 29", default=datetime(2100, 12, 19),
                               smart_defaults=True),
                         datetime(2096, 2, 29))

    # Test that if a year is omitted, we use the most next matching value
    def testSmartDefaultsNoYearFutureDayEarlier(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 5, 1),
                               date_in_future=True, smart_defaults=True),
                         datetime(2014, 8, 3))

    def testSmartDefaultsNoYearFutureMonthEarlier(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 8, 1),
                               date_in_future=True, smart_defaults=True),
                         datetime(2014, 8, 3))

    def testSmartDefaultsNoYearFutureSameDay(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 8, 3),
                               date_in_future=True, smart_defaults=True),
                         datetime(2014, 8, 3))

    def testSmartDefaultsNoYearFutureDayLater(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 8, 4),
                               date_in_future=True, smart_defaults=True),
                         datetime(2015, 8, 3))
    
    def testSmartDefaultsNoYearFutureMonthLater(self):
        self.assertEqual(parse("August 3", default=datetime(2014, 12, 19),
                               date_in_future=True, smart_defaults=True),
                         datetime(2015, 8, 3))

    def testSmartDefaultsNoYearFutureFeb29Y2100(self):
        self.assertEqual(parse("February 29", default=datetime(2098, 12, 19),
                               date_in_future=True, smart_defaults=True),
                         datetime(2104, 2, 29))

    # Test that if only a month is provided, we select the beginning of the most recent
    # occurrence of the specified month
    def testSmartDefaultsMonthOnlyMonthEarlier(self):
        self.assertEqual(parse("September", default=datetime(2014, 5, 1),
                               smart_defaults=True),
                         datetime(2013, 9, 1))

    def testSmartDefaultsMonthOnlySameMonthFirstDay(self):
        self.assertEqual(parse("September", default=datetime(2014, 9, 1),
                               smart_defaults=True),
                         datetime(2014, 9, 1))

    def testSmartDefaultsMonthOnlySameMonthLastDay(self):
        self.assertEqual(parse("September", default=datetime(2014, 9, 30),
                               smart_defaults=True),
                         datetime(2014, 9, 1))

    def testSmartDefaultMonthOnlyMonthLater(self):
        self.assertEqual(parse("September", default=datetime(2014, 11, 1),
                               smart_defaults=True),
                         datetime(2014, 9, 1))

    # Test that if only a month is provided, we select the beginning of the most recent
    # occurrence of the specified month
    def testSmartDefaultsMonthOnlyFutureMonthEarlier(self):
        self.assertEqual(parse("September", default=datetime(2014, 5, 1),
                               date_in_future=True, smart_defaults=True),
                         datetime(2014, 9, 1))

    def testSmartDefaultsMonthOnlyFutureSameMonthFirstDay(self):
        self.assertEqual(parse("September", default=datetime(2014, 9, 1),
                               date_in_future=True, smart_defaults=True),
                         datetime(2014, 9, 1))

    def testSmartDefaultsMonthOnlyFutureSameMonthLastDay(self):
        self.assertEqual(parse("September", default=datetime(2014, 9, 30),
                               date_in_future=True, smart_defaults=True),
                         datetime(2014, 9, 1))
    
    def testSmartDefaultsMonthOnlyFutureMonthLater(self):
        self.assertEqual(parse("September", default=datetime(2014, 11, 1),
                               date_in_future=True, smart_defaults=True),
                         datetime(2015, 9, 1))

    # Test to ensure that if a year is specified, January 1st of that year is
    # returned.
    def testSmartDefaultsYearOnly(self):
        self.assertEqual(parse("2009", smart_defaults=True),
                         datetime(2009, 1, 1))

    def testSmartDefaultsYearOnlyFuture(self):
        self.assertEqual(parse("2009", smart_defaults=True,
                               date_in_future=True),
                         datetime(2009, 1, 1))

    # Tests that invalid days fall back to the end of the month if that's
    # the desired behavior.
    def testInvalidDayNoFallback(self):
        self.assertRaises(ValueError, parse, "Feb 30, 2007",
                          **{'fallback_on_invalid_day':False})

    def testInvalidDayFallbackFebNoLeapYear(self):
        self.assertEqual(parse("Feb 31, 2007", fallback_on_invalid_day=True),
                         datetime(2007, 2, 28))

    def testInvalidDayFallbackFebLeapYear(self):
        self.assertEqual(parse("Feb 31, 2008", fallback_on_invalid_day=True),
                         datetime(2008, 2, 29))

    def testUnspecifiedDayNoFallback(self):
        self.assertRaises(ValueError, parse, "April 2009",
                          **{'fallback_on_invalid_day':False,
                             'default':datetime(2010, 1, 31)})

    def testUnspecifiedDayUnspecifiedFallback(self):
        self.assertEqual(parse("April 2009", default=datetime(2010, 1, 31)),
                         datetime(2009, 4, 30))

    def testUnspecifiedDayUnspecifiedFallback(self):
        self.assertEqual(parse("April 2009", fallback_on_invalid_day=True,
                               default=datetime(2010, 1, 31)),
                         datetime(2009, 4, 30))

    def testUnspecifiedDayUnspecifiedFallbackFebNoLeapYear(self):        
        self.assertEqual(parse("Feb 2007", default=datetime(2010, 1, 31)),
                         datetime(2007, 2, 28))

    def testUnspecifiedDayUnspecifiedFallbackFebLeapYear(self):        
        self.assertEqual(parse("Feb 2008", default=datetime(2010, 1, 31)),
                         datetime(2008, 2, 29))

    def testErrorType01(self):
        self.assertRaises(ValueError,
                          parse, 'shouldfail')

    def testCorrectErrorOnFuzzyWithTokens(self):
        assertRaisesRegex(self, ValueError, 'Unknown string format',
                          parse, '04/04/32/423', fuzzy_with_tokens=True)
        assertRaisesRegex(self, ValueError, 'Unknown string format',
                          parse, '04/04/04 +32423', fuzzy_with_tokens=True)
        assertRaisesRegex(self, ValueError, 'Unknown string format',
                          parse, '04/04/0d4', fuzzy_with_tokens=True)

    def testIncreasingCTime(self):
        # This test will check 200 different years, every month, every day,
        # every hour, every minute, every second, and every weekday, using
        # a delta of more or less 1 year, 1 month, 1 day, 1 minute and
        # 1 second.
        delta = timedelta(days=365+31+1, seconds=1+60+60*60)
        dt = datetime(1900, 1, 1, 0, 0, 0, 0)
        for i in range(200):
            self.assertEqual(parse(dt.ctime()), dt)
            dt += delta

    def testIncreasingISOFormat(self):
        delta = timedelta(days=365+31+1, seconds=1+60+60*60)
        dt = datetime(1900, 1, 1, 0, 0, 0, 0)
        for i in range(200):
            self.assertEqual(parse(dt.isoformat()), dt)
            dt += delta

    def testMicrosecondsPrecisionError(self):
        # Skip found out that sad precision problem. :-(
        dt1 = parse("00:11:25.01")
        dt2 = parse("00:12:10.01")
        self.assertEqual(dt1.microsecond, 10000)
        self.assertEqual(dt2.microsecond, 10000)

    def testMicrosecondPrecisionErrorReturns(self):
        # One more precision issue, discovered by Eric Brown.  This should
        # be the last one, as we're no longer using floating points.
        for ms in [100001, 100000, 99999, 99998,
                    10001,  10000,  9999,  9998,
                     1001,   1000,   999,   998,
                      101,    100,    99,    98]:
            dt = datetime(2008, 2, 27, 21, 26, 1, ms)
            self.assertEqual(parse(dt.isoformat()), dt)

    def testHighPrecisionSeconds(self):
        self.assertEqual(parse("20080227T21:26:01.123456789"),
                          datetime(2008, 2, 27, 21, 26, 1, 123456))

    def testCustomParserInfo(self):
        # Custom parser info wasn't working, as Michael Elsdörfer discovered.
        from dateutil.parser import parserinfo, parser

        class myparserinfo(parserinfo):
            MONTHS = parserinfo.MONTHS[:]
            MONTHS[0] = ("Foo", "Foo")
        myparser = parser(myparserinfo())
        dt = myparser.parse("01/Foo/2007")
        self.assertEqual(dt, datetime(2007, 1, 1))

    def testParseStr(self):
        self.assertEqual(parse(self.str_str),
                         parse(self.uni_str))

    def testParserParseStr(self):
        from dateutil.parser import parser

        self.assertEqual(parser().parse(self.str_str),
                         parser().parse(self.uni_str))

    def testParseUnicodeWords(self):

        class rus_parserinfo(parserinfo):
            MONTHS = [("янв", "Январь"),
                      ("фев", "Февраль"),
                      ("мар", "Март"),
                      ("апр", "Апрель"),
                      ("май", "Май"),
                      ("июн", "Июнь"),
                      ("июл", "Июль"),
                      ("авг", "Август"),
                      ("сен", "Сентябрь"),
                      ("окт", "Октябрь"),
                      ("ноя", "Ноябрь"),
                      ("дек", "Декабрь")]

        self.assertEqual(parse('10 Сентябрь 2015 10:20',
                               parserinfo=rus_parserinfo()),
                         datetime(2015, 9, 10, 10, 20))


class EasterTest(unittest.TestCase):
    easterlist = [
                  # WESTERN            ORTHODOX
                  (date(1990, 4, 15), date(1990, 4, 15)),
                  (date(1991, 3, 31), date(1991, 4,  7)),
                  (date(1992, 4, 19), date(1992, 4, 26)),
                  (date(1993, 4, 11), date(1993, 4, 18)),
                  (date(1994, 4,  3), date(1994, 5,  1)),
                  (date(1995, 4, 16), date(1995, 4, 23)),
                  (date(1996, 4,  7), date(1996, 4, 14)),
                  (date(1997, 3, 30), date(1997, 4, 27)),
                  (date(1998, 4, 12), date(1998, 4, 19)),
                  (date(1999, 4,  4), date(1999, 4, 11)),

                  (date(2000, 4, 23), date(2000, 4, 30)),
                  (date(2001, 4, 15), date(2001, 4, 15)),
                  (date(2002, 3, 31), date(2002, 5,  5)),
                  (date(2003, 4, 20), date(2003, 4, 27)),
                  (date(2004, 4, 11), date(2004, 4, 11)),
                  (date(2005, 3, 27), date(2005, 5,  1)),
                  (date(2006, 4, 16), date(2006, 4, 23)),
                  (date(2007, 4,  8), date(2007, 4,  8)),
                  (date(2008, 3, 23), date(2008, 4, 27)),
                  (date(2009, 4, 12), date(2009, 4, 19)),

                  (date(2010, 4,  4), date(2010, 4,  4)),
                  (date(2011, 4, 24), date(2011, 4, 24)),
                  (date(2012, 4,  8), date(2012, 4, 15)),
                  (date(2013, 3, 31), date(2013, 5,  5)),
                  (date(2014, 4, 20), date(2014, 4, 20)),
                  (date(2015, 4,  5), date(2015, 4, 12)),
                  (date(2016, 3, 27), date(2016, 5,  1)),
                  (date(2017, 4, 16), date(2017, 4, 16)),
                  (date(2018, 4,  1), date(2018, 4,  8)),
                  (date(2019, 4, 21), date(2019, 4, 28)),

                  (date(2020, 4, 12), date(2020, 4, 19)),
                  (date(2021, 4,  4), date(2021, 5,  2)),
                  (date(2022, 4, 17), date(2022, 4, 24)),
                  (date(2023, 4,  9), date(2023, 4, 16)),
                  (date(2024, 3, 31), date(2024, 5,  5)),
                  (date(2025, 4, 20), date(2025, 4, 20)),
                  (date(2026, 4,  5), date(2026, 4, 12)),
                  (date(2027, 3, 28), date(2027, 5,  2)),
                  (date(2028, 4, 16), date(2028, 4, 16)),
                  (date(2029, 4,  1), date(2029, 4,  8)),

                  (date(2030, 4, 21), date(2030, 4, 28)),
                  (date(2031, 4, 13), date(2031, 4, 13)),
                  (date(2032, 3, 28), date(2032, 5,  2)),
                  (date(2033, 4, 17), date(2033, 4, 24)),
                  (date(2034, 4,  9), date(2034, 4,  9)),
                  (date(2035, 3, 25), date(2035, 4, 29)),
                  (date(2036, 4, 13), date(2036, 4, 20)),
                  (date(2037, 4,  5), date(2037, 4,  5)),
                  (date(2038, 4, 25), date(2038, 4, 25)),
                  (date(2039, 4, 10), date(2039, 4, 17)),

                  (date(2040, 4,  1), date(2040, 5,  6)),
                  (date(2041, 4, 21), date(2041, 4, 21)),
                  (date(2042, 4,  6), date(2042, 4, 13)),
                  (date(2043, 3, 29), date(2043, 5,  3)),
                  (date(2044, 4, 17), date(2044, 4, 24)),
                  (date(2045, 4,  9), date(2045, 4,  9)),
                  (date(2046, 3, 25), date(2046, 4, 29)),
                  (date(2047, 4, 14), date(2047, 4, 21)),
                  (date(2048, 4,  5), date(2048, 4,  5)),
                  (date(2049, 4, 18), date(2049, 4, 25)),

                  (date(2050, 4, 10), date(2050, 4, 17)),
                ]

    def testEaster(self):
        for western, orthodox in self.easterlist:
            self.assertEqual(western,  easter(western.year,  EASTER_WESTERN))
            self.assertEqual(orthodox, easter(orthodox.year, EASTER_ORTHODOX))


# vim:ts=4:sw=4
