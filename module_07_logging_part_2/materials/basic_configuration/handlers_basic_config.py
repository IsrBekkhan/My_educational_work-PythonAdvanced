import logging

logging.basicConfig()
root_logger = logging.getLogger()
module_logger = logging.getLogger("module_logger")
submodule_logger = logging.getLogger("module_logger.submodule_logger")
submodule_logger.setLevel("DEBUG")


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
