import csv
import os
import subprocess
import sys

from argparse import ArgumentParser

FIRST_NAME_PLACEHOLDER = 'XXFIRSTNAMEXX'
LAST_NAME_PLACEHOLDER = 'XXNAMEXX'
COMPANY_PLACEHOLDER = 'XXCOMPANYXX'
TWITTER_PLACEHOLDER = 'XXTWITTERXX'

FIRST_NAME_INDEX = 0
LAST_NAME_INDEX = 1
COMPANY_INDEX = 4
TWITTER_INDEX = 7

print(sys.argv)

# Setup argument parser
parser = ArgumentParser(description='Create Attendee badges for Devfest')

parser.add_argument('-a', '--attendees', dest='attendees', type=str, nargs=1, default='sample/attendees.csv',
                    help='attendee list to import data from. MUST ba a CSV. See additional documentation for '
                         'required structure')
parser.add_argument('-t', '--template', dest='template', type=str, nargs=1, default='sample/template.svg',
                    help='badge template file to be used. MUST be an SVG.')

args = parser.parse_args()

# Input files
attendees = args.attendees
template = args.template


os.makedirs(os.path.dirname('output/'), exist_ok=True)

with open(template) as template_file:
    template = template_file.read().replace('\n', '')

with open(attendees) as csvFile:
    reader = csv.reader(csvFile, delimiter=';')
    for index, row in enumerate(reader):
        # Copy template since we need to replace placeholder text
        template_copy = template

        # Get relevant data from CSV
        first_name = row[FIRST_NAME_INDEX]
        last_name = row[LAST_NAME_INDEX]
        company = row[COMPANY_INDEX] if row[COMPANY_INDEX] != '-' else ''
        twitter = row[TWITTER_INDEX] if row[TWITTER_INDEX] != '-' else ''

        # Replace placeholders with actual data
        template_copy = template_copy.replace(FIRST_NAME_PLACEHOLDER, first_name)
        template_copy = template_copy.replace(LAST_NAME_PLACEHOLDER, last_name)
        template_copy = template_copy.replace(COMPANY_PLACEHOLDER, company)
        template_copy = template_copy.replace(TWITTER_PLACEHOLDER, twitter)

        # Write out copy of template to file
        out_filename = 'output/attendee_' + str(index) + '.svg'
        out_file = open(out_filename, 'w')
        out_file.write(template_copy)
        out_file.close()

        # Convert SVG to PDF using Inkscape
        subprocess.run(['inkscape', out_filename, '--export-pdf=output/attendee_' + str(index) + '.pdf',
                        '--export-dpi=300'])


sys.exit(1)
