import pathlib
import numpy as np
import pytest
from pyigra2.base import IGRABase


@pytest.fixture(scope="function")
def base(info):
    """ Create a fresh instance of IGRABAse
    """
    # Setup
    ib = IGRABase(info.obs_singel.path)
    yield ib
    # Teardown


def helper_initial_state(ib):
    """ Helper function for checking IGRABase initial state
    """
    state = (
        isinstance(ib.filename, pathlib.PurePath),
        ib.raw_data == {},
        ib.converted_data == {},
        ib._header_name_index == {},
        ib._header_units == {},
        ib._parameters_name_index == {},
        ib._parameter_units == {},
        ib._dublicate_hour_counter == 0,
        not ib._add_data_bool,
        ib._header == {},
        ib._parameters == {},
    )
    return state


def test_init(base):
    """ Test that the initial state of the instance is correct
    """
    assert all(helper_initial_state(base))


def test_read(base):
    """ Test that calling the read should not do anything to the object when called from IGRABAse
    """
    base.read()
    assert all(helper_initial_state(base))


def test_convert_to_numpy(base):
    """ Test that calling the convert_to_numpy should not do anything to the object when called from IGRABAse
    """
    base.read()
    base.convert_to_numpy()
    assert all(helper_initial_state(base))


def test_print(base):
    """ Test the print method. Most test will focus on the input checks as object is empty.
    """
    # Helper
    date = "2018-01-01"
    hour = "00"
    # Read object, nothing happens
    base.read()

    # Print method
    # Wrong source
    with pytest.raises(ValueError):
        base.print(date, hour, source="fail")

    # Missing date:
    with pytest.raises(KeyError):
        base.print(date, hour)

    # Missing hour
    base.raw_data[date] = {}
    with pytest.raises(KeyError):
        base.print(date, hour)


def test_reset_header_parameters(base):
    """ Test that calling the _convert_hea_reset_header_parameters should not do anything to the object when called from IGRABAse
    """
    base._reset_header_parameters()
    assert all(helper_initial_state(base))


def test_convert_header(base):
    """ Test that calling the _convert_header should not do anything to the object when called from IGRABAse
    """
    base._convert_header({})
    assert all(helper_initial_state(base))


def test_convert_parameters(base):
    """ Test that calling the _convert_parameters should not do anything to the object when called from IGRABAse
    """
    base._convert_parameters({})
    assert all(helper_initial_state(base))


def test_missing_value():
    """ Test the missing value static method in IGRABase
    """
    # Missing true
    assert np.isnan(IGRABase._missing_test("-99999", "-99999"))
    # Missing false: dangerous to test floats with equal sign (==) due to floating point representation.
    out = IGRABase._missing_test("-99", "10")
    assert isinstance(out, float)
    assert int(out) == 10
