import configparser
from gui_controller import main


def main_controller():

    config = configparser.ConfigParser()
    config.read("config.ini")
    main(config)


if __name__ == "__main__":
    main_controller()