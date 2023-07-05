import logging


root_logger = logging.getLogger()
logging.basicConfig()

module_logger = logging.getLogger('module_logger')
module_logger.propagate = False

submodule_logger = logging.getLogger('module_logger.submodule_logger')
submodule_logger.setLevel('DEBUG')
submodule_logger.propagate = True

custom_handler = logging.StreamHandler()
module_logger.addHandler(custom_handler)
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(message)s")
custom_handler.setFormatter(formatter)

file_handler = logging.FileHandler('applog.log', mode='a')
file_handler.setFormatter(formatter)
module_logger.addHandler(file_handler)


def main():
    print("Root logger:")
    print(root_logger.handlers)

    print("Submodule logger:")
    print(submodule_logger.handlers)

    print("Module logger:")
    print(module_logger.handlers)

    submodule_logger.debug("Hi there!")


if __name__ == '__main__':
    main()
