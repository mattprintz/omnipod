import datetime
from struct import unpack, calcsize

from omnipod.records import IBFRecord


class LogDescriptions(IBFRecord):
    def __init__(self, fp):
        super().__init__(fp)
        revisions = unpack("5B", self.data[0:5])
        (
            self.logs_info_revision,
            self.insulin_history_revision,
            self.alarm_history_revision,
            self.blood_glucose_revision,
            self.insulet_stats_revision,
        ) = revisions
        date_values = unpack(">BBHBBB", self.data[5:12])
        (
            self.day,
            self.month,
            self.year,
            self.seconds,
            self.minutes,
            self.hours
        ) = date_values
        self.descriptions = {}

        log_description_count, = unpack(">H", self.data[13:15])
        for offset in range(15, 15 + (18 * log_description_count), 18):
            values = unpack(">5H2I", self.data[offset:offset+18])
            (
                log_index,
                backup,
                location,
                has_variable,
                record_size,
                first_index,
                last_index
            ) = values
            self.descriptions[log_index] = {
                'log_index': log_index,
                'backup': backup,
                'location': location,
                'has_variable': has_variable,
                'record_size': record_size,
                'first_index': first_index,
                'last_index': last_index,
            }



class LogRecord(IBFRecord):

    HISTORY = 0x03
    PUMP_ALARM =0x05
    DELETED = 0x80000000
    IGNORE = 0x100

    RECORD_TYPES = {
        HISTORY: 'HISTORY',
        PUMP_ALARM: 'PUMP_ALARM',
        DELETED: 'DELETED',
        IGNORE: 'IGNORE',
    }

    NO_ERR = 0
    GET_EEPROM_ERR = 3
    CRC_ERR = 4
    LOG_INDEX_ERR = 6
    REC_SIZE_ERR = 8

    ERROR_TYPES = {
        NO_ERR: 'NO_ERR',
        GET_EEPROM_ERR: 'GET_EEPROM_ERR',
        CRC_ERR: 'CRC_ERR',
        LOG_INDEX_ERR: 'LOG_INDEX_ERR',
        REC_SIZE_ERR: 'REC_SIZE_ERR',
    }

    def __init__(self, fp):
        super().__init__(fp)
        type_id, = unpack("B", self.data[0:1])
        (
            log_idx,
            record_size,
            self.error_code
        ) = unpack(">iHH", self.data[1:9])

        date_fmt = "<bbHbbb"
        (
            day,
            month,
            year,
            second,
            minute,
            hour,
        ) = unpack(date_fmt, self.data[9:16])
        try:
            self.dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        except ValueError:
            self.dt = None

        self.seconds_since_powerup, = unpack("<I", self.data[17:21])

        print("Processing {} record; {} bytes".format(self.RECORD_TYPES.get(type_id, "XXXUNKNOWNXX"), record_size))

        print("{} bytes remaining".format(len(self.data) - 21))
        # if type_id == self.HISTORY:
        # print()


