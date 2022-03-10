import click

@click.group()
def cli():
    """
    SCC (Software Catalog Creator)\n
    Automatically generates a searchable portal for every repsitory of an organization/s, which is easy to host.\n

    Steps:

    1. (Command repos) Fetch all repos from the desired organization/s.\n
    2. (Command extract) Extract all metadata for every repo.\n
    3. (Command portal) Generate a searchable portal for all the retreived data.\n

    """
    pass 

@cli.command()
@click.option('--input','-i', required=True, help="Organization name or file with a list of organizations. Use '\/n' as separator.")
@click.option('--output','-o', default="repos.csv", help="Output data will be stored in a new csv file.")
def orgrepos(input, output):
    """Retreive all organization/s repositories."""
    from scc.commands import fetch_repositories_organization
    fetch_repositories_organization.fetch(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="User name or file with a list of users. Use '\/n' as separator.")
@click.option('--output','-o', default="repos.csv", help="Output data will be stored in a new csv file.")
def usrrepos(input, output):
    """Retreive all user/s repositories."""
    from scc.commands import fetch_repositories_user
    fetch_repositories_user.fetch(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="All the pointers to the repositories of the organization/s in csv format.")
@click.option('--output','-o', default="repos-metadata", help="Output dir where repositories metadata will be saved.")
def extract(input, output):
    """Execute  SOMEF for  every  repo introduced."""
    from scc.commands import extract_metadata
    extract_metadata.fetch(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="Respositories metadata representation in json format.")
@click.option('--output','-o', default="portal", help="Outout dir where the Software Catalog Portal will be saved.")
def portal(input, output):
    """Build  a  portal  with a  minimalistic desing."""
    from scc.commands.software_catalog_portal import portal
    portal.generate(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="Respository URL")
@click.option('--output','-o', default="card", help="Outout file where the card will be saved.")
def card(input, output):
    """Create a single ready to use card with the css embedded."""
    from scc.commands import single_card
    single_card.create(input, output)

#if __name__ == "__main__":
#    cli()