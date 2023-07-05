import logging

logging.basicConfig()
# root_logger = logging.getLogger()

module_logger = logging.getLogger("module_logger")
module_logger.propagate = False

custom_handler = logging.StreamHandler()
module_logger.addHandler(custom_handler)
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(message)s")
custom_handler.setFormatter(formatter)

submodule_logger = logging.getLogger("module_logger.submodule_logger")
submodule_logger.setLevel("DEBUG")


def main():
    submodule_logger.debug("Hi there!")


if __name__ == '__main__':
    main()
