from paths import (
    NODE_PATH,
    LND_PATH,
    LNCLI_PATH,
    MASTER_NODE_PATH,
    MASTER_NODE_LNDDIR_PATH,
    MASTER_NODE_LND_DATAGRAPH,
    MASTER_NODE_LND_LOGS,
    MASTER_NODE_TLS_CERT,
    MASTER_NODE_TLS_KEY,
)
import shutil
import subprocess
from time import sleep

import logme

log = logme.log(scope="module", name="node_sync")
LOGLEVEL = log.logger.master_level

lnd_cmd = [
    f"{LND_PATH}",
    "--bitcoin.active",
    "--bitcoin.testnet",
    "--bitcoin.node=neutrino",
    "--neutrino.connect=faucet.lightning.community",
    f"--lnddir={MASTER_NODE_LNDDIR_PATH}",
]

print("removing master node")
shutil.rmtree(MASTER_NODE_LNDDIR_PATH, ignore_errors=True)


def clean_line(line):
    lines = str(line).split(" ")
    cleaned = " ".join(lines[2:])
    return cleaned


proc = subprocess.Popen(lnd_cmd, stdout=subprocess.PIPE)

SYNCED_LOG_LINE = "Fully caught up with cfheaders at"
log.info("Syncing Main Node...")
# while True:
#     proc.poll()
#     line = str(proc.stdout.readline())
#     print(line)
#     print("errors:", proc.errors)
#     print("returncode:", proc.returncode)
#     if SYNCED_LOG_LINE in line:
#         proc.terminate()
#         break
try:
    for line in iter(proc.stdout.readline, ""):
        log.debug(clean_line(line))
        if LOGLEVEL > 10:
            print(".", end="", flush=True)
        if SYNCED_LOG_LINE in str(line):
            print()
            log.info("node appears fully synced. shutting down...")
            sleep(5)
            proc.terminate()
            proc.kill()
            break
    print()
except (KeyboardInterrupt, SystemExit):
    print("\nexiting removing master node")
    shutil.rmtree(MASTER_NODE_LNDDIR_PATH, ignore_errors=True)
    raise

paths_to_remove = [MASTER_NODE_LND_DATAGRAPH, MASTER_NODE_LND_LOGS]
for path in paths_to_remove:
    if path.exists():
        log.debug(f"removing {path}")
        shutil.rmtree(path, ignore_errors=True)

files_to_remove = [MASTER_NODE_TLS_KEY, MASTER_NODE_TLS_CERT]
for file in files_to_remove:
    if file.exists():
        log.debug(f"removing {file}")
        file.unlink()
