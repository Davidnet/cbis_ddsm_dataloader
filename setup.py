import argparse
import json
import os
import tarfile
from pathlib import Path

from utils.ddsm_downloader import CBISDDSMDownloader
from utils.ddsm_png_converter import CBISDDSMConverter
from utils.ddsm_preprocessor import CBISDDSMPreprocessor


def create_tar(folder_path, output_filename):
    with tarfile.open(output_filename, "w") as tar:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file.endswith(".png"):
                    continue
                    # Get the full path of the file
                full_path = os.path.join(root, file)
                # Add the file to the tar archive while preserving the directory structure
                tar.add(full_path, arcname=os.path.relpath(full_path, folder_path))


parser = argparse.ArgumentParser(
    prog="CBIS DDSM Setup",
    description="Welcome to CBIS DDSM Dataloader library.\n"
    "Setup includes: \n"
    "    1. downloading the database, \n"
    "    2. converting images to PNG \n"
    "    3. organizing lesion information for PyTorch dataset creation \n"
    "Please ensure that the information in 'config.json' file is correctly set and the files exist.\n"
    "This process will take a while.\n",
)
parser.add_argument(
    "-c",
    "--config_file",
    default="./config.json",
    help="Path to the configuration file. Default=config.json",
)
parser.add_argument(
    "-d",
    action="store_true",
    help="If used, dcm file will be deleted during conversion, to free up space."
    "However, if download runs again it will need to download the whole dataset again.",
)
parser.add_argument(
    "-o",
    "--output",
    default="./",
    help="Output path for the downloaded files. Default=./",
)
args = parser.parse_args()

print("Using configuration file: ", args.config_file)
print("Output path: ", args.output)

with open(args.config_file, "r") as cf:
    config = json.load(cf)

downloader = CBISDDSMDownloader(config["manifest"], config["download_path"])
downloader.start()
downloader.start()  # Run twice for checks

converter = CBISDDSMConverter(config["download_path"], delete_dcm=args.d)
converter.start()
converter.start()  # Run twice for checks

preprocessor = CBISDDSMPreprocessor(
    config["download_path"],
    (config["mass_train_csv"], config["calc_train_csv"]),
    (config["mass_test_csv"], config["calc_test_csv"]),
)
preprocessor.start()
Path(args.output).parent.mkdir(
    parents=True, exist_ok=True
)  # Create parent directory if it doesn't exist
create_tar(config["download_path"], args.output)
