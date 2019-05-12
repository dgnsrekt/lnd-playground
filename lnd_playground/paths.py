from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
BIN_PATH = ROOT_PATH / "bin"
NODE_PATH = ROOT_PATH / "nodes"

DOWNLOAD_URL = "https://github.com/lightningnetwork/lnd/releases/download/v0.6.1-beta/lnd-linux-amd64-v0.6.1-beta.tar.gz"

DOWNLOAD_FILENAME = DOWNLOAD_URL.split("/")[-1]
LIGHTNING_NETWORK_DAEMON_VERSION = DOWNLOAD_URL.split("/")[-2]

DOWNLOAD_FILE_PATH = ROOT_PATH / DOWNLOAD_FILENAME
EXTRACTED_FOLDER_PATH = ROOT_PATH / DOWNLOAD_FILENAME.replace(".tar.gz", "")

LND_PATH = BIN_PATH / "lnd"
LNCLI_PATH = BIN_PATH / "lncli"

# LND_CONFIG = ROOT_PATH / "lnd.conf"


def check_paths_status():
    """Shows the status of all the above paths."""
    global_variables = globals().copy()

    for key, value in global_variables.items():
        if isinstance(value, Path):
            print(key, value, value.exists(), type(value))

        elif isinstance(value, str):
            print(key, value, type(value))


if __name__ == "__main__":
    check_paths_status()
