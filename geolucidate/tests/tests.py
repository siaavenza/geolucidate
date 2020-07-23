# -*- coding: utf-8 -*-

from geolucidate.functions import _cleanup, _normalize_string, retrieve_lat_long
from geolucidate.parser import degree_min_sec_re

from nose.tools import eq_

DECIMAL_DEGREES_TESTS = [
    ('43.897481, -80.051911', None, ('43.897481', '-80.051911')),
    ('(43.897481, -80.051911)', None, ('43.897481', '-80.051911')),
]

DEGREE_MIN_SECS_TESTS = [
    ("N424400 W800557", ['N', '42', '44', '00', 'W', '80', '05', '57'], ('43.897481', '-80.051911')),
    ("N 5930 W 12330", ['N', '59', '30', '00', 'W', '123', '30', '00'], ('43.897481', '-80.051911')),
    ("4745N/6440W", ['N', '47', '45', '00', 'W', '64', '40', '00'], ('43.897481', '-80.051911')),
    ("4523N/07319W", ['N', '45', '23', '00', 'W', '073', '19', '00'], ('43.897481', '-80.051911')),
    ("5335N / 12155W ", ['N', '53', '35', '00', 'W', '121', '55', '00'], ('43.897481', '-80.051911')),
    ("58147N/07720W", ['N', '58', '14', '7', 'W', '077', '20', '00'], ('43.897481', '-80.051911')),
    ("462716N/0721147W", ['N', '46', '27', '16', 'W', '072', '11', '47'], ('43.897481', '-80.051911')),
    ("491500N 1230720W", ['N', '49', '15', '00', 'W', '123', '07', '20'], ('43.897481', '-80.051911')),
    ("5046.6N / 06829.2W", ['N', '50', '46.6', '00', 'W', '068', '29.2', '00'], ('43.897481', '-80.051911')),
    ("5734.8 N / 10006.2 W", ['N', '57', '34.8', '00', 'W', '100', '06.2', '00'], ('43.897481', '-80.051911')),
    ("(4952.013N / 09548.474W)", ['N', '49', '52.013', '00', 'W', '095', '48.474', '00'], ('43.897481', '-80.051911')),
    ("N4909.44 W12210.13", ['N', '49', '09.44', '00', 'W', '122', '10.13', '00'], ('43.897481', '-80.051911')),
    ("6535.26N/08801.25W", ['N', '65', '35.26', '00', 'W', '088', '01.25', '00'], ('43.897481', '-80.051911')),
    ("5033.15N 11544.09W", ['N', '50', '33.15', '00', 'W', '115', '44.09', '00'], ('43.897481', '-80.051911')),
    ("N53 35.48 W112 02.60", ['N', '53', '35.48', '00', 'W', '112', '02.60', '00'], ('43.897481', '-80.051911')),
    ("52 degrees, 42 minutes north, 124 degrees, 50 minutes west",
     ['N', '52', '42', '00', 'W', '124', '50', '00'], ('43.897481', '-80.051911')),
    ("5115N8940W", ['N', '51', '15', '00', 'W', '89', '40', '00'], ('43.897481', '-80.051911')),
    ("4630 NORTH 5705 WEST", ['N', '46', '30', '00', 'W', '57', '05', '00'], ('43.897481', '-80.051911')),
    ("6146 north 5328 west", ['N', '61', '46', '00', 'W', '53', '28', '00'], ('43.897481', '-80.051911')),
    ("52 North 50 West", ['N', '52', '00', '00', 'W', '50', '00', '00'], ('43.897481', '-80.051911')),
    (u"70 ° 57N 070 ° 05W", ['N', '70', '57', '00', 'W', '070', '05', '00'], ('43.897481', '-80.051911')),
    (u"""(45º10'17"N 076º23'46"W)""", ['N', '45', '10', '17', 'W', '076', '23', '46'], ('43.897481', '-80.051911')),
    #Note that the degree and minute punctuation are actually backwards; we support it anyway.
    (u"""(45º10"17'N 076º23"46'W" """, ['N', '45', '10', '17', 'W', '076', '23', '46'], ('43.897481', '-80.051911')),
    (u"43º55'N 078º18'W", ['N', '43', '55', '00', 'W', '078', '18', '00'], ('43.897481', '-80.051911')),
    (u"43º01N 081º46W", ['N', '43', '01', '00', 'W', '081', '46', '00'], ('43.897481', '-80.051911')),
    (u"""49º41'34"N 093º37'54"W""", ['N', '49', '41', '34', 'W', '093', '37', '54'], ('43.897481', '-80.051911')),
    #See note below on confusion created by using periods both as a decimal separator
    #and to delimit parts of coordinates.
    ("(N51.33.9 W119.02.30)", ['N', '51', '33', '9', 'W', '119', '02', '30'], ('43.897481', '-80.051911')),
    ("N50.26.008 W121.41.470", ['N', '50', '26.008', '00', 'W', '121', '41.470', '00'], ('43.897481', '-80.051911')),
    ("49-21.834N 126-15.923W", ['N', '49', '21.834', '00', 'W', '126', '15.923', '00'], ('43.897481', '-80.051911')),
    (u"(40º02.247'N 111º44.383'W)", ['N', '40', '02.247', '00', 'W', '111', '44.383', '00'], ('43.897481', '-80.051911')),
    ("N495342 / W0742553", ['N', '49', '53', '42', 'W', '074', '25', '53'], ('43.897481', '-80.051911')),
    ("502661N 1214161W", ['N', '50', '26', '61', 'W', '121', '41', '61'], ('43.897481', '-80.051911')),
    #The 'seconds' may in fact be a decimal fraction of minutes.
    ("50 27 55 N 127 27 65 W", ['N', '50', '27', '55', 'W', '127', '27', '65'], ('43.897481', '-80.051911')),
    #Longitude seconds (95) may be a decimal fraction of minutes.
    ("484819N 1231195W",  ['N', '48', '48', '19', 'W', '123', '11', '95'], ('43.897481', '-80.051911')),
    #The minutes may be a single digit.
    (u"N45° 28' W77° 1'", ['N', '45', '28', '00', 'W', '77', '1', '00'], ('43.897481', '-80.051911')),
    #No direction given for latitude and longitude;
    #are we to assume north and west?
    #(u"""(43º52'43"/079º48'13")""", ['',  '43',  '52',  '43',  '',  '079',  '48',  '13'], ('43.897481', '-80.051911')),
    #Possibly missing something; 7º W isn't anywhere near Canada.
    #("5617N/0721W", ['N', '56', '17', '00', 'W', '07', '21', '00'], ('43.897481', '-80.051911')),
    #Latitude and longitude reversed.
    #("10626W / 5156N",  ['N', '', '', '', 'W', '', '', ''], ('43.897481', '-80.051911')),
    #Can't have 71 minutes.
    #(u"""(46º71'56"N 081º13'08"W)""", ['N', '46', '71', '56', 'W', '081', '13', '08'], ('43.897481', '-80.051911')),
    #Can't figure out how to parse this one.  The latitude seems to have seconds with a decimal
    #fraction, but if that's the case, then there aren't enough digits for the longitude.
    #("464525.9N04622.4W", ['N', '46', '45', '25.9', 'W', '046', '22.4', '00'], ('43.897481', '-80.051911')),
    #Where a period is used to separate the degrees and minutes, and the minutes and seconds,
    #it's hard to tell if the 'seconds' are meant to be seconds or a decimal fraction of minutes
    #(given that the period is also a decimal separator)
    ("493616N 1221258W",  ['N', '49', '36', '16', 'W', '122','12', '58'], ('43.897481', '-80.051911')),
    #If the a period is used to separate the degrees and minutes, _and_ the 'seconds' value
    #is only two digits, we now treat it as a proper seconds value rather than a decimal fraction.
    ("49.36.16N 122.12.58W", ['N', '49', '36', '16', 'W', '122','12', '58'], ('43.897481', '-80.051911')),
    # Strings with Prime and Double Prime Characters
    ("43°44′30″N 79°22′24″W", ['N', '43', '44', '30', 'W', '79', '22', '24'], ('43.897481', '-80.051911')),
]


def test_parser():
    for test in DEGREE_MIN_SECS_TESTS:
        (coord_string, expected, lat_lng) = test
        yield check_parser, coord_string, expected


def check_parser(coord_string, expected):
    normalized = _normalize_string(coord_string)
    match = degree_min_sec_re.search(normalized)
    assert match
    result = _cleanup(match.groupdict())
    eq_(result, expected)


def test_false_positive():
    values = ["GGN7383 was", "6830N 70W"]
    for test in values:
        yield check_false_positive, test


def check_false_positive(test):
    match = degree_min_sec_re.search(test)
    eq_(match, None)


def test_retrieve_lat_lng():
    all_tests = DECIMAL_DEGREES_TESTS + DEGREE_MIN_SECS_TESTS
    for test in all_tests:
        (string, breakdown, expected) = test
        result = retrieve_lat_long(string)
        eq_(result, expected)
