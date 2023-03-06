#this file is to create the config.ini file that will be used in upload.py
#TODO discuss
from configparser import ConfigParser
import os
from pathlib import Path
import sys

path = Path(__file__).parent.absolute()

def create_config():
    config = ConfigParser()
    config.add_section("INFLUX_SETTINGS")


    return


def get_config():
    """Function that retrieves the configuration file
    Returns
    -------
    config object
    """
    #TODO ask if this is the correct file path I should be using
    config_obj = ConfigParser()
    config_file = Path(
        os.getenv("SOCA_CONFIGURATION_FILE",'~/.soca/config.ini')
    ).expanduser()
    if config_file.exists():
        config_obj.read(config_file)
        print('success')

    else:
        print('ya yeet')
        raise Exception("Error: Please provide a config.json file or run SOCA configure.")
        #sys.exit("Error: Please provide a config.json file or run somef configure.")

    return config_obj

def create_config(url,bucket,token,org):
    """Function that creates the configuration file
    Returns
    -------
    configParser object
    """
    config = ConfigParser()
    config.add_section('DATABASE')
    config.set('DATABASE','host',url)
    config.set('DATABASE','token',token)
    config.set('DATABASE','bucket',bucket)
    config.set('DATABASE', 'org', org)
    #TODO look into adding option to soca -Upload
    #config.set('DATABASE',org,)
    #config.set('DATABASE',measurement)

    home = str(Path("~").expanduser())
    if not os.path.isdir(home+"/.soca"):
        try:
            os.mkdir(home+"/.soca", mode=0o777)
        except Exception as e:
            print(str(e))
            print("Creation of the directory %s failed" % path)
    path_file = Path(os.getenv("SOCA_CONFIGURATION_FILE", '~/.soca/config.ini')).expanduser()
    with open(path_file, 'w+') as configfile:
        config.write(configfile)

