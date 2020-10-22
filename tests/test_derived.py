import pathlib
import pytest
from pyigra2.derived import Derived


@pytest.fixture(scope="module")
def der(info):
    """Create a fresh instance of Derived"""
    # Setup
    der = Derived(info.der_singel.path)
    yield der
    # Teardown


@pytest.fixture(scope="module")
def der_read(info):
    """Create a fresh instance of Derived"""
    # Setup
    der = Derived(info.der_singel.path)
    der.read()
    yield der
    # Teardown


@pytest.fixture(scope="module")
def der_read_convert(info):
    """Create a fresh instance of Derived"""
    # Setup
    der = Derived(info.der_singel.path)
    der.read()
    der.convert_to_numpy()
    yield der
    # Teardown


@pytest.fixture(scope="module")
def der_multi(info):
    """Create a fresh instance of Derived"""
    # Setup
    der = Derived(info.der_multi.path)
    yield der
    # Teardown


@pytest.fixture(scope="module")
def der_read_multi(info):
    """Create a fresh instance of Derived"""
    # Setup
    der = Derived(info.der_multi.path)
    der.read()
    yield der
    # Teardown


@pytest.fixture(scope="module")
def der_read_convert_multi(info):
    """Create a fresh instance of Derived"""
    # Setup
    der = Derived(info.der_multi.path)
    der.read()
    der.convert_to_numpy()
    yield der
    # Teardown


def test_header_names(der, derived_content):
    """Test that all header names is in the object"""
    expected_header_names = derived_content["expected_header_names"]

    # Object names
    names_header_name_index = tuple(der._header_name_index.keys())
    names_header_units = tuple(der._header_units.keys())

    # Length
    assert len(names_header_name_index) == len(expected_header_names)
    assert len(names_header_units) == len(expected_header_names)

    for name in expected_header_names:
        assert name in names_header_name_index
        assert name in names_header_units


def test_parameter_names(der, derived_content):
    """Test that all header names is in the object"""
    expected_parameter_names = derived_content["expected_parameter_names"]

    # Object names
    names_parameters_name_index = tuple(der._parameters_name_index.keys())
    names_parameter_units = tuple(der._parameter_units.keys())

    # Length
    assert len(names_parameters_name_index) == len(expected_parameter_names)
    assert len(names_parameter_units) == len(expected_parameter_names)

    for name in expected_parameter_names:
        assert name in names_parameters_name_index
        assert name in names_parameter_units


def test_read_state(der_read, derived_content):
    """Test read and check the state of the object"""
    # Check state
    assert isinstance(der_read.filename, pathlib.PurePath)
    assert der_read.raw_data
    assert der_read.converted_data == {}
    assert der_read._header_name_index
    assert der_read._header_units
    assert der_read._parameters_name_index
    assert der_read._parameter_units
    assert der_read._dublicate_hour_counter == 0
    assert der_read._add_data_bool

    # During read, _reset_header_parameters is called which resets header parameters
    assert der_read._header == {}

    # _parameters should be a dict keys="parameter names" and value="empty list"
    assert isinstance(der_read._parameters, dict)
    assert len(der_read._parameters) == len(derived_content["expected_parameter_names"])
    for value in der_read._parameters.values():
        assert not value
        assert isinstance(value, list)


##########
def test_read_file_not_found():
    """Test if file is not found"""
    der = Derived("FileNotFound.txt")

    with pytest.raises(FileNotFoundError):
        der.read()


def test_raw_data_structure(der_read, info, derived_content):
    """Check the structure and content av .raw_data"""

    # Check dates and hours:
    for date in info.der_singel.dates:
        assert date in der_read.raw_data
        for hour in info.der_singel.hours:
            assert hour in der_read.raw_data[date]

            # Structure of header
            assert "header" in der_read.raw_data[date][hour]
            assert len(der_read.raw_data[date][hour]["header"]) == len(
                derived_content["expected_header_names"]
            )

            for header in der_read.raw_data[date][hour]["header"]:
                assert header in derived_content["expected_header_names"]

            # Structure of parameters
            assert "parameters" in der_read.raw_data[date][hour]
            assert len(der_read.raw_data[date][hour]["parameters"]) == len(
                derived_content["expected_parameter_names"]
            )

            for parameter in der_read.raw_data[date][hour]["parameters"]:
                assert parameter in derived_content["expected_parameter_names"]


