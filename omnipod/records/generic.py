from struct import unpack, calcsize


class IBFRecord(object):
    def __init__(self, fp):
        self._size, = unpack(">H", fp.read(2))
        self.data = fp.read(self._size - 2)
        self._checksum, = unpack(">H", fp.read(2))
        checksum = 0
        for c in self.data:
            checksum += c
        if checksum != self._checksum:
            raise ValueError("Checksum integrity error")


class EEPromRecord(IBFRecord):
    def __init__(self, fp):
        super().__init__(fp)

        offset = 13
        pattern = "<4I2B"
        (
            self.bolus_incr,
            self.bolus_max,
            self.basal_max,
            self.low_vol,
            self.auto_off,
            self.language,
        ) = unpack(pattern, self.data[offset:offset + calcsize(pattern)])
        offset += calcsize(pattern) + 4
        self.expire_alert, = unpack("B", self.data[offset:offset + 1])
        offset += 6
        self.bg_reminder, = unpack("B", self.data[offset:offset + 1])
        offset += 2
        self.conf_alert, self.reminder_alert = unpack("2B", self.data[offset:offset+2])
        offset += 10
        self.remote_id, = unpack("<I", self.data[offset:offset+4])
        offset += 23
        pattern = "<7B3HB"
        (
            self.temp_basal_type,
            self.ext_bolus_type,
            self.bolus_reminder,
            self.bolus_calcs,
            self.bolus_calcs_reverse,
            self.bg_display,
            self.bg_sound,
            self.bg_min,
            self.bg_goal_low,
            self.bg_goal_up,
            self.insulin_duration,
        ) = unpack(pattern, self.data[offset:offset+calcsize(pattern)])
        offset += calcsize(pattern) + 19
        self.alarm_repair_count, self.pdm_config = unpack("<bI", self.data[offset:offset+5])
