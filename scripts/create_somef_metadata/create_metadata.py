import csv
import click

from somef.cli import cli_get_data

__version__ = "0.0.1"

@click.command()
@click.version_option(__version__)
@click.option('-i', '--in_path', type=str, required=True, help='Input of the CSV with repository names to process')
@click.option('-o', '--out_path', type=str, default='out', help='output folder path. Default is out')
def create_metadata(in_path, out_path):
    with open(out_path, 'w') as file_out:
        with open(in_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print(row)
                # TO DO: Invoke somef cli here.

if __name__ == '__main__':
    create_metadata()
