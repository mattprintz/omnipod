from struct import unpack, calcsize

from . import IBFRecord
from omnipod.utils import clean_string


class BasalPrograms(IBFRecord):
    PREFIX_STRUCT = '>3H'

    def __init__(self, fp):
        super().__init__(fp)
        offset = calcsize(self.PREFIX_STRUCT)
        prefix_data = unpack(self.PREFIX_STRUCT, self.data[0:offset])
        self.program_count, self.enabled_index, max_name_size = prefix_data
        self.programs = {}
        record_struct = ">H{}s".format(max_name_size)
        record_size = calcsize(record_struct)
        for _ in range(self.program_count):
            index, name = unpack(record_struct, self.data[offset:offset+record_size])
            self.programs[index] = clean_string(name)
            offset += record_size

    @property
    def active_program(self):
        return self.programs[self.enabled_index]


