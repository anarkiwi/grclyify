#!/usr/bin/python3
import os
import subprocess
import unittest


class GrClyifyTestCase(unittest.TestCase):
    def test_grclyify(self):
        test_src_dir = os.path.dirname(os.path.abspath(__file__))
        test_fg_grc = os.path.join(test_src_dir, "test_flow.grc")
        grclify = os.path.join(test_src_dir, "../grclyify.py")
        subprocess.check_call(["grcc", test_fg_grc, "-o", os.path.dirname(test_fg_grc)])
        test_fg_py = test_fg_grc.replace(".grc", ".py")
        subprocess.check_call([grclify, test_fg_py, "--help"])
        subprocess.check_call(
            [grclify, test_fg_py, "--set_samp_rate", "64000", "--runtime", "10"]
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
