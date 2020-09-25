import collections
import pathlib
import pytest

# python3 -m pytest -v --cov-report html --cov=pyigra2 ./tests/


@pytest.fixture(scope="session")
def info():
    """Collection of paths to datafiles
    """
    # Setup:
    data_path = pathlib.Path(__file__).parent.resolve() / "data"

    # Create namedtuples
    Info = collections.namedtuple("Info", "obs_singel obs_multi der_singel der_multi")
    case = collections.namedtuple("case", "path dates hours")

    # obs_singel
    obs_singel = case(
        path=data_path / "SWM00002527_observation_single.txt",
        dates=("2018-01-01",),
        hours=("00",),
    )

    # obs_multi
    obs_multi = case(
        path=data_path / "SWM00002527_observation_multi.txt",
        dates=("2018-01-01", "2018-01-02"),
        hours=("00", "99"),
    )

    # der_singel
    der_singel = case(
        path=data_path / "SWM00002527_derived_single.txt",
        dates=("2020-05-26",),
        hours=("00",),
    )

    # der_multi
    der_multi = case(
        path=data_path / "SWM00002527_derived_multi.txt",
        dates=("2020-05-26", "2020-05-27"),
        hours=("00", "99"),
    )

    # Add cases to info
    all_info = Info(
        obs_singel=obs_singel,
        obs_multi=obs_multi,
        der_singel=der_singel,
        der_multi=der_multi,
    )

    yield all_info
    # Teardown:


@pytest.fixture(scope="session")
def observation_content():
    """
    """
    content = dict()
    # Expected header names
    content["expected_header_names"] = (
        "HEADREC",
        "ID",
        "YEAR",
        "MONTH",
        "DAY",
        "HOUR",
        "RELTIME",
        "NUMLEV",
        "P_SRC",
        "NP_SRC",
        "LAT",
        "LON",
    )

    # Expected header names
    content["expected_parameter_names"] = (
        "LVLTYP1",
        "LVLTYP2",
        "ETIME",
        "PRESS",
        "PFLAG",
        "GPH",
        "ZFLAG",
        "TEMP",
        "TFLAG",
        "RH",
        "DPDP",
        "WDIR",
        "WSPD",
    )

    yield content


@pytest.fixture(scope="session")
def derived_content():
    """
    """
    content = dict()
    # Expected header names
    content["expected_header_names"] = (
        "HEADREC",
        "ID",
        "YEAR",
        "MONTH",
        "DAY",
        "HOUR",
        "RELTIME",
        "NUMLEV",
        "PW",
        "INVPRESS",
        "INVHGT",
        "INVTEMPDIF",
        "MIXPRESS",
        "MIXHGT",
        "FRZPRESS",
        "FRZHGT",
        "LCLPRESS",
        "LCLHGT",
        "LFCPRESS",
        "LFCHGT",
        "LNBPRESS",
        "LNBHGT",
        "LI",
        "SI",
        "KI",
        "TTI",
        "CAPE",
        "CIN",
    )

    # Expected header names
    content["expected_parameter_names"] = (
        "PRESS",
        "REPGPH",
        "CALCGPH",
        "TEMP",
        "TEMPGRAD",
        "PTEMP",
        "PTEMPGRAD",
        "VTEMP",
        "VPTEMP",
        "VAPPRESS",
        "SATVAP",
        "REPRH",
        "CALCRH",
        "RHGRAD",
        "UWND",
        "UWDGRAD",
        "VWND",
        "VWNDGRAD",
        "N",
    )

    yield content
