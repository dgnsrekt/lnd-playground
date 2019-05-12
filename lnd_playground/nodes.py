from decouple import config
from paths import LND_CONFIG
from jinja2 import Template
from names import NAMES

LISTEN_PORT = config("LISTEN_PORT", cast=int)
RPC_LISTEN_PORT = config("RPC_LISTEN_PORT", cast=int)

ALIAS = config("NODE_ALIAS")
COLOR = config("NODE_COLOR")


with open(LND_CONFIG, "r") as file:
    template = Template(file.read())

for idx, name in enumerate(NAMES):
    listen = LISTEN_PORT + idx
    rpc_listen = RPC_LISTEN_PORT + idx
    debug_level = "info"
    alias = ALIAS + f"[{name.upper()}]"
    color = "#FF0000"

    print(
        template.render(
            listen=f"localhost:{9000 + idx}",
            rpc_listen=f"localhost:{10000 + idx}",
            debug_level="info",
            node_alias=alias,
            node_color=color,
        )
    )
    if idx > 3:
        break
