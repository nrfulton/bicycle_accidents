"""
Copyright Nathan Fulton 2018
"""
import csv
from NathanGeoUtils import NathanGeoUtils

utils = NathanGeoUtils()

crashes = csv.DictReader(open("crashes.csv"))

deaths = []
injuries = []
bicycle_somehow = [] # "bicycle somehow involved"
questionable_data = 0
for crash in crashes:
  # Bycicle data. Note: deaths are sometimes but not always double-entered as serious
  # injuries, so we'll subtract deaths from injuries and ensure that the total
  # count is correct.
  bicycle_death          = int(crash.get("BICYCLE_DEATH_COUNT"))
  bicycle_serious_injury = max(0, int(crash.get("BICYCLE_MAJ_INJ_COUNT")) - bicycle_death)
  bicycle_count          = int(crash.get("BICYCLE_COUNT"))

  # If we are going to include this data in the dataset, do some sanity checks
  # on it.
  if bicycle_death > 0 or bicycle_serious_injury > 0 or bicycle_count > 0:
    # Some cases worth paying attention to, either because they're exception or
    # because they might indicate missing data:
    if bicycle_count != bicycle_death + bicycle_serious_injury: 
      #print("bicycle_count != bicycle_death + bicycle_serious_injury (%d != %d + %d)" % (bicycle_count, bicycle_death, bicycle_serious_injury))
      questionable_data += 1
    if(bicycle_count > 1):
      print("Multiple cyclists involved (%d) (no problem w/ data but worth investigating further)" % bicycle_count)
      print(crash)

  # Grab the location of the death/injury.
  if crash.get("LATITUDE") != '' and crash.get("LATITUDE") != '':
    latlon = utils.pgh_dms_to_degrees(crash.get("LATITUDE"), crash.get("LONGITUDE"))
  
  if bicycle_death > 0:
    deaths.append(latlon)
  elif bicycle_serious_injury > 0:
    injuries.append(latlon)
  elif bicycle_count > 0:
    bicycle_somehow.append(latlon)

print("DEATH LOCATIONS")
print("---------------")
for death in deaths:
  print(death)

print("INJURY LOCATIONS")
print("----------------")
for injury in injuries:
  print(injury)

print("CYCLIST INVOLVED")
print("----------------")
for bs in bicycle_somehow:
  print(bs)


print("total accidents resulting in death of at least one cyclist: %s" % len(deaths))
print("total accidents resulting in serious injury of at least one cyclist: %s" % len(injuries))
print("total 'other' accidents that need further analysis: %s" % len(bicycle_somehow))
print("Quesationable data points remaining: %d" % questionable_data)
