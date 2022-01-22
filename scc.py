import click
from commands import organization_repositories, repositories_metadata, software_catalog_portal

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
@click.option('--input','-i', required=True, help="Organization name or file with a list of organizations. Use '\/n' as separator.")
@click.option('--output','-o', default="repos.csv", help="Output data will be stored in a new csv file.")
def repos(input, output):
    """Retreive all organization/s repositories."""
    organization_repositories.fetch(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="All the pointers to the repositories of the organization/s in csv format.")
@click.option('--output','-o', default="repos-metadata.json", help="Output data will be stored in a new json file.")
def extract(input, output):
    """Execute  SOMEF for  every  repo introduced."""
    repositories_metadata.fetch(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="Respositories metadata representation in json format.")
@click.option('--output','-o', default="portal", help="Outout dir where the Software Catalog Portal will be saved.")
def portal(input, output):
    """Build  a  portal  with a  minimalistic desing."""
    software_catalog_portal.generate(input, output)

if __name__ == "__main__":
    cli()