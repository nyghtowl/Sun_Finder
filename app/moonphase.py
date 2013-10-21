#!/usr/bin/env python
"""
Moonphase  - Calculate Lunar Phase

Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
"""

import math, decimal, datetime, pytz
dec = decimal.Decimal

def position(as_of): 

   standard_date = datetime.datetime(2001, 1, 1)
   # Need to compare when both naive
   as_of_notz = as_of.replace(tzinfo=None)
   diff = as_of_notz.date() - standard_date.date()
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   return lunations % dec(1)

def phase(pos): 
   index = (pos * dec(8)) + dec("0.5")
   index = math.floor(index)
   return {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }[int(index) & 7]

def main(as_of): 
   pos = position(as_of)
   phasename = phase(pos)

   roundedpos = round(float(pos), 3)
   #print "%s" % (phasename)
   return phasename

if __name__=="__main__": 
   main()