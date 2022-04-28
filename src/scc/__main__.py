import click
from . import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
def cli():
    """
    SCC (Software Catalog Creator)\n
    Automatically generates a searchable portal for every repository of an organization/s or user/s, which is easy to host.\n

    Usage:

    1. (fetch) Fetch all repos from the desired organization/s\n
    2. (extract) Extract all metadata for every repo\n
    3. (portal) Generate a searchable portal for all the retrieved data\n

    """
    pass 

@cli.command()
@click.option('--input','-i', required=True, help="Organization or user name", metavar='<name-or-path>')
@click.option('--output','-o', default="repos.csv", show_default=True, help="Output csv file", metavar='<path>')
@click.option('--org', 'repo_type', flag_value='orgs', default=True, show_default=True, help="Extracting from a organization")
@click.option('--user', 'repo_type', flag_value='users', default=False, show_default=True, help="Extracting from a user")
@click.option('--not_archived','-na', flag_value=True, default=False, show_default=True, help="Fetch only repos that are not archived")
def fetch(input, output, repo_type, not_archived):
    """Retreive all organization/s or user/s repositories"""
    from scc.commands import fetch_repositories
    print(not_archived)
    fetch_repositories.fetch(input, output, repo_type, not_archived)

@cli.command()
@click.option('--input','-i', required=True, help="Pointers to the repositories in csv format", metavar='<csv-repos>')
@click.option('--output','-o', default="repos-metadata", help="Dir where repositories metadata will be saved", metavar='<path>')
@click.option('--inspect4py','-i4p', is_flag=True, help="Use inspect4py to extract additional metadata from Python repositories")
def extract(input, output, inspect4py):
    """Fetch and save metadata from introduced repos"""
    from scc.commands import extract_metadata
    extract_metadata.fetch(input, output, inspect4py)

@cli.command()
@click.option('--input','-i', required=True, help="Dir repositories metadata in json format", metavar='<dir-json-metadata>')
@click.option('--output','-o', default="portal", show_default=True, help="Dir where Software Catalog Portal will be saved", metavar='<path>')
def portal(input, output):
    """Build a portal with a minimalistic desing"""
    from scc.commands.portal import portal
    portal.generate(input, output)

@cli.command()
@click.option('--input','-i', required=True, help="Repository URL", metavar='<url>')
@click.option('--output','-o', default="card", show_default=True, help="Output file where the html will be saved", metavar='<path>')
@click.option('--html', 'save_as', flag_value='html', default=True, show_default=True, help="Save card as html")
@click.option('--png', 'save_as', flag_value='png', default=False, show_default=True, help="Save card as a png")
def card(input, output, save_as):
    """Create a stand-alone card ready to be embedded in a website"""
    from scc.commands import single_card
    single_card.create(input, output, save_as)

