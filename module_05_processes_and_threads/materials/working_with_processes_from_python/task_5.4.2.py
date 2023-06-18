import subprocess
import shlex
import json


def get_request():
    command_str = 'curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json'
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True)

    result_text = result.stdout.decode()
    result_list = result_text.splitlines()
    main_result = json.loads(result_list[-1])

    return main_result['ip']


if __name__ == '__main__':
    ip = get_request()
    print('IP -', ip)