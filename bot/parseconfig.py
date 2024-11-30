from collections import defaultdict
from configparser import ConfigParser
from typing import Any, Dict


class ConfigError(Exception):
    pass


def parse_config(config_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Function parses configuration file.
    :param config_path: path to configuration file.
    :return: data from configuration file.
    """

    config_structure = {"GENERAL": [{"option": "token",
                                     "type": str}]}

    config_parser = ConfigParser()
    config_parser.read(config_path)

    missed_sections = [f"'{section}'" for section in config_structure if not config_parser.has_section(section)]
    if len(missed_sections) == 1:
        raise ConfigError(f"Config file '{config_path}' has no section {missed_sections[0]}")

    if len(missed_sections) > 1:
        raise ConfigError(f"Config file '{config_path}' has no sections {', '.join(missed_sections)}")

    data = defaultdict(dict)
    for section, options in config_structure.items():
        data[section] = {}
        for option in options:
            option_name = option["option"]
            if not config_parser.has_option(section, option_name):
                if "default" not in option:
                    raise ConfigError(f"Config file '{config_path}' has no option '{option_name}' in section "
                                      f"'{section}'")
                data[section][option_name] = option["default"]
            else:
                convert_func = option.get("type", str)
                try:
                    data[section][option_name] = convert_func(config_parser.get(section, option_name))
                except ValueError as exc:
                    exc_info = f" ({exc})" if str(exc) else ""
                    raise ConfigError(f"Invalid value of option '{option_name}' in section '{section}'{exc_info}") \
                        from exc
    return data
