eval_block_size_list = [
    # Positive/Negative/Zero, Str/Int/Flt/Boolean/Error/DataStruc, Escape Characters
    {"Input": -15, "Output": ValueError},
    {"Input": 0, "Output": ValueError},
    {"Input": 1, "Output": 2},
    {"Input": 1.5, "Output": TypeError},
    {"Input": -1.5, "Output": TypeError},
    {"Input": 1610612736-32, "Output": 1610612736},
    {"Input": 1610612736*2, "Output": 1610612736},
    {"Input": -1610612736, "Output": ValueError},
    {"Input": -1.5, "Output": TypeError},
    {"Input": -1.5, "Output": TypeError},
    {"Input": "-1.5", "Output": TypeError},
    {"Input": "20", "Output": TypeError},
    {"Input": "-15", "Output": TypeError},
    {"Input": [16], "Output": TypeError},
    {"Input": [15, 16], "Output": TypeError},
    {"Input": True, "Output": TypeError},
    {"Input": False, "Output": TypeError},
    {"Input": KeyError, "Output": TypeError}
]