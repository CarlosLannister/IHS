"""
swat-s1 utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

Actuator tags are redundant, we will use only the XXX_XXX_OPEN tag ignoring
the XXX_XXX_CLOSE with the following convention:
    - 0 = error
    - 1 = on
    - 2 = off

sqlite uses float keyword and cpppo use REAL keyword.
"""

from minicps.utils import build_debug_logger

swat = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')

# physical process {{{1
# SPHINX_SWAT_TUTORIAL PROCESS UTILS(
GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2
PUMP_FLOWRATE_IN = 1.35        # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 1.85       # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100E-3
T_PLC_W = 100E-3

T_PP_R = 200E-3
T_PP_W = 200E-3
T_HMI_R = 100E-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    'LL': 0.0,
    'L': 500.0,
    'H': 800.0,
    'HH': 1200.0,
}
LIT_101_M = {  # raw water tank m
    'LL': 0.00,
    'L': 0.500,
    'H': 0.800,
    'HH': 1.200,
}

# Scada parameters

SCADA_LOOP = 1


MQTT_SERVER = '127.0.0.1'
MQTT_PORT = 1883

#

TANK_HEIGHT = 1.600  # m

PLC_PERIOD_SEC = 0.60  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 100000000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

RWT_INIT_LEVEL = 0.500  # l

# m^3 / h
FIT_201_THRESH = 1.00
# SPHINX_SWAT_TUTORIAL PROCESS UTILS)


#### From here IP stuff

# topo {{{1
IP = {
    'plc0': '10.168.1.10',
    'plc1': '10.168.1.20',
    'rtu': '10.168.1.20',
    'plc2': '10.168.1.30',
    'attacker': '10.168.1.77',
    'scada': '10.168.1.150'
}

MAC = {
    'plc0': '00:1D:9C:C6:A0:60',
    'plc1': '00:1D:9C:C7:B0:70',
    'rtu': '00:1D:9C:C7:B0:71',
    'plc2': '00:1D:9C:C8:BC:46',
    'attacker': 'AA:AA:AA:AA:AA:AA',
    'scada': 'BB:BB:BB:BB:BB:BB'
}

SUBNET_1 = {
    'plc0': '10.168.2.10',
    'rtu': '10.168.2.20',
    'plc2': '10.168.2.30',
    'attacker': '10.168.2.77'
}

SUBNET_1_MAC = {
    'plc0': '00:1D:9C:C6:20:60',
    'rtu': '00:1D:9C:C7:20:71',
    'plc2': '00:1D:9C:C8:2C:46',
    'attacker': 'AA:AA:AA:AA:2A:AA'
}

SUBNET_2 = {
    'plc0': '10.168.3.10',
    'rtu': '10.168.3.20',
    'plc2': '10.168.3.30',
    'attacker': '10.168.3.77'
}

SUBNET_2_MAC = {
    'plc0': '00:1D:9C:C6:30:60',
    'rtu': '00:1D:9C:C7:30:71',
    'plc2': '00:1D:9C:C8:3C:46',
    'attacker': 'AA:AA:AA:AA:3A:AA'
}

SUBNET_3 = {
    'plc0': '10.168.4.10',
    'rtu': '10.168.4.20',
    'plc2': '10.168.4.30',
    'attacker': '10.168.4.77'
}

SUBNET_3_MAC = {
    'plc0': '00:1D:9C:C6:40:60',
    'rtu': '00:1D:9C:C7:40:71',
    'plc2': '00:1D:9C:C8:4C:46',
    'attacker': 'AA:AA:AA:AA:4A:AA'
}

NETMASK = '/24'




# others
# TODO
PLC0_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC1_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC2_DATA = {
    'TODO': 'TODO',
}



# COPY

PLC0_DATA = {
    'TODO': 'TODO',
}
PLC0_TAGS = (
    #TODO add flag here
    ('MV001', 0, 'INT'),
)
PLC0_SERVER = {
    'address': IP['plc0'],
    'tags': PLC0_TAGS
}
PLC0_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC0_SERVER
}
PATH = 'swat_s1_db.sqlite'
NAME = 'swat_s1'

STATE = {
    'name': NAME,
    'path': PATH
}

####

# SPHINX_SWAT_TUTORIAL PLC0 UTILS(

