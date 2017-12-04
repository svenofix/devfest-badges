import html.parser
import csv
import os
import subprocess
import sys

from argparse import ArgumentParser
from glob import glob

# "Constants"
FIRST_NAME_PLACEHOLDER = 'XXFIRSTNAMEXX'
LAST_NAME_PLACEHOLDER = 'XXNAMEXX'
COMPANY_PLACEHOLDER = 'XXCOMPANYXX'
TWITTER_PLACEHOLDER = 'XXTWITTERXX'

FIRST_NAME_INDEX = 0
LAST_NAME_INDEX = 1
COMPANY_INDEX = 2
TWITTER_INDEX = 3

DEFAULT_DPI = 300

# Argument parser
parser = ArgumentParser(description='Create Attendee badges for Devfest')

parser.add_argument('-a', '--attendees', dest='attendees', type=str, nargs=1, default='sample/attendees.csv',
                    help='attendee list to import data from. MUST ba a CSV.')
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

print('Open template file.')
with open(template) as template_file:
    template = template_file.read().replace('\n', '')

print('Open attendee file.')
with open(attendees, 'r') as csvFile:
    reader = csv.reader(csvFile, delimiter=';')
    print('Begin row parsing.')
    for index, row in enumerate(reader):
        print()
        print('Begin badge #' + str(index + 1))

        # Copy template since we need to replace placeholder text
        template_copy = template

        # Get relevant data from CSV
        first_name = html.escape(row[FIRST_NAME_INDEX])
        last_name = html.escape(row[LAST_NAME_INDEX])
        company = html.escape(row[COMPANY_INDEX]) if row[COMPANY_INDEX] != '-' else ''
        twitter = html.escape(row[TWITTER_INDEX]) if row[TWITTER_INDEX] != '-' else ''

        # Replace placeholders with actual data
        template_copy = template_copy.replace(FIRST_NAME_PLACEHOLDER, first_name)
        template_copy = template_copy.replace(LAST_NAME_PLACEHOLDER, last_name)
        template_copy = template_copy.replace(COMPANY_PLACEHOLDER, company)
        template_copy = template_copy.replace(TWITTER_PLACEHOLDER, twitter)

        # Write out copy of template to file
        print('Creating SVG badge...')
        out_filename = 'output/attendee_' + str(index) + '.svg'
        out_file = open(out_filename, 'w')
        out_file.write(template_copy)
        out_file.close()

        # Convert SVG to PDF using Inkscape
        print('Converting SVG to PDF...')
        subprocess.run(['inkscape', out_filename, '--export-pdf=output/attendee_' + str(index) + '.pdf',
                        '--export-dpi=' + str(dpi)])

        # Cleanup
        os.remove(out_filename)

# Merge PDF files
pdf_files = glob('./output/attendee_*.pdf')
pdf_files.sort()

pdftk_args = ['pdftk', 'cat', 'output', './output/merged.pdf']
# Insert list of pdf files after 'pdftk' command
pdftk_args[1:1] = pdf_files

subprocess.run(pdftk_args)

# Cleanup
for file in pdf_files:
    os.remove(file)

print()
print('All done!')
sys.exit(1)
