from enum import Enum


def convert_list_to_string(list_of_values):
    string_representation = ""
    for value in list_of_values:
        if isinstance(value, str):
            string_representation += f"'{value}'"
        else:
            string_representation += f"{value}"
        string_representation += ", "
    string_representation = string_representation[:-2]
    return string_representation


def read_file(file_path):
    with open(file_path, 'r') as f:
        file = f.read()
    return file


def write_file(data, file_path):
    with open(file_path, "w") as f:
        f.write(data)


class TaxiType(Enum):
    Yellow = "yellow"
    Green = "green"
    ForHire = "fhv"
    HighVolume = "fhvhv"

    def __str__(self):
        return str(self.value)


def _filename_for_date(year: int, month: int, taxi_type: str) -> str:
    assert 2000 < year < 2050
    assert 1 <= month <= 12
    return f"{taxi_type}_tripdata_{year:04}-{month:02}.parquet"
