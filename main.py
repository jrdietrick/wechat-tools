import re
from adb_android import adb_android


class HostException(Exception):
    pass


class DeviceException(Exception):
    pass


def _shell_command(command):
    host_status_code, output = adb_android.shell('%s; echo $?' % command)
    if host_status_code != 0:
        raise HostException
    output = output.splitlines()
    device_status_code = int(output[-1])
    if device_status_code != 0:
        raise DeviceException
    return output[:-1]


def _su_shell_command(command):
    return _shell_command('su -c "%s"' % command)


wechat_user_directories_regex = re.compile('^[0-9A-Fa-f]{32}$')


def main():
    adb_android.wait_for_device()
    output = _su_shell_command('ls /data/data/com.tencent.mm/MicroMsg/')
    candidates = filter(lambda x: wechat_user_directories_regex.match(x) != None, output)
    found_dbs = []
    for candidate in candidates:
        full_db_path = '/data/data/com.tencent.mm/MicroMsg/%s/EnMicroMsg.db' % candidate
        try:
            _su_shell_command('ls %s' % full_db_path)
        except DeviceException:
            continue
        found_dbs.append(full_db_path)
    for db in found_dbs:
        print db


if __name__ == '__main__':
    main()
