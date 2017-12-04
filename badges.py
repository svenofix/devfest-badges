import glob
import os
import subprocess
import sys

from argparse import ArgumentParser
from template import make_badges

DEFAULT_DPI = 300

# Setup argument parser
parser = ArgumentParser(description='Create Attendee badges for Devfest')

parser.add_argument('-a', '--attendees', dest='attendees', type=str, nargs=1, default='sample/attendees.csv',
                    help='attendee list to import data from. MUST ba a CSV. See additional documentation for '
                         'required structure')
parser.add_argument('-t', '--template', dest='template', type=str, nargs=1, default='sample/template.svg',
                    help='badge template file to be used. MUST be an SVG.')
parser.add_argument('-d', '--dpi', dest='dpi', type=int, nargs=1, default=DEFAULT_DPI,
                    help='output DPI')

args = parser.parse_args()

# Input files
attendees = args.attendees
template = args.template
dpi = args.dpi

print('Creating output dir.')
os.makedirs(os.path.dirname('output/'), exist_ok=True)

make_badges(template, attendees, dpi)

# Get list of PDF files
pdf_files = glob.glob('./output/attendee_*.pdf')
pdf_files.sort()

pdftk_args = ['pdftk', 'cat', 'output', './output/merged.pdf']
# Insert list of PDF files as direct arguments for pdftk instead of using regex (eg: *.pdf)
pdftk_args[1:1] = pdf_files

subprocess.run(pdftk_args)

# Cleanup
for file in pdf_files:
    os.remove(file)

print()
print('All done!')
sys.exit(1)
