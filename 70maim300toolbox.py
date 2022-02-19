from absl import app, flags, logging  # 3p dependency
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Dict, List
import datetime
import hashlib
import json
import os
import random
import requests  # 3p dependency
import string
import time

# Specify --verbosity=1 --alsologtostderr, and you can see something... nice.
# lol this two cmd args turns on additional logging.

_CONNECT_KEY = flags.DEFINE_string(
    name='connect_key',
    default=None,
    required=True,
    help=
    ("A 32 char long hex string that's generated when paring with the phone. "
     'It can be found in 70mai app data. '
     'Or use Wireshark to sniff clear text HTTP packages between the phone and the dashcam when pairing. '
     'Example: --connect_key=873ea99b5db1e67d1f065dedce6059f0'))

_OPERATIONS = flags.DEFINE_multi_enum(
    name='operations',
    default=None,
    required=True,
    enum_values=[
        'get_sd_card_status',
        'purge_files',
        'sync_files',
        'sync_time',
        'update_wifi_password',
        'stop_recording',
        'start_recording',
        'format_sd_card',
        'experimental',
    ],
    help=
    ('A list of operations to perform in sequence. '
     'Example: --operations=get_sd_card_status --operations=sync_files --operations=purge_files --operations=get_sd_card_status'
    ))

_HTTP_TIMEOUT_SEC = flags.DEFINE_float(
    name='http_timeout_sec',
    default=30,
    required=False,
    help=('Longer HTTP timeout in case the Wi-Fi connection is weak. '
          'Example: --http_timeout_sec=60'))


@dataclass
class SdCardStatus:
    status: str
    capacity_mb: int
    used_mb: int


class FileType(IntEnum):
    NORMAL = 0
    UNKNOWN_TYPE_1 = 1
    PARKING = 2
    UNKNOWN_TYPE_3 = 3
    UNKNOWN_TYPE_4 = 4
    TIME_LAPSE = 5


@dataclass
class FileEntry:
    LOCAL_FILE_TYPE_PATHS = {
        FileType.NORMAL: 'Normal',
        FileType.PARKING: 'Parking',
        FileType.TIME_LAPSE: 'TimeLapse',
    }

    path: str
    name: str
    size_b: int
    type: FileType

    def __lt__(self, other) -> bool:
        # Compare based on timestamps only.
        # Example: 'PA20211120-114000-000127.mp4' < 'NO20211121-085131-000240.mp4'
        return self.name[2:] < other.name[2:]

    def to_local_path(self) -> str:
        file_type_path = self.LOCAL_FILE_TYPE_PATHS[self.type]
        # Extract date from file path.
        # Example: PA20211120-113426-000122 => 20211120
        date_path = self.name[2:-18]
        # Example: TimeLapse/20211113/LA20211113-230648-000321.mp4
        local_path = f'{file_type_path}/{date_path}/{self.name}'
        return local_path


def _get_http_response(command: str, raw_params: Dict[str, Any] = {}) -> requests.models.Response:
    # Prepend all HTML param keys with '-' and convert values to string.
    params = {f'-{key}': str(value) for key, value in raw_params.items()}
    params['-timestamp'] = int(time.time())

    # Example:
    # record.cgi?-cmd=start&-timestamp=1546810919873ea99b5db1e67d1f065dedce6059f0
    params_str = '&'.join(f'{key}={value}' for key, value in params.items())
    hash_data = f'{command}?{params_str}{_CONNECT_KEY.value}'

    # Example: md5(hash_data) = 'a3785b506baa56d346034f4c00323c5d'
    sign_key = hashlib.md5(hash_data.encode('utf-8')).hexdigest()
    params['-signkey'] = sign_key
    logging.debug('hash_data = %s, sign_key = %s', hash_data, sign_key)

    # Example:
    # http://192.168.0.1/cgi-bin/record.cgi?-cmd=start&-timestamp=1546810919&-signkey=a3785b506baa56d346034f4c00323c5d
    logging.debug('command = %s, params = %s', command, params)
    response = requests.get(f'http://192.168.0.1/cgi-bin/{command}',
                            params=params,
                            timeout=_HTTP_TIMEOUT_SEC.value)

    logging.debug('response.text = %s', response.text)
    return response


