# STD-lib
import pathlib

# 3rd-party
import numpy as np

# Local


class IGRABase:
    def __init__(self, filename):
        """Init method

        IGRA.raw_data structure:

        * YYYY-MM-DD (date)
            * HOUR
                * header = {header1: value1, header2: value2, ..., headerN: valueN}
                * parameters = {parameter1: [value1, value2, ...], parameter2: [value1, value2, ...], ...}
            * HOUR_X (If multiple equal hour, add counter X)

        :param filename: /path/to/extracted file, i.e. .txt file
        :type filename: str
        """
        self.filename = pathlib.Path(filename)
        self.raw_data = {}
        self.converted_data = {}

        # Internal params:
        self._header_name_index = {}
        self._header_units = {}
        self._parameters_name_index = {}
        self._parameter_units = {}

        # Duplicate hour counter
        self._dublicate_hour_counter = 0

        # Skip adding data during first loop:
        self._add_data_bool = False

        # The following variables are reset with _reset_header_parameters()
        self._header = {}
        self._parameters = {}

    def read(self):
        """Reads the file and stores the data in self.raw_data

        :return: None
        """
        # Run read if and only if header and parameter names and indies are non-empty
        if self._header_name_index and self._parameters_name_index:

            # Check if file exists:
            if not self.filename.exists():
                raise FileNotFoundError(f"File {self.filename.as_posix()} not found.")

            # Open and read the file
            with open(self.filename, "r") as f:
                lines = f.readlines()

            # Reset header and parameters:
            self._reset_header_parameters()

            # Loop through all lines in lines
            for line in lines:
                # Lines starting with # are headers
                if line[0] == "#":
                    # Add data to self.raw_data?
                    if self._add_data_bool:
                        self._add_data()

                    # Set _add_data_bool to true to save for all loop exclude the first
                    self._add_data_bool = True

                    # Set _header:
                    self._set_header(line)

                else:
                    # Set _parameters:
                    self._set_parameters(line)

            # Add last instance of data:
            self._add_data()

    def convert_to_numpy(self):
        """Convert raw_data to correct types and SI-units.

        :return: None
        """
        for date, hours in self.raw_data.items():

            if date not in self.converted_data:
                self.converted_data[date] = {}

            for hour, head_param in hours.items():
                if hour not in self.converted_data[date]:
                    self.converted_data[date][hour] = {}

                # Convert headers
                self._convert_header(head_param["header"], date, hour)

                # Convert parameters
                self._convert_parameters(head_param["parameters"], date, hour)

    def print(self, date, hour, source="converted"):
        """Print date and hour to screen based on converted data

        :param date: date to print
        :param hour: hour to print
        :return: None
        """
        if source == "converted":
            data = self.converted_data
            unit_index = 1
        elif source == "raw":
            data = self.raw_data
            unit_index = 0
        else:
            raise ValueError(
                f"The source variable should equal to 'converted or 'raw', got {source}' "
            )

        if date not in data:
            raise KeyError(f"Date {date} not in data.")

        if hour not in data[date]:
            raise KeyError(f"Hour {hour} not found for date {date} in data.")

        # Helpers
        params = data[date][hour]["parameters"]
        header = data[date][hour]["header"]

        # Print title
        print(150 * "-")
        print(
            f"Station: {header['ID']}\n"
            f"Date: {header['YEAR']}-{header['MONTH']}-{header['DAY']}\n"
            f"Hour: {header['HOUR']}\n"
            f"Data type: {source}\n"
        )

        # Print data:
        width_add = 7
        width_all = 0
        width_vertical = 20

        # Print headers:
        print(f"Header information:")
        for name, value in header.items():
            if name == "HEADREC":
                continue
            name_unit = f"{name} [{self._header_units[name][unit_index]}]"
            print(f"{name_unit.rjust(width_vertical)}: {value}")

        # Print parameter units
        print(f"\nParameters and units:")
        for name, value in self._parameter_units.items():
            print(f"{name.rjust(width_vertical)}: [{value[unit_index]}]")
        print("\n", end="")

        # Print parameter names:
        for param_name in params.keys():
            width = len(param_name) + width_add
            print(param_name.rjust(width), end="")
            width_all += width
        print("\n" + (width_all + width_add) * "-")

        # Print parameter data
        num_data_points = len(params[list(params.keys())[0]])
        for idx in range(num_data_points):
            for param_name, value in params.items():
                width = len(param_name) + width_add
                item = value[idx]
                if isinstance(item, np.float):
                    item = f"{item:.2f}"
                else:
                    item = f"{item}"
                print(item.rjust(width), end="")
            print("\n", end="")

        print((width_all + width_add) * "_")

    def _add_data(self):
        """Add collected data to self.raw_data

        :return: None
        """
        # Get date
        date = (
            f"{self._header['YEAR']}-"
            f"{self._header['MONTH']}-"
            f"{self._header['DAY']}"
        )

        # Add date to data. This should happen only ones
        if date not in self.raw_data:
            self.raw_data[date] = {}
            # Reset duplicate_hour_counter here!
            # Rationale: if we reset it here we will have one counter / date. Which is desired!
            self._dublicate_hour_counter = 0

        # Get the hour (hour=99 => hour info missing)
        hour = self._header["HOUR"]
        if hour == "99":
            hour = f"{hour}_{self._dublicate_hour_counter}"
            self._dublicate_hour_counter += 1

        # Add _header and _parameters to date and hour in data
        self.raw_data[date][hour] = {
            "header": self._header,
            "parameters": self._parameters,
        }

        # Reset headers and parameters
        self._reset_header_parameters()

    def _reset_header_parameters(self):
        """Reset the internal parameters for the next sounding.

        Resets the following parameters:
        * _header - empty dictionary
        * _parameters - dictionary with keys as keys in self._parameters_name_index and
            empty lists as values.

        :return: None
        """
        self._header = {}
        self._parameters = {key: [] for key in list(self._parameters_name_index.keys())}

    def _set_header(self, line):
        """Collects data from header line.

        :param line: line from file
        :type line: str
        :return: None
        """
        # Set _header
        # We subtract the first index with one due to python indexing start from zero.
        for header_name, index in self._header_name_index.items():
            self._header[header_name] = line[index[0] - 1 : index[1]]

    def _set_parameters(self, line):
        """Collects data from data line.

        :param line: line from file
        :type line: str
        :return: None
        """
        # Set _values.
        # We subtract the first index with one due to python indexing start from zero.
        for parameter_name, index in self._parameters_name_index.items():
            self._parameters[parameter_name].append(line[index[0] - 1 : index[1]])

    def _convert_header(self, header):
        """Convert header

        :param header: header to convert
        :return: None
        """
        # This method is implemented in child classes
        pass

    def _convert_parameters(self, parameters):
        """Convert data

        :param parameters: parameters to convert
        :return: None
        """
        # This method is implemented in child classes
        pass

    @staticmethod
    def _missing_test(missing_value, value):
        """Test if value is "missing_value", if not convert to float.

        :param missing_value: the missing value indicator, e.g. -99999
        :param value: the value to be checked and converted
        :return: the checked value as float (np.nan = missing)
        """
        # Missing values:
        if value == missing_value:
            value = np.nan
        else:
            value = float(value)
        return value
