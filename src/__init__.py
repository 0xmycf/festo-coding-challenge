# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
import os, glob

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
del os, glob
