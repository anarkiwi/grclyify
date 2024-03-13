#!/usr/bin/python3

import argparse
import importlib
import inspect
import sys
from gnuradio import gr

if not len(sys.argv) > 1:
    print("need name of flow graph python module")
    raise ValueError

fg_file = sys.argv[1]
fg_file = fg_file.replace(".py", "")
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
for set_method in set_methods:
    parser.add_argument(
        f"--{set_method}",
        dest=set_method,
    )
options = {
    option: val
    for option, val in vars(parser.parse_args()).items()
    if option.startswith("set_") and val is not None
}


class fgsub(fg_class):
    OPTIONS = options

    def start(self):
        for option, value in self.OPTIONS.items():
            option_name = option.replace("set_", "")
            option_type = type(getattr(self, option_name))
            print(f"overriding {option_name} to {value}")
            getattr(self, option)(option_type(value))
        super().start()


fg_module.main(fgsub)
