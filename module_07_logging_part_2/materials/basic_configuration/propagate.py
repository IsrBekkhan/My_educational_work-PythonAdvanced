import logging

logging.basicConfig()
root_logger = logging.getLogger()
module_logger = logging.getLogger("module_logger")

submodule_logger = logging.getLogger("module_logger.submodule_logger")
submodule_logger.setLevel("DEBUG")
submodule_logger.propagate = True

def main():


    submodule_logger.debug("Hi there!")


if __name__ == '__main__':
    main()
