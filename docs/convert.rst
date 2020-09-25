Conversion tables
==========================================

This document describes how parameters are converted when using
.convert_to_numpy() method found in both Observations and Derived classes.

Observations
-----------------------------------------
Observation files are converted according to the following table

Headers:

=========   ======  ======
Header      Unit    Type
=========   ======  ======
HEADREC     [-]     str
ID          [-]     str
YEAR        [yyyy]  str
MONTH       [mm]    str
DAY         [dd]    str
HOUR        [HH]    str
RELTIME     [HHMM]  str
NUMLEV      [-]     float
P_SRC       [-]     str
NP_SRC      [-]     str
LAT         [-]     float
LON         [-]     float
=========   ======  ======

Parameters

=========   ======= ======
Parameter   Unit    Type
=========   ======= ======
LVLTYP1     [-]     int
LVLTYP2     [-]     int
ETIME       [MMMSS] float
PRESS       [Pa]    float
PFLAG       [-]     str
GPH         [m]     float
ZFLAG       [-]     str
TEMP        [K]     float
TFLAG       [-]     str
RH          [%]     float
DPDP        [K]     float
WDIR        [rad]   float
WSPD        [m/s]   float
=========   ======= ======

Derived
-----------------------------------------
Derived files are converted according to the following table

Headers

==========  ======  ======
Header      Unit    Type
==========  ======  ======
HEADREC     [-]     str
ID          [-]     str
YEAR        [yyyy]  str
MONTH       [mm]    str
DAY         [dd]    str
HOUR        [HH]    str
RELTIME     [HHMM]  str
NUMLEV      [-]     float
PW          [mm]    float
INVPRESS    [Pa]    float
INVHGT      [m]     float
INVTEMPDIF  [K]     float
MIXPRESS    [Pa]    float
MIXHGT      [m]     float
FRZPRESS    [Pa]    float
FRZHGT      [m]     float
LCLPRESS    [Pa]    float
LCLHGT      [m]     float
LFCPRESS    [Pa]    float
LFCHGT      [m]     float
LNBPRESS    [Pa]    float
LNBHGT      [m]     float
LI          [K]     float
SI          [K]     float
KI          [K]     float
TTI         [K]     float
CAPE        [J/kg]  float
CIN         [J/kg]  float
==========  ======  ======

Parameters

==========  =========== ======
Parameter   Unit        Type
==========  =========== ======
PRESS       [Pa]        float
REPGPH      [m]         float
CALCGPH     [m]         float
TEMP        [K]         float
TEMPGRAD    [K/m]       float
PTEMP       [K]         float
PTEMPGRAD   [K/m]       float
VTEMP       [K]         float
VPTEMP      [K]         float
VAPPRESS    [Pa]        float
SATVAP      [Pa]        float
REPRH       [%]         float
CALCRH      [%]         float
RHGRAD      [%/m]       float
UWND        [m/s]       float
UWDGRAD     [(m/s) / m] float
VWND        [m/s]       float
VWNDGRAD    [(m/s) / m] float
N           [-]         float
==========  =========== ======
