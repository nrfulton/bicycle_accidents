#40 25:05.948 lat 79 56:52.507 long
import re

class NathanGeoUtils:
  __DEBUG = False

  def pgh_dms_to_degrees(self, lat_dms_str, lon_dms_str):
    """ Converts something like '40 25:05.948' to decimal degrees. Automatically makes longitude negative if not already. that's what makes this pgh-specific... Based loosely on something from SO. @todo find relevant link. """
    lat_dms = self._parse_dms(lat_dms_str)
    lon_dms = self._parse_dms(lon_dms_str)
    if(lat_dms is None or lon_dms is None):
      return None
    else:
      lat = self._dms2dd(lat_dms, False)
      lon = self._dms2dd(lon_dms, True)
      return (lat, lon)

  def _dms2dd(self, dms, negate):
    """ for use with pgh_dms_to_degrees only """
    degrees, minutes, seconds = dms 
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if negate and dd > 0:
      dd = -1*dd
    return dd

  def _parse_dms(self, dms):
    """ for use with pgh_dms_to_degrees only """
    pattern = re.compile("(\d\d)\ (\d\d?):(\d\d?\.?\d?\d?\d?)")
    result  = pattern.match(dms)
    if(result is not None):
      assert len(result.groups()) == 3, "Expected 3 results but found %s" % result.groups()
      return (result.group(1), result.group(2), result.group(3))
    else:
      if(self.__DEBUG): print("NathanGeoUtils._parse_dms: Expected NN NN:NN.NNN? but found: .%s." % dms)
      return None
    
