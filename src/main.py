from absl import app, flags, logging

from src.files.filetype import FileType
from src.files.getfiles import get_files
from src.files.purgefiles import purge_files
from src.misc.recordingutil import start_recording, stop_recording
from src.misc.synctime import sync_time
from src.misc.updatewifipassword import update_wifi_password
from src.sdcard.sdcardutil import format_sd_card, get_sd_card_status

_OPERATIONS = flags.DEFINE_multi_enum(
    name='operations',
    default=None,
    required=True,
    enum_values=[
        'format-sd-card',
        'get-files',
        'get-sd-card-status',
        'purge-files',
        'start-recording',
        'stop-recording',
        'sync-time',
        'update-wifi-password',
    ],
    help='A list of operations to perform in sequence. '
    'Example: --operations=get-sd-card-status --operations=sync-files --operations=purge-files --operations=get-sd-card-status'
)

def app_run_main() -> None:
  app.run(main)

def main(_: list[str]) -> None:
  logging.get_absl_handler().use_absl_log_file()

  operation: str
  for operation in _OPERATIONS.value:
    dispatch_operation(operation)

def dispatch_operation(operation: str) -> None:
  match operation:
    case 'format-sd-card':
      format_sd_card()

    case 'get-files':
      for file_type in FileType.get_enabled_types():
        get_files(file_type)

    case 'get-sd-card-status':
      get_sd_card_status()

    case 'purge-files':
      for file_type in FileType.get_enabled_types():
        purge_files(file_type)

    case 'start-recording':
      start_recording()

    case 'stop-recording':
      stop_recording()

    case 'sync-time':
      sync_time()

    case 'update-wifi-password':
      update_wifi_password()

    case _:
      raise ValueError('unexpected operation')

if __name__ == '__main__':
  app_run_main()