def test_raw_data_size(der_read, info):
    """Check size of data lists"""

    parameters = der_read.raw_data[info.der_singel.dates[0]][info.der_singel.hours[0]][
        "parameters"
    ]

    list_len = None
    for parameter, values_list in parameters.items():
        # Grab the first list length as ref:
        if list_len is None:
            list_len = len(values_list)

        assert len(values_list) == list_len


def test_converted_data_structure(der_read_convert, info, derived_content):
    """Check the structure and content av .converted_data"""

    # Check dates and hours:
    for date in info.der_singel.dates:
        assert date in der_read_convert.converted_data
        for hour in info.der_singel.hours:
            assert hour in der_read_convert.converted_data[date]

            # Structure of header
            assert "header" in der_read_convert.converted_data[date][hour]
            assert len(der_read_convert.converted_data[date][hour]["header"]) == len(
                derived_content["expected_header_names"]
            )

            for header in der_read_convert.converted_data[date][hour]["header"]:
                assert header in derived_content["expected_header_names"]

            # Structure of parameters
            assert "parameters" in der_read_convert.converted_data[date][hour]
            assert len(
                der_read_convert.converted_data[date][hour]["parameters"]
            ) == len(derived_content["expected_parameter_names"])

            for parameter in der_read_convert.converted_data[date][hour]["parameters"]:
                assert parameter in derived_content["expected_parameter_names"]


def test_converted_data_size(der_read_convert, info):
    """Check size of data lists"""

    parameters = der_read_convert.converted_data[info.der_singel.dates[0]][
        info.der_singel.hours[0]
    ]["parameters"]

    list_len = None
    for parameter, values_list in parameters.items():
        # Grab the first list length as ref:
        if list_len is None:
            list_len = len(values_list)

        assert len(values_list) == list_len


def test_raw_vs_converted(der_read, der_read_convert):
    """Compare raw_data and converted_data structure and number of headers and values for each parameter."""

    raw = der_read.raw_data
    converted = der_read_convert.converted_data

    for date, hours in raw.items():
        assert date in converted
        for hour in hours:
            assert hour in converted[date]
            assert len(raw[date][hour]["header"]) == len(
                converted[date][hour]["header"]
            )
            assert len(raw[date][hour]["parameters"]) == len(
                converted[date][hour]["parameters"]
            )

            for parameter, values in raw[date][hour]["parameters"].items():
                assert parameter in converted[date][hour]["parameters"]
                assert len(values) == len(
                    converted[date][hour]["parameters"][parameter]
                )


def test_print_converted(der_read_convert, info, capsys):
    """Test incorrect source"""
    der_read_convert.print(
        info.der_singel.dates[0], info.der_singel.hours[0], source="converted"
    )

    # Capture output
    captured = capsys.readouterr()

    assert "Station: SWM00002527" in captured.out
    assert "VWNDGRAD: [(m/s) / m]" in captured.out


def test_print_raw(der_read_convert, info, capsys):
    """Test incorrect source"""
    der_read_convert.print(
        info.der_singel.dates[0], info.der_singel.hours[0], source="raw"
    )

    # Capture output
    captured = capsys.readouterr()

    assert "Station: SWM00002527" in captured.out
    assert "VWNDGRAD: [(m/s per km) * 10]" in captured.out


def test_print_missing_hour(der_read_convert, info):
    """Test incorrect source"""
    missing_hour = "42"
    with pytest.raises(KeyError):
        der_read_convert.print(info.der_singel.dates[0], missing_hour, source="raw")


# Multi-line
def test_read_multi(der_read_multi, info):
    """Multiline read"""
    # Number of dates
    assert len(der_read_multi.raw_data) == len(info.der_multi.dates)

    # We have duplicate hours, check ._dublicate_hour_counter is not zero
    assert not der_read_multi._dublicate_hour_counter == 0


def test_raw_vs_converted_multi(der_read_multi, der_read_convert_multi):
    """Compare raw_data and converted_data structure and number of headers and values for each parameter."""

    raw = der_read_multi.raw_data
    converted = der_read_convert_multi.converted_data

    for date, hours in raw.items():
        assert date in converted
        for hour in hours:
            assert hour in converted[date]
            assert len(raw[date][hour]["header"]) == len(
                converted[date][hour]["header"]
            )
            assert len(raw[date][hour]["parameters"]) == len(
                converted[date][hour]["parameters"]
            )

            for parameter, values in raw[date][hour]["parameters"].items():
                assert parameter in converted[date][hour]["parameters"]
                assert len(values) == len(
                    converted[date][hour]["parameters"][parameter]
                )
