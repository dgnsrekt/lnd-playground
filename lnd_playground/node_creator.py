import luigi
import logme
import shutil
from paths import NODE_PATH, MASTER_NODE_PATH
import errno
from names import NAMES
from time import sleep


def copy(src, dest):
    src = str(src)
    dest = str(dest)
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print("Directory not copied. Error: %s" % e)


for folder in list(NODE_PATH.glob("*")):
    if folder != MASTER_NODE_PATH:
        shutil.rmtree(str(folder))

sleep(10)

number_of_nodes = 4

for idx, name in enumerate(NAMES):
    node_location = NODE_PATH / name
    print("created:", node_location)
    assert MASTER_NODE_PATH.exists(), "missing"
    assert not node_location.exists(), "already exists"

    copy(MASTER_NODE_PATH, node_location)
    if idx >= number_of_nodes:
        break
