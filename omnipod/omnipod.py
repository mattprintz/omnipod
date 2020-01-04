from struct import unpack, calcsize

from .records import (IBFRecord, Profile, BasalPrograms, EEPromRecord, LogRecord, LogDescriptions)
from .utils import clean_string


# Classes

class IBFFile(object):
    def __init__(self):
        self.ibf_version = None
        self.eng_version = None
        self.vendor_id = None
        self.product_id = None

    def _load_version_data(self, version_record):
        data = unpack(">6h8s8s", version_record.data)
        self.ibf_version = tuple(data[0:3])
        self.eng_version = tuple(data[3:6])
        self.vendor_id = clean_string(data[6])
        self.product_id = clean_string(data[7])

    @classmethod
    def load(cls, fp):
        self = cls()
        fp.seek(0)
        version_record = IBFRecord(fp)
        self._load_version_data(version_record)

        # Skip unidentified/unneeded data
        fp.read(46)

        self.basal_programs = BasalPrograms(fp)

        self.eeprom_record = EEPromRecord(fp)

        self.profiles = [Profile(fp, self.basal_programs) for _ in range(11)]

        self.log_descriptions = LogDescriptions(fp)

        self.log_records = []
        while fp.peek(1):
            log_record = LogRecord(fp)
            self.log_records.append(log_record)

        return self


