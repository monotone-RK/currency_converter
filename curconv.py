#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import urllib2
import argparse
import locale

#**  Currency code(ISO 4217) and Locale ID                                   **/
#******************************************************************************/
dic = {
    "JPY": "ja_JP",
    "USD": "en_US",
    "EUR": u"\u20AC",  # EURO SIGN
    "KRW": "ko_KR",
    "GBP": "en_GB",
    "CNY": "zh_CN"}

#**  Functions                                                               **/
#******************************************************************************/
def currencyConverter(FROM, TO, VALUE):
    # ----- Error Check ----- #
    if FROM == "ALL":
        err_message = 'ERROR!\n"ALL" is not available as curcode_from.\nIf curcode_to, "ALL" can be used.'
        sys.exit(err_message)
    elif (FROM not in dic) or ((TO not in dic) and (TO != "ALL")):
        err_message = "ERROR!\nThis currency code(%s) is not supported.\nThis currency code(%s) is not supported." % (FROM, TO)
        if not ((TO not in dic) and (TO != "ALL")):
            err_message = "ERROR!\nThis currency code(%s) is not supported." % FROM
        elif not (FROM not in dic):
            err_message = "ERROR!\nThis currency code(%s) is not supported." % TO
        sys.exit(err_message)
    elif FROM == TO:
        err_message = "ERROR!\ncurcode_from and curcode_to are same."
        sys.exit(err_message)
    elif not VALUE.replace(",", "").isdigit():
        err_message = "ERROR!\n%s is invalid value." % VALUE
        sys.exit(err_message)

    if FROM == "EUR":
        print "Currency I Have: %s%s %s" % (dic[FROM], VALUE, FROM)
        VALUE = VALUE.replace(",", "")
    else:
        VALUE = VALUE.replace(",", "")
        locale.setlocale(locale.LC_MONETARY, dic[FROM])
        print "Currency I Have: %s %s" % (locale.currency(int(VALUE), True, True), FROM)

    if TO == "ALL":
        for key in dic.keys():
            if not FROM == key:
                showAmmount(FROM, key, VALUE, dic[key])
    else:
        showAmmount(FROM, TO, VALUE, dic[TO])


def showAmmount(From, To, Value, LCID):
    url = "http://rate-exchange.appspot.com/currency?from=%s&to=%s" % (From, To)
    f = urllib2.urlopen(url).read()
    jsondata = json.loads(f)
    howmuch = jsondata["rate"] * int(Value)
    print "-" * 40
    if To == "EUR":
        print To + ":", LCID + str(howmuch), "[Rate: 1 %s -> %s %s]" % (From, str(jsondata["rate"]), To)
    else:
        locale.setlocale(locale.LC_MONETARY, LCID)
        print To + ":", locale.currency(howmuch, True, True), "[Rate: 1 %s -> %s %s]" % (From, str(jsondata["rate"]), To)

#**  Arguments definition                                                    **/
#******************************************************************************/
argparser = argparse.ArgumentParser(description="Example: python curconv.py JPY USD 30,000")
argparser.add_argument("-v", "--version", action="version",
                       version="Currency Converter Written in Python v1.1 last upated:2014.11.30")
argparser.add_argument("curcode_from", metavar="currency_code_from",
                       help="currency code(src)")
argparser.add_argument("curcode_to", metavar="currency_code_to",
                       help="currency code(dst)")
argparser.add_argument("value", metavar="value",
                       help="value you want to convert from currency code(src) you selected")

#**  main                                                                    **/
#******************************************************************************/
args = argparser.parse_args()
if __name__ == "__main__":
    currencyConverter(args.curcode_from.upper(),
                      args.curcode_to.upper(),
                      args.value)
