from modules.Helptransform.extensions import Helptransform_registry

# Import your transforms here
from transforms import getfavicon

if __name__ == "__main__":
    Helptransform_registry.write_local_mtz(command="./venv/bin/python3")
