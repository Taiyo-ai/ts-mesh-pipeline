import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


with open("requirements.txt") as f:
    lines = f.readlines()

packages = []
for line in lines:
    packages = line.strip()

if __name__ == "__main__":
    install(packages)
