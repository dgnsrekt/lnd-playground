from paths import NODE_PATH, MASTER_NODE_PATH, MASTER_NODE_LNDDIR_PATH, LND_PATH, LNCLI_PATH
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
try:
    for line in iter(proc.stdout.readline, ""):
        log.debug(clean_line(line))
        if LOGLEVEL > 10:
            print(".", end="", flush=True)
        if SYNCED_LOG_LINE in str(line):
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
