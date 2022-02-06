import sys
import os

# Silent errors
old_stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
global bibtext
from ply_bibtex_parser import parser as bibtext
sys.stderr = old_stderr

