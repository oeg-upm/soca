import click

@click.group()
def cli():
    """
    SCC (Software Catalog Creator)\n
    Automatically generates a searchable portal for every repsitory of an organization/s, which is easy to host.\n

    Steps:

    1. (Command repos) Fetch all the repos from the desired organization/s.\n
    2. (Command extract) Extract all the metadata for every repo.\n
    3. (Command portal) Generate a searchable portal for all the retreived data.\n
    """
    pass

@cli.command()
@click.option('--input','-i', required=True, help="Url of organization or file name of list of organizations. Use '\/n' as separator.")
@click.option('--output','-o', default="repos.csv", help="Output data will be stored in a new csv file.")
def repos(input, output):
    """Retreive all organization/s repositories."""
    print("Work in progress...")

@cli.command()
@click.option('--input','-i', required=True, help="All the pointers to the repositories of the organization/s in csv format.")
@click.option('--output','-o', default="repos-metadata.json", help="Output data will be stored in a new json file.")
def extract(input, output):
    """Execute  SOMEF for  every  repo introduced."""
    print("Work in progress...")

@cli.command()
@click.option('--input','-i', required=True, help="Respositories metadata representation in json format.")
@click.option('--output','-o', default="portal", help="Directory with all the portal/web files.")
def portal(input, output):
    """Build  a  portal  with a  minimalistic desing."""
    print("Work in progress...")

if __name__ == "__main__":
    cli()