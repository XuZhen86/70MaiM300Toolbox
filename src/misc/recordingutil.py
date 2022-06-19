from src.http import httputil


def start_recording() -> None:
  httputil.get_result('setaccessalbum.cgi', {'enable': 1})


def stop_recording() -> None:
  httputil.get_result('setaccessalbum.cgi', {'enable': 0})


# record.cgi doesn't work for M300.
# httputil.get_result('record.cgi', {'cmd': 'start' if is_recording else 'stop'})
