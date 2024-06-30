import os


class Utils:
    BASE_PATH = os.path.dirname(__file__)
    RESOURCES_PATH = BASE_PATH + "\\src\\main\\resources"


if __name__ == "__main__":
    print(Utils.BASE_PATH)
