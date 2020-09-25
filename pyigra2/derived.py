# STD-lib
# 3rd-party
import numpy as np

# Local
from pyigra2.base import IGRABase


class Derived(IGRABase):
    def __init__(self, filename):
        # Init parent class
        super().__init__(filename)

        # Set file specific headers and parameters
        # OBS! These index values are exactly what was given in "igra2-derived-format.txt". However, python start index
        # with zero. This is taken care of in parent class IGRABase._set_header() and IGRABase._set_parameters.

        # Header name and index
        self._header_name_index = {
            "HEADREC": [1, 1],
            "ID": [2, 12],
            "YEAR": [14, 17],
            "MONTH": [19, 20],
            "DAY": [22, 23],
            "HOUR": [25, 26],
            "RELTIME": [28, 31],
            "NUMLEV": [32, 36],
            "PW": [38, 43],
            "INVPRESS": [44, 49],
            "INVHGT": [50, 55],
            "INVTEMPDIF": [56, 61],
            "MIXPRESS": [62, 67],
            "MIXHGT": [68, 73],
            "FRZPRESS": [74, 79],
            "FRZHGT": [80, 85],
            "LCLPRESS": [86, 91],
            "LCLHGT": [92, 97],
            "LFCPRESS": [98, 103],
            "LFCHGT": [104, 109],
            "LNBPRESS": [110, 115],
            "LNBHGT": [116, 121],
            "LI": [122, 127],
            "SI": [128, 133],
            "KI": [134, 139],
            "TTI": [140, 145],
            "CAPE": [146, 151],
            "CIN": [152, 157],
        }

        # Header units:
        # Structure: header_name: [raw_unit, converted_unit]
        self._header_units = {
            "HEADREC": ["-", "-"],
            "ID": ["-", "-"],
            "YEAR": ["yyyy", "yyyy"],
            "MONTH": ["mm", "mm"],
            "DAY": ["dd", "dd"],
            "HOUR": ["HH", "HH"],
            "RELTIME": ["HHMM", "HHMM"],
            "NUMLEV": ["-", "-"],
            "PW": ["mm*100", "mm"],
            "INVPRESS": ["Pa", "Pa"],
            "INVHGT": ["m", "m"],
            "INVTEMPDIF": ["K*10", "K"],
            "MIXPRESS": ["Pa", "Pa"],
            "MIXHGT": ["m", "m"],
            "FRZPRESS": ["Pa", "Pa"],
            "FRZHGT": ["m", "m"],
            "LCLPRESS": ["Pa", "Pa"],
            "LCLHGT": ["m", "m"],
            "LFCPRESS": ["Pa", "Pa"],
            "LFCHGT": ["m", "m"],
            "LNBPRESS": ["Pa", "Pa"],
            "LNBHGT": ["m", "m"],
            "LI": ["deg C", "K"],
            "SI": ["deg C", "K"],
            "KI": ["deg C", "K"],
            "TTI": ["deg C", "K"],
            "CAPE": ["J/kg", "J/kg"],
            "CIN": ["J/kg", "J/kg"],
        }

        # Parameter name and index
        self._parameters_name_index = {
            "PRESS": [1, 7],
            "REPGPH": [9, 15],
            "CALCGPH": [17, 23],
            "TEMP": [25, 31],
            "TEMPGRAD": [33, 39],
            "PTEMP": [41, 47],
            "PTEMPGRAD": [49, 55],
            "VTEMP": [57, 63],
            "VPTEMP": [65, 71],
            "VAPPRESS": [73, 79],
            "SATVAP": [81, 87],
            "REPRH": [89, 95],
            "CALCRH": [97, 103],
            "RHGRAD": [105, 111],
            "UWND": [113, 119],
            "UWDGRAD": [121, 127],
            "VWND": [129, 135],
            "VWNDGRAD": [137, 143],
            "N": [145, 151],
        }

        # Parameter units:
        # Structure: parameter_name: [raw unit, converted unit]
        self._parameter_units = {
            "PRESS": ["Pa", "Pa"],
            "REPGPH": ["m", "m"],
            "CALCGPH": ["m", "m"],
            "TEMP": ["K * 10", "K"],
            "TEMPGRAD": ["(K/km) * 10", "K/m"],
            "PTEMP": ["K * 10", "K"],
            "PTEMPGRAD": ["(K/km) * 10", "K/m"],
            "VTEMP": ["K * 10", "K"],
            "VPTEMP": ["K * 10", "K"],
            "VAPPRESS": ["mb * 1000", "Pa"],
            "SATVAP": ["mb * 1000", "Pa"],
            "REPRH": ["% * 10", "%"],
            "CALCRH": ["% * 10", "%"],
            "RHGRAD": ["(%/km) * 10", "%/m"],
            "UWND": ["(m/s) * 10", "m/s"],
            "UWDGRAD": ["(m/s per km) * 10", "(m/s) / m"],
            "VWND": ["(m/s) * 10", "m/s"],
            "VWNDGRAD": ["(m/s per km) * 10", "(m/s) / m"],
            "N": ["-", "-"],
        }

    def _convert_header(self, header, date, hour):
        """ Convert header

        :param header: header to convert
        :param date, date to update
        :param hour: hour to update
        :return: None
        """
        # Create target dict
        self.converted_data[date][hour]["header"] = {}

        # Remove whitespaces:
        for header_name, header_value in header.items():
            # Remove white space
            header_value = header_value.replace(" ", "")

            # These variables have the following definitions:

            # HEADREC		is the header record indicator (always set to "#").

            # ID		is the station identification code. See "igra2-stations.txt"
            # 		for a complete list of stations and their names and locations.

            # YEAR 		is the year of the sounding.

            # MONTH 		is the month of the sounding.

            # DAY 		is the day of the sounding.

            # HOUR 		is the hour of the sounding (99 = missing).

            # RELTIME 	is the release time of the sounding (format HHMM, missing=9999).

            # NUMLEV 		is the number of levels in the sounding (i.e., the number of
            # 		data records that follow).
            if header_name == "NUMLEV":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: -

            # PW 		is the precipitable water (mm*100) between the surface and 500 hPa.
            if header_name == "PW":
                header_value = IGRABase._missing_test("-99999", header_value)
                header_value = header_value / 100.0
                # New unit: mm

            # INVPRESS 	is the pressure (in Pa or mb*100) at the level of the
            # 		warmest temperature in the sounding. Only provided if
            # 		the warmest temperature is above the surface.
            if header_name == "INVPRESS":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: Pa

            # INVHGT 		is the height (in meters above the surface) of the warmest
            # 		temperature in the sounding. Only provided when the
            # 		warmest temperature is above the surface.
            if header_name == "INVHGT":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: m

            # INVTEMPDIF 	is the difference between the warmest temperature in the
            # 		sounding and the surface temperature (K * 10). Only provided if
            # 		the warmest temperature is above the surface.
            if header_name == "INVTEMPDIF":
                header_value = IGRABase._missing_test("-99999", header_value)
                header_value = header_value / 10.0
                # New unit: K

            # MIXPRESS 	is the pressure (in Pa or mb * 100) at the top of the
            # 		mixed layer as determined using the parcel method.
            if header_name == "MIXPRESS":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: Pa

            # MIXHGT 		is the height (in meters above the surface) of the top of the
            # 		mixed layer As determined using the parcel method.
            if header_name == "MIXHGT":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: m

            # FRZPRESS 	is the pressure (in Pa or mb * 100) where the temperature
            # 		first reaches the freezing point when moving upward from
            # 		the surface. Determined by interpolating linearly with respect
            # 		to the logarithm of pressure between adjacent reported levels.
            # 		Not provided if the surface temperature is below freezing.
            if header_name == "FRZPRESS":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: Pa

            # FRZHGT 		is the height (in meters above the surface) where the temperature
            # 		first reaches the freezing point when moving upward from the
            # 		surface. Determined analogously to FRZPRESS. Not provided if the
            # 		surface temperature is below freezing.
            if header_name == "FRZHGT":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: m

            # LCLPRESS 	is the pressure (in Pa or mb * 100) of the lifting condensation
            # 		level.
            if header_name == "LCLPRESS":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: Pa

            # LCLHGT 		is the height (in meters above the surface) of the lifting
            # 		condensation level.
            if header_name == "LCLHGT":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: m

            # LFCPRESS 	is the pressure (in Pa or mb * 100) of the level of free convection.
            if header_name == "LFCPRESS":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: Pa

            # LFCHGT 		is the height (in meters above the surface) of the level of free
            # 		convection.
            if header_name == "LFCHGT":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: m

            # LNBPRESS 	is the pressure (in Pa or mb * 100) of the level of
            # 		neutral buoyancy (or equilibrium level).
            if header_name == "LNBPRESS":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: Pa

            # LNBHGT 		is the height (in meters above the surface) of the level of
            # 		neutral buoyancy (or equilibrium level).
            if header_name == "LNBHGT":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: m

            # LI 		is the lifted index (in degrees C).
            if header_name == "LI":
                header_value = IGRABase._missing_test("-99999", header_value)
                header_value = header_value + 273.15
                # New unit: K

            # SI 		is the Showalter index (in degrees C).
            if header_name == "SI":
                header_value = IGRABase._missing_test("-99999", header_value)
                header_value = header_value + 273.15
                # New unit: K

            # KI 		is the K index (in degrees C).
            if header_name == "KI":
                header_value = IGRABase._missing_test("-99999", header_value)
                header_value = header_value + 273.15
                # New unit: K

            # TTI 		is the total totals index (in degrees C).
            if header_name == "TTI":
                header_value = IGRABase._missing_test("-99999", header_value)
                header_value = header_value + 273.15
                # New unit: K

            # CAPE 		is the convective available potential energy (in J/kg).
            if header_name == "CAPE":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: J/kg

            # CIN 		is the convective inhibition (in J/kg).
            if header_name == "CIN":
                header_value = IGRABase._missing_test("-99999", header_value)
                # New unit: J/kg

            # Add to new header
            self.converted_data[date][hour]["header"][header_name] = header_value

    def _convert_parameters(self, parameters, date, hour):
        """ Convert data

        :param parameters: parameters to convert
        :param date, date to update
        :param hour: hour to update
        :return: None
        """
        # Create target dict
        self.converted_data[date][hour]["parameters"] = {}

        for param_name, value_lst in parameters.items():
            # For every parameter do:

            # Convert to numpy array with dtype str
            array = np.array(value_lst, dtype=np.str)

            # Remove white spaces
            array = np.char.replace(array, " ", "")

            # Convert to float due to nans
            array = array.astype(np.float)

            # Missing values: -99999
            array[array == -99999] = np.nan

            # Convert specific parameters:
            # PRESS 		is the reported pressure (Pa or mb * 100).

            # REPGPH 		is the reported geopotential height (meters). This value is
            # 		often not available at significant levels.

            # CALCGPH 	is the calculated geopotential height (meters). The geopotential
            # 		height has been estimated by applying the hydrostatic balance to
            # 		the atmospheric layer between the next lower level with a
            # 		reported geopotential height and the current level.

            # TEMP 		is the reported temperature (K * 10).
            if param_name == "TEMP":
                array = array / 10.0
                # New unit: K

            # TEMPGRAD 	is the temperature gradient between the current level and
            # 		the next higher level with a temperature [(K/km) * 10, positive
            # 		if temperature increases with height].
            if param_name == "TEMPGRAD":
                array = array / 10000.0
                # New unit: K/m

            # PTEMP 		is the potential temperature (K * 10).
            if param_name == "PTEMP":
                array = array / 10.0
                # New unit: K

            # PTEMPGRAD 	is the potential temperature gradient between the current level
            # 		and the next higher level with a potential temperature
            # 		[(K/km) * 10, positive if potential temperature increases
            # 		with height].
            if param_name == "PTEMPGRAD":
                array = array / 10000.0
                # New unit: K/m

            # VTEMP 		is the virtual temperature (K * 10).
            if param_name == "VTEMP":
                array = array / 10.0
                # New unit: K

            # VPTEMP 		is the virtual potential temperature (K * 10).
            if param_name == "VPTEMP":
                array = array / 10.0
                # New unit: K

            # VAPPRESS 	is the vapor pressure (mb * 1000) as computed from temperature,
            # 		pressure, and dewpoint depression at the same level.
            if param_name == "VAPPRESS":
                array = array / 10.0
                # New unit: Pa

            # SATVAP 		is the saturation vapor pressure (mb * 1000) as computed from
            # 		pressure and temperature at the same level.
            if param_name == "SATVAP":
                array = array / 10.0
                # New unit: Pa

            # REPRH 		is the relative humidity (Percent * 10) as reported in the
            # 		original sounding.
            if param_name == "REPRH":
                array = array / 10.0
                # New unit: %

            # CALCRH		is the relative humidity (Percent * 10) as calculated from vapor
            # 		pressure, saturation vapor pressure, and pressure at the same
            # 		level.
            if param_name == "CALCRH":
                array = array / 10.0
                # New unit: %

            # RHGRAD 		is the relative humidity gradient between the current level and
            # 		the next higher usable level [(%/km) * 10, positive if relative
            # 		humidity increases with height].
            if param_name == "RHGRAD":
                array = array / 10000.0
                # New unit: %/m

            # UWND 		is the zonal wind component [(m/s) * 10] as computed from the
            # 		reported wind speed and direction.
            if param_name == "UWND":
                array = array / 10.0
                # New unit: m/s

            # UWDGRAD 	is the vertical gradient of the zonal wind between the current
            # 		level and the next higher level with a wind observation
            # 		[(m/s per km) * 10, positive if zonal wind becomes more
            # 		positive with height].
            if param_name == "UWDGRAD":
                array = array / 10000.0
                # New unit: (m/s) / m

            # VWND 		is the meridional wind component [(m/s) * 10] as computed
            # 		from the reported wind speed and direction.
            if param_name == "VWND":
                array = array / 10.0
                # New unit: m/s

            # VWNDGRAD 	is the vertical gradient of the meridional wind component
            # 		between the current level and the next higher level with a wind
            # 		observation [(m/s per km) * 10, positive if the meridional
            # 		wind becomes more positive with height].
            if param_name == "VWNDGRAD":
                array = array / 10000.0
                # New unit: (m/s) / m

            # N 		is the refractive index (unitless).

            # Add data to converted data
            self.converted_data[date][hour]["parameters"][param_name] = array
