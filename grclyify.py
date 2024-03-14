#!/usr/bin/python3

import argparse
import importlib
import inspect
import os
import signal
import sys
import threading
import time
from gnuradio import gr

if not len(sys.argv) > 1:
    print("need name of flow graph python module")
    raise ValueError

fg_file = os.path.realpath(sys.argv[1])
fg_file = fg_file.replace(".py", "")
fg_dir = os.path.dirname(fg_file)
fg_file = os.path.basename(fg_file)
sys.path.append(fg_dir)
fg_module = importlib.import_module(fg_file)
fg_class = None
for o in vars(fg_module):
    try:
        if issubclass(getattr(fg_module, o), gr.top_block):
            fg_class = o
            break
    except TypeError:
        continue

if fg_class is None:
    print("flow graph module not found (no gr.top_block)")
    raise ValueError

fg_class = getattr(fg_module, fg_class)
set_methods = [
    method[0] for method in inspect.getmembers(fg_class) if method[0].startswith("set_")
]
parser = argparse.ArgumentParser()
parser.add_argument(
    "fg_file", type=str, default=None, help="Path to flow graph python file"
)
parser.add_argument(
    "--runtime", type=float, default=None, help="Runtime limit, in seconds"
)
for set_method in set_methods:
    parser.add_argument(
        f"--{set_method}",
        dest=set_method,
    )
options = parser.parse_args()
set_options = {
    option: val
    for option, val in vars(options).items()
    if option.startswith("set_") and val is not None
}


class fgsub(fg_class):
    OPTIONS = set_options

    def limit_runtime(self, runtime):
        print(f"will exit in {runtime}s")
        time.sleep(runtime)
        print("exiting")
        os.kill(os.getpid(), signal.SIGTERM)

    def start(self):
        for option, value in self.OPTIONS.items():
            option_name = option.replace("set_", "")
            option_type = type(getattr(self, option_name))
            print(f"overriding {option_name} to {value}")
            getattr(self, option)(option_type(value))
        if options.runtime is not None:
            self.limit_thread = threading.Thread(
                target=self.limit_runtime, args=(options.runtime,)
            )
            self.limit_thread.start()
        super().start()


fg_module.main(fgsub)
