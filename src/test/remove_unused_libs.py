import subprocess

from my_utils import Utils
import os


def read_packages(file_path):
    packages = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            packages = set(line.strip().split('==')[0] for line in file if line.strip())
    return packages


requirements_path = os.path.join(Utils.BASE_PATH, 'requirements.txt')
installed_path = os.path.join(Utils.BASE_PATH, 'installed.txt')

required_packages = read_packages(requirements_path)
installed_packages = read_packages(installed_path)

unused_packages = installed_packages - required_packages

for package in unused_packages:
    subprocess.run(['pip', 'uninstall', '-y', package])
    print(f"删除成功: {package}")
