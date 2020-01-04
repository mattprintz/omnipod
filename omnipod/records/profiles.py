from collections import namedtuple
from struct import unpack, calcsize

from . import IBFRecord


ProfileType = namedtuple('ProfileType', ['name', 'mfr_name', 'basal', 'key_name', 'value_name'])

PROFILE_TYPES = {
    11: ProfileType("carbRatio", "IC Ratio", False, "amount", "value"),
    12: ProfileType("insulinSensitivity", "Correction", False, "amount", "value"),
    13: ProfileType("bgTarget", "Target BG", False, "low", "value"),
    14: ProfileType("bgThreshold", "BG Threshold", False, "amount", "value"),
    15: ProfileType("basalprofile0", "Basal Profile 0", True, "rate", "units"),
    16: ProfileType("basalprofile1", "Basal Profile 1", True, "rate", "units"),
    17: ProfileType("basalprofile2", "Basal Profile 2", True, "rate", "units"),
    18: ProfileType("basalprofile3", "Basal Profile 3", True, "rate", "units"),
    19: ProfileType("basalprofile4", "Basal Profile 4", True, "rate", "units"),
    20: ProfileType("basalprofile5", "Basal Profile 5", True, "rate", "units"),
    21: ProfileType("basalprofile6", "Basal Profile 6", True, "rate", "units")
}


class Profile(IBFRecord):
    def __init__(self, fp, basal_programs):
        super().__init__(fp)
        index, = unpack("B", self.data[0:1])
        self.error_code, = unpack(">H", self.data[7:9])
        self.operation_time, = unpack("<I", self.data[9:13])
        self.profile = []

        profile_type = PROFILE_TYPES.get(index)
        if profile_type.basal:
            basal_program_idx = index - 15
            self.name = basal_programs.programs[basal_program_idx]
        else:
            self.name = profile_type.name

        for offset in range(13, 13 + (48 * 4), 4):
            profile_value, = unpack("<I", self.data[offset:offset+4])
            self.profile.append(profile_value)

