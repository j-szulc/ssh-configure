import os
from pathlib import Path
import shutil
import click

from sshcfg import __version__

__author__ = "Jakub Szulc"
__copyright__ = "Jakub Szulc"
__license__ = "MIT"


def prepend_file(file_path, text):
    text_old = ""
    try:
        with open(file_path, "r") as f:
            text_old = f.read()
        shutil.move(file_path, file_path.with_suffix(".bak"))
    except FileNotFoundError:
        pass
    with open(file_path, "w+") as f:
        f.write(text + text_old)
    try:
        os.remove(file_path.with_suffix(".bak"))
    except FileNotFoundError:
        pass

@click.command()
@click.argument("USER_HOST", metavar="USER@HOST", nargs=1)
@click.argument("ALIAS", nargs=1)
def main(user_host, alias):
    """sshcfg - SSH config file generator"""
    user, host = user_host.split("@")
    config = f"""
    HOST {alias}
        HostName {host}
        User {user}
        Port 22
    """
    prepend_file(Path.home() / ".ssh" / "config", config)
    return 0


if __name__ == '__main__':
    main()
