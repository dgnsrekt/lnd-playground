from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
BIN_PATH = ROOT_PATH / "bin"
NODE_PATH = ROOT_PATH / "nodes"


LND_URL = "https://github.com/lightningnetwork/lnd/releases/download/v0.6.1-beta/lnd-linux-amd64-v0.6.1-beta.tar.gz"
LND_ZIP_FILENAME = LND_URL.split("/")[-1]
LND_VERSION = LND_URL.split("/")[-2]
LND_EXTRACTED_PATH = BIN_PATH / LND_ZIP_FILENAME.replace(".tar.gz", "")

LND_PATH = LND_EXTRACTED_PATH / "lnd"
LNCLI_PATH = LND_EXTRACTED_PATH / "lncli"

LND_CONFIG = ROOT_PATH / "lnd.conf"

# print(ROOT_PATH, ROOT_PATH.exists())
# print(BIN_PATH, BIN_PATH.exists())
# print(NODE_PATH, NODE_PATH.exists())
#
# print(LND_URL)
# print(LND_ZIP_FILENAME)
# print(LND_VERSION)
# print(LND_EXTRACTED_PATH, LND_EXTRACTED_PATH.exists())
#
# print(LND_PATH, LND_PATH.exists())
# print(LNCLI_PATH, LNCLI_PATH.exists())