def _check_and_get_result(text_response: str) -> Any:
    # It could have no text at all. This should be interpreted as an error.
    if len(text_response) == 0:
        raise ValueError('text_response is empty.')

    json_response: Dict[str, Any] = json.loads(text_response)

    result_code = int(json_response['ResultCode'])
    if result_code != 0:
        logging.error('text_response=%s', text_response)
        raise ValueError(f'ResultCode is {result_code}, expected 0.')

    # Example:
    # {
    #     'ResultCode': '0',
    #     'Result': {'sdstate': 'SDOK', 'sdtotal': '60882MB', 'sdused': '3360MB'}
    # }
    if 'Result' in json_response:
        return json_response['Result']

    # Example:
    # {
    #     'ResultCode': '0'
    # }
    return None


def _get_file_count(file_type: FileType) -> int:
    http_response = _get_http_response('getfilecount.cgi')

    # Cleanup response text, it has a trailing comma that breaks json.load().
    # Example:
    # [
    #     {'type': '0', 'count': '122'},
    #     {'type': '1', 'count': '0'},
    #     {'type': '2', 'count': '11'},
    #     {'type': '3', 'count': '0'},
    #     {'type': '4', 'count': '0'},
    #     {'type': '5', 'count': '86'},  # Here
    # ]
    text_response = http_response.text[:-3] + ']}'
    results: List[Dict[str, str]] = _check_and_get_result(text_response)

    for result in results:
        if int(result['type']) == file_type:
            logging.debug('result = %s', result)
            return int(result['count'])

    raise ValueError(f'No matching result for file type {file_type}.')


def _get_file_entries(file_type: FileType) -> List[FileEntry]:
    file_count = _get_file_count(file_type)
    if file_count == 0:
        return []

    http_response = _get_http_response('getfilelist.cgi', {
        'start': 1,
        'end': file_count,
        'type': int(file_type)
    })

    # Example:
    # [
    #     {'path': 'sd/Lapse', 'name': 'LA20211112-194823-000002.mp4', 'size': '5373952', 'type': '4'},
    #     {'path': 'sd/Lapse', 'name': 'LA20211112-201849-000001.mp4', 'size': '20971520', 'type': '4'}
    # ]
    results: List[Dict[str, str]] = _check_and_get_result(http_response.text)

    file_entries: List[FileEntry] = []
    for result in results:
        # The size in response isn't always accurate and can cause a file to never be purged.
        # Using HTTP header to get the real file size.
        # https://stackoverflow.com/a/44299915
        head_response = requests.head(f'http://192.168.0.1/{result["path"]}/{result["name"]}',
                                      timeout=_HTTP_TIMEOUT_SEC.value)
        content_length_b = int(head_response.headers['Content-Length'])

        file_entry = FileEntry(result['path'], result['name'], content_length_b, file_type)
        file_entries.append(file_entry)
        logging.debug('%s', file_entry)

    return file_entries


def get_sd_card_status() -> SdCardStatus:
    http_response = _get_http_response('getsdstate.cgi')
    # Example: {'sdstate': 'SDOK', 'sdtotal': '60882MB', 'sdused': '3360MB'}
    result: Dict[str, str] = _check_and_get_result(http_response.text)
    return SdCardStatus(result['sdstate'], int(result['sdtotal'][:-2]), int(result['sdused'][:-2]))


