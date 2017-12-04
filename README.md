# Devfest Badges

## Introduction
A small script that parses a list of attendees from a CSV, converts the attendee to a SVG badge, and outputs a PDF with a complete list of badges ready for printing.

## Requirements

* Python >= 3.x
* Inkscape
* Pdftk >= 2.x

#### Expected CSV structure

A semicolon separated list with no header

[first_name];[last_name];[company];[twitter_handle]

e.g.: Joe;Smith;Company;stwitter

## Usage

The script uses the samples/attendees.csv for attendee data. As well as samples/template.svg for the badges.
Both can be overridden, see optional arguments.

python3 badges.py [-h] [-a ATTENDEES] [-t TEMPLATE] [-d DPI]

**optional arguments:**

    -h, --help          
                        show this help message and exit
    -a ATTENDEES, --attendees ATTENDEES
                        attendee list to import data from. MUST ba a CSV.
    -t TEMPLATE, --template TEMPLATE
                        badge template file to be used. MUST be an SVG.
    -d DPI, --dpi DPI     
                        output DPI