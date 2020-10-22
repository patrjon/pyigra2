# STD-lib
# 3rd-party
import numpy as np

# Local
from pyigra2.base import IGRABase


class Observations(IGRABase):
    """Observations is a class for reading and converting IGRA2 observation files"""

    def __init__(self, filename):
        # Init parent class
        super().__init__(filename)

        # Set file specific headers and parameters
        # OBS! These index values are exactly what was given in "igra2-data-format.txt". However, python start index
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
            "NUMLEV": [33, 36],
            "P_SRC": [38, 45],
            "NP_SRC": [47, 54],
            "LAT": [56, 62],
            "LON": [64, 71],
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
            "P_SRC": ["-", "-"],
            "NP_SRC": ["-", "-"],
            "LAT": ["-", "-"],
            "LON": ["-", "-"],
        }

        # Parameter name and index
        self._parameters_name_index = {
            "LVLTYP1": [1, 1],
            "LVLTYP2": [2, 2],
            "ETIME": [4, 8],
            "PRESS": [10, 15],
            "PFLAG": [16, 16],
            "GPH": [17, 21],
            "ZFLAG": [22, 22],
            "TEMP": [23, 27],
            "TFLAG": [28, 28],
            "RH": [29, 33],
            "DPDP": [35, 39],
            "WDIR": [41, 45],
            "WSPD": [47, 51],
        }

        # Parameter units:
        # Structure: parameter_name: [raw_unit, converted_unit]
        self._parameter_units = {
            "LVLTYP1": ["-", "-"],
            "LVLTYP2": ["-", "-"],
            "ETIME": ["MMMSS", "MMMSS"],
            "PRESS": ["Pa", "Pa"],
            "PFLAG": ["-", "-"],
            "GPH": ["m", "m"],
            "ZFLAG": ["-", "-"],
            "TEMP": ["deg C * 10", "K"],
            "TFLAG": ["-", "-"],
            "RH": ["% * 10", "%"],
            "DPDP": ["deg C * 10", "K"],
            "WDIR": ["deg", "rad"],
            "WSPD": ["m/s * 10", "m/s"],
        }

    def _convert_header(self, header, date, hour):
        """Convert header

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

            # HOUR 		is the nominal or observation hour of the sounding (in UTC on
            # 		the date indicated in the YEAR/MONTH/DAY fields). Possible
            # 		valid hours are 00 through 23, and 99 = missing. Hours are
            # 		given as provided by the data provider, and the relationship
            # 		between this hour and the release time varies by data
            # 		provider, over time, and among stations.

            # RELTIME 	is the release time of the sounding in UTC. The format is
            # 		HHMM, where HH is the hour and MM is the minute. Possible
            # 		are 0000 through 2359, 0099 through 2399 when only the release
            # 		hour is available, and 9999 when both hour and minute are
            # 		missing.

            # NUMLEV 		is the number of levels in the sounding (i.e., the number of
            # 		data records that follow).
            if header_name == "NUMLEV":
                header_value = IGRABase._missing_test("", header_value)
                # New unit: -

            # P_SRC 		is the data source code for pressure levels in the sounding.
            # 		It has 25 possible values:
            #
            # 		bas-data = British Antarctic Survey READER Upper-Air Data
            # 		cdmp-amr = African Monthly Radiosonde Forms
            # 		           digitized by the U.S. Climate Data Modernization
            # 		           Program
            # 		cdmp-awc = "African Wind Component Data" digitized from
            # 		           Monthly Forms by the U.S. Climate Data
            # 		           Modernization Program
            # 		cdmp-mgr = "WMO-Coded Messages" for Malawi, digitized from
            # 		           "Computer-Generated Forms" by the U.S. Climate
            # 		           Data Modernization Program
            # 		cdmp-zdm = Zambian "Daily UA MB Ascent Sheets" digitized by
            # 		           the U.S. Climate Data Modernization Program
            # 		chuan101 = Comprehensive Historical Upper Air Network (v1.01)
            # 		erac-hud = ERA-CLIM Historical Upper Air Data
            # 		iorgc-id = IORGC/JAMSTEC-Digitized data for Indonesia
            # 		mfwa-ptu = West African Temperature-Humidity Soundings
            # 		           digitized by Meteo-France
            # 		ncar-ccd = C-Cards Radiosonde Data Set from NCAR
            # 		ncar-mit = MIT Global Upper Air Data from NCAR
            # 		ncdc6210 = NCDC Marine Upper Air Data (NCDC DSI-6210)
            # 		ncdc6301 = NCDC U.S. Rawindsonde Data (NCDC DSI-6301)
            # 		ncdc6309 = NCDC "NCAR-NMC Upper Air" (NCDC DSI-6309)
            # 		ncdc6310 = NCDC "Global U/A Cards" (NCDC DSI-6310)
            # 		ncdc6314 = Global Telecommunications System messages received
            # 		           and processed at Roshydromet and archived at NCDC
            # 		           (NCDC DSI-6314)
            # 		ncdc6315 = NCDC "People's Republic of China Data" (NCDC DSI-6315)
            # 		ncdc6316 = NCDC "Argentina National Upper Air Data" (NCDC
            # 		           DSI-6316)
            # 		ncdc6319 = NCDC "Korea National Upper Air Data" (NCDC DSI-6319)
            # 		ncdc6322 = Global Telecommunications System messages received
            # 		           at the Australian Bureau of Meteorology and
            # 		           archived at NCDC (NCDC DSI-6322)
            # 		ncdc6323 = NCDC "Australian U/A Thermo/Winds Merged" (NCDC
            # 		           DSI-6323)
            # 		ncdc6324 = NCDC "Brazil National Upper Air Data" (NCDC DSI-6324)
            # 		ncdc6326 = NCDC "Global Upper Air Cards" (NCDC DSI-6326)
            # 		ncdc6355 = Russian Ice Island upper air data  processed by
            # 		           NCAR and archived at NCDC
            # 		ncdc-gts = Global Telecommunications System (GTS) messages
            # 		           received at NCDC from the National Centers for
            # 		           Environmental Prediction
            # 		ncdc-nws =  U.S. National Weather Service upper air data
            # 		            received at NCDC in real-time
            # 		ngdc-har = Historical Arctic radiosonde archive from the
            # 		           National Geophysical Data Center
            # 		usaf-ds3 = U.S. Air Force 14th Weather Squadron Upper Air
            # 		           Data Set ( received in DS3 format)

            # NP_SRC 		is the data source code for non-pressure levels in the
            # 		sounding. These include levels whose vertical coordinate
            # 		is only identified by height as well as surface levels without
            # 		either pressure or height.
            # 		NP_SRC has 15 possible values:
            #
            # 		cdmp-adp = "African Daily Pilot Balloon Ascent Sheets" digitized
            # 		           by the U.S. Climate Data Modernization Program
            # 		cdmp-awc = "African Wind Component Data" digitized from
            # 		           "Monthly Forms" by the U.S. Climate Data
            # 		           Modernization Program
            # 		cdmp-us2 = "U.S. Winds Aloft digitized from "Daily Computation
            # 		           Sheets" by the U.S. Climate Data Modernization
            # 		           Program
            # 		cdmp-us3 = "U.S. Winds Aloft" digitized from "Military Daily
            # 		           Computation Sheets" by the U.S. Climate Data
            # 		           Modernization Program
            # 		cdmp-usm = U.S. pilot balloon observations digitized from
            # 		           "Monthly Forms" by the U.S. Climate Data
            # 		           Modernization Program
            # 		chuan101 = Comprehensive Historical Upper Air Network (v1.01)
            # 		erac-hud = ERA-CLIM Historical Upper Air Data
            # 		mfwa-wnd = West African Winds Aloft digitized by Meteo-France
            # 		ncdc6301 = NCDC U.S. Rawindsonde Data (NCDC DSI-6301)
            # 		ncdc6309 = NCDC "NCAR-NMC Upper Air" (NCDC DSI-6309)
            # 		ncdc6314 = Global Telecommunications System messages received
            # 		           and processed at Roshydromet and archived at NCDC
            # 		           (NCDC DSI-6314)
            # 		ncdc-gts = Global Telecommunications System (GTS) messages
            # 		           received at NCDC from the National Centers for
            # 		           Environmental Prediction
            # 		ncdc-nws =  U.S. National Weather Service upper air data
            # 		            received at NCDC in real-time
            # 		ngdc-har = Historical Arctic radiosonde archive from the
            # 		           National Geophysical Data Center
            # 		usaf-ds3 = U.S. Air Force 14th Weather Squadron Upper Air
            # 		           Data Set (received in DS3 format)

            # LAT 		is the Latitude at which the sounding was taken. For mobile
            # 		stations, it is the latitude at the time of observation.
            # 		For fixed stations, it is the same as the latitude shown
            # 		in the IGRA station list regardless of the date of the
            # 		sounding since no attempt was made to reconstruct the
            # 		sounding-by-sounding location history of these stations.
            if header_name == "LAT":
                header_value = IGRABase._missing_test("", header_value)
                # New unit: -

            # LON 		is the longitude at which the sounding was taken. For mobile
            # 		stations, it is the longitude at the time of observation.
            # 		For fixed stations, it is the same as the longitude shown
            # 		in the IGRA station list regardless of the date of the
            # 		sounding since no attempt was made to reconstruct the
            # 		sounding-by-sounding location history of these stations.
            if header_name == "LON":
                header_value = IGRABase._missing_test("", header_value)
                # New unit: -

            # Add to new header
            self.converted_data[date][hour]["header"][header_name] = header_value

    def _convert_parameters(self, parameters, date, hour):
        """Convert data

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

            # These variables have the following definitions:

            # LVLTYP1 	is the major level type indicator. It has the following
            # 		three possible values:
            #
            # 		1 = Standard pressure level (for levels at 1000, 925, 850,
            # 		    700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30,
            # 		    20, 10, 7, 5, 3, 2, and 1 hPa)
            # 		2 = Other pressure level
            # 		3 = Non-pressure level
            if param_name == "LVLTYP1":
                # Convert to int
                array = array.astype(np.int)

            # LVLTYP2 	is the minor level type indicator. It has the following
            # 		three possible values:
            #
            # 		1 = Surface
            # 		2 = Tropopause
            # 		0 = Other
            if param_name == "LVLTYP2":
                # Convert to int
                array = array.astype(np.int)

            # ETIME		is the elapsed time since launch. The format is MMMSS, where
            # 		MMM represents minutes and SS represents seconds, though
            # 		values are not left-padded with zeros. The following special
            # 		values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "ETIME":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

                # @TODO: Convert to seconds instead of MMMSS

            # PRESS 		is the reported pressure (Pa or mb * 100, e.g.,
            # 		100000 = 1000 hPa or 1000 mb). -9999 = missing.
            if param_name == "PRESS":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Fix missing values, set to nans
                array[array == -9999] = np.nan

            # PFLAG 		is the pressure processing flag indicating what level of
            # 		climatology-based quality assurance checks were applied. It
            # 		has three possible values:
            #
            # 		blank = Not checked by any climatology checks. If data value
            # 		        not equal to -9999, it passed all other applicable
            # 		        checks.
            # 		A     = Value falls within "tier-1" climatological limits
            # 		        based on all days of the year and all times of day
            # 		        at the station, but not checked by
            # 		        "tier-2" climatology checks due to
            # 		        insufficient data.
            # 		B     = Value passes checks based on both the tier-1
            # 		        climatology and a "tier-2" climatology specific to
            # 		        the time of year and time of day of the data value.

            # GPH 		is the reported geopotential height (meters above sea level).
            # 		This value is often not available at variable-pressure levels.
            # 		The following special values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "GPH":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

            # ZFLAG 		is the  geopotential height processing flag indicating what
            # 		level of climatology-based quality assurance checks were
            # 		applied. It has three possible values:
            #
            # 		blank = Not checked by any climatology checks or flag not
            # 		        applicable. If data value not equal to -8888 or -9999,
            # 		        it passed all other applicable checks.
            # 		A     = Value falls within "tier-1" climatological limits
            # 		        based on all days of the year and all times of day
            # 		        at the station, but not checked by
            # 		        "tier-2" climatology checks due to insufficient data.
            # 		B     = Value passes checks based on both the tier-1
            # 		        climatology and a "tier-2" climatology specific to
            # 		        the time of year and time of day of the data value.

            # TEMP 		is the reported temperature (degrees C to tenths, e.g.,
            # 		11 = 1.1�C). The following special values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "TEMP":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

                # Convert to deg, not tenths
                array = array / 10.0

                # Convert to Kelvin (SI-unit)
                array = array + 273.15

            # TFLAG 		is the temperature processing flag indicating what
            # 		level of climatology-based quality assurance checks were
            # 		applied. It has three possible values:
            #
            # 		blank = Not checked by any climatology checks or flag not
            # 		        applicable. If data value not equal to -8888 or -9999,
            # 		        it passed all other applicable checks.
            # 		A     = Value falls within "tier-1" climatological limits
            # 		        based on all days of the year and all times of day
            # 		        at the station, but not checked by "tier-2"
            # 		        climatology checks due to insufficient data.
            # 		B     = Value passes checks based on both the tier-1
            # 		        climatology and a "tier-2" climatology specific to
            # 		        the time of year and time of day of the data value.

            # RH 		is the reported relative humidity (Percent to tenths, e.g.,
            # 		11 = 1.1%). The following special values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "RH":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

                # Convert to Percent, not tenths
                array = array / 10.0

            # DPDP 		is the reported dewpoint depression (degrees C to tenths, e.g.,
            # 		11 = 1.1�C). The following special values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "DPDP":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

                # Convert to deg, not tenths
                array = array / 10.0

                # Convert to Kelvin (SI-unit)
                array = array + 273.15

            # WDIR 		is the reported wind direction (degrees from north,
            # 		90 = east). The following special values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "WDIR":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

                # Convert to radians
                array = array * (np.pi / 180.0)

            # WSPD 		is the reported wind speed (meters per second to tenths, e.g.,
            # 		11 = 1.1 m/s). The following special values are used:
            #
            # 		-8888 = Value removed by IGRA quality assurance, but valid
            # 		        data remain at the same level.
            # 		-9999 = Value missing prior to quality assurance.
            if param_name == "WSPD":
                # Convert to float due to nans
                array = array.astype(np.float)

                # Quality assurance fixes, set to np.nan
                array[array == -9999] = np.nan
                array[array == -8888] = np.nan

                # Convert to m/s, not tenths
                array = array / 10.0

            # Add data to converted data
            self.converted_data[date][hour]["parameters"][param_name] = array
