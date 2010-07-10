# -*- coding: utf-8 -*-

from geolucidate.functions import cleanup
from geolucidate.parser import parser_re

def test_parser():
    values = [
        ("N424400 W800557", ['N','42','44','00','W','80','05','57']),
        ("4745N/6440W", ['N','47','45','00','W','64','40','00']),
        ("4834N/06639W", ['N','48','34','00','W','066','39','00']),
        ("4645N/06602W", ['N','46','45','00','W','066','02','00']),
        ("5719N/07453W", ['N','57','19','00','W','074','53','00']),
        ("5615N/11320W", ['N','56','15','00','W','113','20','00']),
        ("4523N/07319W", ['N','45','23','00','W','073','19','00']),
        ("58147N/07720W", ['N','58','14','7','W','077','20','00']),
        ("6828N/8234W", ['N','68','28','00','W','82','34','00']),
        ("5046.6N / 06829.2W", ['N','50','46.6','00','W','068','29.2','00']),
        ("5734.8 N / 10006.2 W", ['N','57','34.8','00','W','100','06.2','00']),
        ("6535.26N/08801.25W", ['N','65','35.26','00','W','088','01.25','00']),
        ("5033.15N 11544.09W", ['N','50','33.15','00','W','115','44.09','00']),
        ("N53 35.48 W112 02.60", ['N','53','35.48','00','W','112','02.60','00']),
        ("52 degrees, 42 minutes north, 124 degrees, 50 minutes west", ['N','52','42','00','W','124','50','00']),
        (u"49º41\'34\"N 093º37\'54\"W", ['N','49','41','34','W','093','37','54']),
        ("5115N8940W", ['N','51','15','00','W','89','40','00']),
        ("4630 NORTH 5705 WEST", ['N','46','30','00','W','57','05','00']),
        ("6146 north 5328 west", ['N','61','46','00','W','53','28','00']),
        (u"43º01N 081º46W", ['N','43','01','00','W','081','46','00']),
        ("52 North 50 West", ['N','52','00','00','W','50','00','00']),
        ("462716N/0721147W", ['N','46','27','16','W','072','11','47']),
        ("491500N 1230720W", ['N','49','15','00','W','123','07','20']),
        ("490600N 1163000W", ['N','49','06','00','W','116','30','00']),
        ("490103N 1235145W", ['N','49','01','03','W','123','51','45'])
        #Possibly missing something; 7º W isn't anywhere near Canada.
        #("5617N/0721W", ['N','56','17','00','W','07','21','00']),
        #Latitude and longitude reversed.
        #("10626W / 5156N", ['N','','','','W','','','']),
        #Longitude seconds (78) impossible.
        #("491129N 1230778W", ['N','49','11','29','W','123','07','78']),
        #Longitude seconds (95) impossible.
        #("484819N 1231195W", ['N','48','48','13','W','123','11','95']),
        ]

    for test in values:
        (coord_string, result) = test
        yield check_parser, coord_string, result

def check_parser(coord_string, result):
    match = parser_re.search(coord_string)
    assert match
    assert cleanup(match.groupdict()) == result