PLC0_TAGS = (
    #TODO add flag here
    ('MV001', 0, 'INT'),
)
PLC0_SERVER = {
    'address': IP['plc0'],
    'tags': PLC0_TAGS
}
PLC0_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC0_SERVER
}



# SPHINX_SWAT_TUTORIAL PLC1 UTILS(
# RTU UTILS


PLC1_ADDR = IP['plc1']


PLC1_TAGS = (
    ('LIT101', 1, 'REAL'),
    # interlocks does NOT go to the statedb
)
PLC1_SERVER = {
    'address': PLC1_ADDR,
    'tags': PLC1_TAGS
}

PLC1_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC1_SERVER
}

RTU_ADDR = IP['rtu']
RTU_TAGS = (
    ('LIT101', 1, 'REAL'),
    ('MODE', 1, 'INT')
)
RTU_SERVER = {
    'address': RTU_ADDR,
    'tags': RTU_TAGS
}
RTU_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': RTU_SERVER
}

# SCADA values


SCADA_ADDR = IP['scada']
SCADA_TAGS = (
    ('LIT101', 1, 'REAL'),
    ('MODE', 1, 'INT')
)
SCADA_SERVER = {
    'address': SCADA_ADDR,
    'tags': SCADA_TAGS
}
SCADA_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': SCADA_SERVER
}

# PLC1 UTILS)

PLC2_ADDR = IP['plc2']
PLC2_TAGS = (
    ('P201', 2, 'INT'),
    ('FIT201', 2, 'REAL')
    # no interlocks
)
PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS
}
PLC2_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC2_SERVER
}

# Test protocol
PLC3_TAGS = (10, 10, 10, 10)
PLC3_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC3_TAGS
}
PLC3_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': PLC3_SERVER
}

# state TODO change name
PATH = 'swat_s1_db.sqlite'
NAME = 'swat_s1'

STATE = {
    'name': NAME,
    'path': PATH
}


# WaterTower subnet initial state

SCHEMA = """
CREATE TABLE swat_s1 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO swat_s1 VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_s1 VALUES ('MV001',    0, '1');
    INSERT INTO swat_s1 VALUES ('LIT101',   1, '0.500');
    
    INSERT INTO swat_s1 VALUES ('P201',     2, '2');
    INSERT INTO swat_s1 VALUES ('FIT201',   2, '2.45');
"""

# subnet 2

PATH_2 = 'swat_s2_db.sqlite'
NAME_2 = 'swat_s2'

STATE_2 = {
    'name': NAME_2,
    'path': PATH_2
}

SCHEMA_2 = """
CREATE TABLE swat_s2 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT_2 = """
    INSERT INTO swat_s2 VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_s2 VALUES ('MV001',    0, '1');
    INSERT INTO swat_s2 VALUES ('LIT101',   1, '0.500');
    
    INSERT INTO swat_s2 VALUES ('P201',     2, '2');
    INSERT INTO swat_s2 VALUES ('FIT201',   2, '2.45');
"""


#subnet 3

PATH_3 = 'swat_s3_db.sqlite'
NAME_3 = 'swat_s3'

STATE_3 = {
    'name': NAME_3,
    'path': PATH_3
}

SCHEMA_3 = """
CREATE TABLE swat_s3 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT_3 = """
    INSERT INTO swat_s3 VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_s3 VALUES ('MV001',    0, '1');
    INSERT INTO swat_s3 VALUES ('LIT101',   1, '0.500');
    
    INSERT INTO swat_s3 VALUES ('P201',     2, '2');
    INSERT INTO swat_s3 VALUES ('FIT201',   2, '2.45');
"""

# state TODO change name
PATH2 = 'hmi_db.sqlite'
NAME2 = 'hmi'

STATE2 = {
    'name': NAME2,
    'path': PATH2
}

SCHEMA2 = """
CREATE TABLE hmi (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT2 = """
    INSERT INTO hmi VALUES ('FIT101',   1, '2.55');
    INSERT INTO hmi VALUES ('MV001',    0, '1');
    INSERT INTO hmi VALUES ('LIT101',   1, '0.500');
    
    INSERT INTO hmi VALUES ('P201',     2, '2');
    INSERT INTO hmi VALUES ('FIT201',   2, '2.45');
    INSERT INTO hmi VALUES ('MODE',   1, '1');
"""