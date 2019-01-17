#!/usr/bin/env python
import click
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import requests
import re
import csv
'''
date: 10/09/2018, 26/09/2018
vers: 1.1
name: Daniel Lee
desc: returns a csv of water flow data to be fed into IFAS
        and graphed
build: pyinstaller --onefile convert.py
'''

VERSION = 1.1


class FlowData(object):
    def __init__(self, title, outfile, date_range=None, url=None, infile=None):
        self.title = title
        self.date_range = date_range
        if infile:
            self.infile = infile
            self.raw_data = self.data_read()
        if url:
            self.url = url
            self.raw_data = self.get_html()
        self.outfile = outfile
        self.data = ''.join([self.row_process(row) for row in self.raw_data])
        self.header = self.make_header()

    def __repr__(self):
        return "dataseries:\t{}\ndaterange:\t{}\ntargeturl:\t{}\noutfile:\t{}".format(self.title, self.date_range, self.url, self.outfile)

    def get_html(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table_data = []
        table_body = soup.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [ele.text.strip() for ele in cols]
            table_data.append([ele for ele in cols if ele]
                              )  # Get rid of empty values
        if self.date_range is not None:
            return table_data[1+self.date_range[0]:2+self.date_range[1]]
        else:
            return table_data[2:]

    def data_read(self):
        with open(self.infile) as csvfile:
            rows = [row for row in csv.reader(csvfile)]
        return rows

    def make_header(self):
        return 'TITLE,{}\nDATA,\n'.format(self.title)

    def row_process(self, row):
        rowdata = ''
        p = re.compile(r'(?P<year>\d{4})\/(?P<month>\d{2})\/(?P<day>\d{2})')
        m = p.search(row[0])
        if m:
            date = ''.join(m.group('year', 'month', 'day'))
            hour = 1
            for data in row[1:]:
                if data == "欠測" or data == "閉局":
                    data = "-1.00"
                rowdata += date + '{:02}'.format(hour) + '00,' + data + '\n'
                hour += 1
            return rowdata
        else:
            return ''

    def output(self):
        with open(self.outfile, 'w') as text_file:
            text_file.write(self.header + self.data)
        return self.header + self.data


@click.command()
@click.option('--name', '-n', default='ObservationData',
              help='Set a name for the data series. Default is "ObservationData"')
@click.option('--date_range', '-d', nargs=2, type=click.IntRange(1, 31), default=(1, 31),
              help='Choose a day range for data series. Default is all dates in the month')
@click.argument('target_url', type=click.STRING)
@click.argument('output_filename')
def main(name, date_range, target_url, output_filename):
    """
    This program retrieves data from http://www1.river.go.jp/ 
    and converts it into a csv file that IFAS can read.
    \n
    TARGET_URL is the url of the raindata you wish to process.
    \n
    The OUTPUT_FILENAME is the filename of the csv that will be created.
    \n
    Version 1.1
    """
    
    rain = FlowData(title=name,
                    date_range=date_range,
                    url=target_url,
                    outfile=output_filename)
    rain.output()
    print(rain)


def test(target_url):
    rain = FlowData(title='RealData',
                    url=target_url,
                    outfile='outtest.csv')
    rain.output()


if __name__ == '__main__':
    # test(target_url = 'http://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=6&ID=309121289918020&BGNDATE=20161201&ENDDATE=20161231&KAWABOU=NO')
    main()
