import pathlib
import pytest
from pyigra2.observations import Observations


@pytest.fixture(scope="module")
def obs(info):
    """Create a fresh instance of Observations"""
    # Setup
    obs = Observations(info.obs_singel.path)
    yield obs
    # Teardown


@pytest.fixture(scope="module")
def obs_read(info):
    """Create a fresh instance of Observations"""
    # Setup
    obs = Observations(info.obs_singel.path)
    obs.read()
    yield obs
    # Teardown


@pytest.fixture(scope="module")
def obs_read_convert(info):
    """Create a fresh instance of Observations"""
    # Setup
    obs = Observations(info.obs_singel.path)
    obs.read()
    obs.convert_to_numpy()
    yield obs
    # Teardown


@pytest.fixture(scope="module")
def obs_multi(info):
    """Create a fresh instance of Observations"""
    # Setup
    obs = Observations(info.obs_multi.path)
    yield obs
    # Teardown


@pytest.fixture(scope="module")
def obs_read_multi(info):
    """Create a fresh instance of Observations"""
    # Setup
    obs = Observations(info.obs_multi.path)
    obs.read()
    yield obs
    # Teardown


@pytest.fixture(scope="module")
def obs_read_convert_multi(info):
    """Create a fresh instance of Observations"""
    # Setup
    obs = Observations(info.obs_multi.path)
    obs.read()
    obs.convert_to_numpy()
    yield obs
    # Teardown


def test_header_names(obs, observation_content):
    """Test that all header names is in the object"""
    expected_header_names = observation_content["expected_header_names"]

    # Object names
    names_header_name_index = tuple(obs._header_name_index.keys())
    names_header_units = tuple(obs._header_units.keys())

    # Length
    assert len(names_header_name_index) == len(expected_header_names)
    assert len(names_header_units) == len(expected_header_names)

    for name in expected_header_names:
        assert name in names_header_name_index
        assert name in names_header_units


def test_parameter_names(obs, observation_content):
    """Test that all header names is in the object"""
    expected_parameter_names = observation_content["expected_parameter_names"]

    # Object names
    names_parameters_name_index = tuple(obs._parameters_name_index.keys())
    names_parameter_units = tuple(obs._parameter_units.keys())

    # Length
    assert len(names_parameters_name_index) == len(expected_parameter_names)
    assert len(names_parameter_units) == len(expected_parameter_names)

    for name in expected_parameter_names:
        assert name in names_parameters_name_index
        assert name in names_parameter_units


def test_read_state(obs_read, observation_content):
    """Test read and check the state of the object"""
    # Check state
    assert isinstance(obs_read.filename, pathlib.PurePath)
    assert obs_read.raw_data
    assert obs_read.converted_data == {}
    assert obs_read._header_name_index
    assert obs_read._header_units
    assert obs_read._parameters_name_index
    assert obs_read._parameter_units
    assert obs_read._dublicate_hour_counter == 0
    assert obs_read._add_data_bool

    # During read, _reset_header_parameters is called which resets header parameters
    assert obs_read._header == {}

    # _parameters should be a dict keys="parameter names" and value="empty list"
    assert isinstance(obs_read._parameters, dict)
    assert len(obs_read._parameters) == len(
        observation_content["expected_parameter_names"]
    )
    for value in obs_read._parameters.values():
        assert not value
        assert isinstance(value, list)


def test_read_file_not_found():
    """Test if file is not found"""
    obs = Observations("FileNotFound.txt")

    with pytest.raises(FileNotFoundError):
        obs.read()


def test_raw_data_structure(obs_read, info, observation_content):
    """Check the structure and content av .raw_data"""

    # Check dates and hours:
    for date in info.obs_singel.dates:
        assert date in obs_read.raw_data
        for hour in info.obs_singel.hours:
            assert hour in obs_read.raw_data[date]

            # Structure of header
            assert "header" in obs_read.raw_data[date][hour]
            assert len(obs_read.raw_data[date][hour]["header"]) == len(
                observation_content["expected_header_names"]
            )

            for header in obs_read.raw_data[date][hour]["header"]:
                assert header in observation_content["expected_header_names"]

            # Structure of parameters
            assert "parameters" in obs_read.raw_data[date][hour]
            assert len(obs_read.raw_data[date][hour]["parameters"]) == len(
                observation_content["expected_parameter_names"]
            )

            for parameter in obs_read.raw_data[date][hour]["parameters"]:
                assert parameter in observation_content["expected_parameter_names"]


