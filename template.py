import csv
import html
import os
import subprocess

FIRST_NAME_PLACEHOLDER = 'XXFIRSTNAMEXX'
LAST_NAME_PLACEHOLDER = 'XXNAMEXX'
COMPANY_PLACEHOLDER = 'XXCOMPANYXX'
TWITTER_PLACEHOLDER = 'XXTWITTERXX'

COL_FIRST_NAME = 'first_name'
COL_LAST_NAME = 'last_name'
COL_COMPANY = 'company'
COL_TWITTER = 'twitter'


class Badge:
    def __init__(self, template: str):
        self.template = template

    def set_first_name(self, first_name):
        self.template = self.template.replace(FIRST_NAME_PLACEHOLDER, html.escape(first_name))

    def set_last_name(self, last_name):
        self.template = self.template.replace(LAST_NAME_PLACEHOLDER, html.escape(last_name))

    def set_company(self, company):
        self.template = self.template.replace(COMPANY_PLACEHOLDER, html.escape(company))

    def set_twitter(self, twitter):
        self.template = self.template.replace(TWITTER_PLACEHOLDER, html.escape(twitter))

    def to_pdf(self, svg_path: str, pdf_path: str, svg_output_dpi: int):
        out_file = open(svg_path, 'w')
        out_file.write(self.template)
        out_file.close()

        subprocess.run(['inkscape', svg_path, '--export-pdf=' + pdf_path,
                        '--export-dpi=' + str(svg_output_dpi)])


def make_badges(template_file: str, attendees_file: str, svg_output_dpi: int):
    print('Open template file.')
    with open(template_file) as template_file:
        template = template_file.read().replace('\n', '')

    print('Open attendee file.')
    with open(attendees_file, 'r') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=';')
        print('Begin row parsing.')
        for index, row in enumerate(reader):
            svg_path = 'output/attendee_' + str(index) + '.svg'
            pdf_path = 'output/attendee_' + str(index) + '.pdf'

            badge = Badge(template)
            badge.set_first_name(row[COL_FIRST_NAME])
            badge.set_last_name(row[COL_LAST_NAME])
            badge.set_company(row[COL_COMPANY])
            badge.set_twitter(row[COL_TWITTER])

            print()
            print('Creating PDF badge...')
            badge.to_pdf(svg_path, pdf_path, svg_output_dpi)


            # Cleanup
            os.remove(svg_path)
