import json


def ini_to_dict(file_path: str) -> dict:
    config_dict = {
        'version': 1,
        'disable_existing_loggers': False
    }

    with open(file_path, 'r') as ini_file:
        ini_config = ini_file.read().split('\n\n')

    for config in ini_config:
        config_elements = config.split('\n')

        config_name = config_elements[0]

        if len(config_name.split('_')) > 1:
            sub_dict = dict()

            for elem in config_elements[1:]:

                key_values = elem.split('=')

                if len(key_values) == 2:
                    key = key_values[0]

                    if key == 'handlers':
                        value = key_values[1].split(',')
                    else:
                        value = key_values[1]

                    sub_dict[key] = value

            config_name_elements = config_name.split('_')

            param_type = config_name_elements[0][1:]
            param_name = config_name_elements[1][:-1]

            if param_type == 'logger':

                if param_name == 'root':
                    config_dict['root'] = sub_dict
                else:
                    try:
                        config_dict['loggers'].update({param_name: sub_dict})
                    except KeyError:
                        config_dict['loggers'] = {param_name: sub_dict}

            elif param_type == 'handler':
                try:
                    config_dict['handlers'].update({param_name: sub_dict})
                except KeyError:
                    config_dict['handlers'] = {param_name: sub_dict}

            elif param_type == 'formatter':
                try:
                    config_dict['formatters'].update({param_name: sub_dict})
                except KeyError:
                    config_dict['formatters'] = {param_name: sub_dict}

    return config_dict


result = ini_to_dict('logging_conf.ini')
json_type = json.dumps(result, indent=4)
print(json_type)