def test_raw_data_size(obs_read, info):
    """Check size of data lists"""

    parameters = obs_read.raw_data[info.obs_singel.dates[0]][info.obs_singel.hours[0]][
        "parameters"
    ]

    list_len = None
    for parameter, values_list in parameters.items():
        # Grab the first list length as ref:
        if list_len is None:
            list_len = len(values_list)

        assert len(values_list) == list_len


def test_converted_data_structure(obs_read_convert, info, observation_content):
    """Check the structure and content av .converted_data"""

    # Check dates and hours:
    for date in info.obs_singel.dates:
        assert date in obs_read_convert.converted_data
        for hour in info.obs_singel.hours:
            assert hour in obs_read_convert.converted_data[date]

            # Structure of header
            assert "header" in obs_read_convert.converted_data[date][hour]
            assert len(obs_read_convert.converted_data[date][hour]["header"]) == len(
                observation_content["expected_header_names"]
            )

            for header in obs_read_convert.converted_data[date][hour]["header"]:
                assert header in observation_content["expected_header_names"]

            # Structure of parameters
            assert "parameters" in obs_read_convert.converted_data[date][hour]
            assert len(
                obs_read_convert.converted_data[date][hour]["parameters"]
            ) == len(observation_content["expected_parameter_names"])

            for parameter in obs_read_convert.converted_data[date][hour]["parameters"]:
                assert parameter in observation_content["expected_parameter_names"]


def test_converted_data_size(obs_read_convert, info):
    """Check size of data lists"""

    parameters = obs_read_convert.converted_data[info.obs_singel.dates[0]][
        info.obs_singel.hours[0]
    ]["parameters"]

    list_len = None
    for parameter, values_list in parameters.items():
        # Grab the first list length as ref:
        if list_len is None:
            list_len = len(values_list)

        assert len(values_list) == list_len


def test_raw_vs_converted(obs_read, obs_read_convert):
    """Compare raw_data and converted_data structure and number of headers and values for each parameter."""

    raw = obs_read.raw_data
    converted = obs_read_convert.converted_data

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


def test_print_converted(obs_read_convert, info, capsys):
    """Test incorrect source"""
    obs_read_convert.print(
        info.obs_singel.dates[0], info.obs_singel.hours[0], source="converted"
    )

    # Capture output
    captured = capsys.readouterr()

    assert "Station: SWM00002527" in captured.out
    assert "WSPD: [m/s]" in captured.out


def test_print_raw(obs_read_convert, info, capsys):
    """Test incorrect source"""
    obs_read_convert.print(
        info.obs_singel.dates[0], info.obs_singel.hours[0], source="raw"
    )

    # Capture output
    captured = capsys.readouterr()

    assert "Station: SWM00002527" in captured.out
    assert "WSPD: [m/s * 10]" in captured.out


def test_print_missing_hour(obs_read_convert, info):
    """Test incorrect source"""
    missing_hour = "42"
    with pytest.raises(KeyError):
        obs_read_convert.print(info.obs_singel.dates[0], missing_hour, source="raw")


# Multi-line
def test_read_multi(obs_read_multi, info):
    """Multiline read"""
    # Number of dates
    assert len(obs_read_multi.raw_data) == len(info.obs_multi.dates)

    # We have duplicate hours, check ._dublicate_hour_counter is not zero
    assert not obs_read_multi._dublicate_hour_counter == 0


def test_raw_vs_converted_multi(obs_read_multi, obs_read_convert_multi):
    """Compare raw_data and converted_data structure and number of headers and values for each parameter."""

    raw = obs_read_multi.raw_data
    converted = obs_read_convert_multi.converted_data

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
