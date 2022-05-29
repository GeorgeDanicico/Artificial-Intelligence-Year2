
# left, middle, right
THETA = {
    "NVB": (None, -40, -25),
    "NB": (-40, -25, -10),
    "N": (-20, -10, 0),
    "ZO": (-5, 0, 5),
    "P": (0, 10, 20),
    "PB": (10, 25, 40),
    "PVB": (25, 40, None)
}

OMEGA = {
    "NB": (None, -8, -3),
    "N": (-6, -3, 0),
    "ZO": (-1, 0, 1),
    "P": (0, 3, 6),
    "PB": (3, 8, None)
}

FORCE = {
    "NVVB": (None, -32, -24),
    "NVB": (-32, -24, -16),
    "NB": (-24, -16, -8),
    "N": (-16, -8, 0),
    "Z": (-4, 0, 4),
    "P": (0, 8, 16),
    "PB": (8, 16, 24),
    "PVB": (16, 24, 32),
    "PVVB": (24, 32, None)
}

FUZZY_TABLE = dict()
FUZZY_TABLE["NB"] = dict()
FUZZY_TABLE["NB"]["NB"] = "NVVB"
FUZZY_TABLE["NB"]["N"] = "NVB"
FUZZY_TABLE["NB"]["ZO"] = "NB"
FUZZY_TABLE["NB"]["P"] = "N"
FUZZY_TABLE["NB"]["PB"] = "Z"
FUZZY_TABLE["N"] = dict()
FUZZY_TABLE["N"]["NB"] = "NVB"
FUZZY_TABLE["N"]["N"] = "NB"
FUZZY_TABLE["N"]["ZO"] = "N"
FUZZY_TABLE["N"]["P"] = "Z"
FUZZY_TABLE["N"]["PB"] = "P"
FUZZY_TABLE["ZO"] = dict()
FUZZY_TABLE["ZO"]["NB"] = "NB"
FUZZY_TABLE["ZO"]["N"] = "N"
FUZZY_TABLE["ZO"]["ZO"] = "Z"
FUZZY_TABLE["ZO"]["P"] = "P"
FUZZY_TABLE["ZO"]["PB"] = "PB"
FUZZY_TABLE["P"] = dict()
FUZZY_TABLE["P"]["NB"] = "N"
FUZZY_TABLE["P"]["N"] = "Z"
FUZZY_TABLE["P"]["ZO"] = "P"
FUZZY_TABLE["P"]["P"] = "PB"
FUZZY_TABLE["P"]["PB"] = "PVB"
FUZZY_TABLE["PB"] = dict()
FUZZY_TABLE["PB"]["NB"] = "Z"
FUZZY_TABLE["PB"]["N"] = "P"
FUZZY_TABLE["PB"]["ZO"] = "PB"
FUZZY_TABLE["PB"]["P"] = "PVB"
FUZZY_TABLE["PB"]["PB"] = "PVVB"
FUZZY_TABLE["PVB"] = dict()
FUZZY_TABLE["PVB"]["NB"] = "P"
FUZZY_TABLE["PVB"]["N"] = "PB"
FUZZY_TABLE["PVB"]["ZO"] = "PVB"
FUZZY_TABLE["PVB"]["P"] = "PVVB"
FUZZY_TABLE["PVB"]["PB"] = "PVVB"
FUZZY_TABLE["NVB"] = dict()
FUZZY_TABLE["NVB"]["N"] = "NVVB"
FUZZY_TABLE["NVB"]["ZO"] = "NVB"
FUZZY_TABLE["NVB"]["P"] = "NB"
FUZZY_TABLE["NVB"]["PB"] = "N"
FUZZY_TABLE["NVB"]["NB"] = "NVVB"