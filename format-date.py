import csv
import io
import os

import glob

def format_date(input_filename, output_filename):
    print(input_filename)
    with io.open(input_filename, "r", encoding='utf-8', errors="surrogateescape") as csvfile:
        rows = [row for row in csv.reader(csvfile)]

    # first 3 rows are metadata
    dates =[row[0].split('/') for row in rows[3:]]
    new_date = ['{:0>4}/{:0>2}/{:0>2}'.format(date[2][:4],date[0],date[1]) for date in dates]
    for i in range(len(new_date)):
        rows[i + 3][0] = new_date[i]
    # print(rows)
    try:
        with io.open(output_filename, 'x', encoding='utf-8',newline='', errors="surrogateescape") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows) 
    except FileExistsError:
        print(output_filename + " already exists.")
  

def main():
    input_files = glob.glob(os.getcwd() + "/**/*.csv") + (glob.glob(os.getcwd() + "/*.csv"))
    output_files = [output_file.split(".csv")[0] + "-reformatted.csv" for output_file in input_files]
    print(output_files)
    for input_file, output_file in zip(input_files, output_files):
        format_date(input_file, output_file)

if __name__ == '__main__':
    main()