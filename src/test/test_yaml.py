import yaml
from my_utils import Utils
import os

path = os.path.join(Utils.RESOURCES_PATH, "config.yaml")

with open(path, 'r', encoding="utf-8") as file:
    data = yaml.safe_load(file)