def sync_files(file_type: FileType) -> None:
    # Start with the oldest file.
    # The newest file is likely incomplete so we wait longer before downloading it.
    file_entries = _get_file_entries(file_type)
    file_entries.sort()

    if len(file_entries) == 0:
        logging.info('No files to download for %s', file_type)
        return

    for index, file_entry in enumerate(file_entries):
        # Example: TimeLapse/20211113/LA20211113-230648-000321.mp4
        local_path = file_entry.to_local_path()

        if os.path.exists(local_path) and os.path.getsize(local_path) == file_entry.size_b:
            logging.info('(%s / %s) Skip downloading %s', index + 1, len(file_entries),
                         file_entry.name)
            continue

        logging.info('(%s / %s) Downloading %s', index + 1, len(file_entries), file_entry.name)

        # Example: TimeLapse/20211113
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Stream file content to local.
        # https://docs.python-requests.org/en/latest/user/quickstart/#raw-response-content
        response = requests.get(f'http://192.168.0.1/{file_entry.path}/{file_entry.name}',
                                timeout=_HTTP_TIMEOUT_SEC.value,
                                stream=True)
        with open(local_path, 'wb') as local_file:
            for chunk in response.iter_content(1024 * 1024):  # 1MiB
                local_file.write(chunk)


def purge_files(file_type: FileType) -> None:
    file_entries = _get_file_entries(file_type)
    file_entries.sort()

    for index, file_entry in enumerate(file_entries):
        # Example: TimeLapse/20211113/LA20211113-230648-000321.mp4
        local_path = file_entry.to_local_path()

        # Only delete files that have been downloaded and match size.
        # The newest file will change size as it records and will need to be re-downloaded.
        if not os.path.exists(local_path) or os.path.getsize(local_path) != file_entry.size_b:
            logging.info('(%s / %s) Skip deleting %s', index + 1, len(file_entries),
                         file_entry.name)
            continue

        logging.info('(%s / %s) Deleting %s', index + 1, len(file_entries), file_entry.name)

        http_response = _get_http_response('delete.cgi', {
            'path': file_entry.path,
            'name': file_entry.name
        })
        _check_and_get_result(http_response.text)


def sync_time() -> None:
    # Example: 20211121115810
    formatted_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    http_response = _get_http_response('setsystime.cgi', {'time': formatted_time})
    _check_and_get_result(http_response.text)

    logging.info('Synced to time: %s', formatted_time)


def update_wifi_password() -> str:
    # Example: zJLSp881PJw1QTkfAm0EEJrbTPqxTeX0nG4LtaT7syCm5J825KUjboobCgVcawD
    new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(63))

    # The dashcam automatically truncates password length to <= 63.
    http_response = _get_http_response('setwifi.cgi', {'wifikey': new_password})
    _check_and_get_result(http_response.text)

    logging.info('New Wi-Fi password: %s', new_password)
    return new_password


def set_recording(is_recording: bool) -> None:
    # record.cgi doesn't work for M300.
    # http_response = _get_http_response('record.cgi', {'cmd': 'start' if is_recording else 'stop'})
    http_response = _get_http_response('setaccessalbum.cgi', {'enable': 1 if is_recording else 0})
    _check_and_get_result(http_response.text)


def format_sd_card() -> None:
    http_response = _get_http_response('sdcommand.cgi', {'format': 1})
    _check_and_get_result(http_response.text)


# Good for trying out new stuff without disrupting the rest of the script.
def experimental() -> Any:
    http_response = _get_http_response('getAllMenu.cgi')
    return _check_and_get_result(http_response.text)


def main(_: List[str]):
    logging.get_absl_handler().use_absl_log_file()

    operation: str
    for operation in _OPERATIONS.value:
        if operation == 'get_sd_card_status':
            print(get_sd_card_status())
            continue

        if operation == 'sync_files':
            sync_files(FileType.NORMAL)
            sync_files(FileType.PARKING)
            sync_files(FileType.TIME_LAPSE)
            continue

        if operation == 'purge_files':
            purge_files(FileType.NORMAL)
            purge_files(FileType.PARKING)
            purge_files(FileType.TIME_LAPSE)
            continue

        if operation == 'sync_time':
            sync_time()
            continue

        if operation == 'update_wifi_password':
            print(update_wifi_password())
            continue

        if operation == 'start_recording':
            set_recording(True)
            continue

        if operation == 'stop_recording':
            set_recording(False)
            continue

        if operation == 'format_sd_card':
            format_sd_card()
            continue

        if operation == 'experimental':
            print(experimental())
            continue

        raise ValueError(f'Unknown operation {operation}')


if __name__ == '__main__':
    app.run(main)
