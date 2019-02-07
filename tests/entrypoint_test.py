import glob
import os
import shutil

from entrypoint import LAUNCHER_PATH, main
from launcher.launcher_entry import launcher


def test_install_bot():
    launcher(["-nw", "-u"])
    assert glob.glob("OctoBot*")


def test_install_launcher():
    shutil.rmtree(LAUNCHER_PATH)
    main()
    assert os.path.exists(LAUNCHER_PATH)
