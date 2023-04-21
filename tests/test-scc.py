import unittest
from unittest import TestCase, mock
import json
from pathlib import Path
from datetime import datetime

import soca.commands.portal.metadata as md
#from ..src.soca.commands.portal.metadata import metadata as m
import soca.commands.extract_metadata as ex






path4 = Path(__file__).parent / "json_files"  / "ver8.json"
with path4.open() as f:
    ver8 = json.load(f)
f.close()
ver8 = md.metadata(path4, ver8)
######





class test_soca(TestCase):
    pass

class test_extract_metadata_py(TestCase):
    pass
    #def test_general(self):
    #    csv = Path(__file__).parent / "csv_files" / "repos.csv"
    #    ex.extract(str(csv),"repos-metadata", True, False)
class test_metadata_py(TestCase):
    def test_License(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        pass
    #TODO
    def test_noLicense(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.license())
        pass
    def test_lastUpdate_type(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        self.assertTrue(isinstance(meta.last_update(),datetime))
    def test_lastUpdate_equals(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        date_json = data['date_updated'][0]['result']['value'][:-1]
        test_date= datetime.strptime(date_json, '%Y-%m-%dT%H:%M:%S')
        self.assertEqual(test_date,meta.last_update())
    def test_updateDays(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        #for the WIDOCO json the num days is 0 but diff is 20h
        date_json = data['somef_provenance']['date']
        date2_json = data['date_updated'][0]['result']['value'][:-1]
        prov = datetime.strptime(date_json, '%Y-%m-%d %H:%M:%S')
        extract = datetime.strptime(date2_json, '%Y-%m-%dT%H:%M:%S')
        days = (prov-extract).days
        self.assertEqual(days,meta.last_update_days(),0)
    def test_licence(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        license = data['license'][0]['result']['name']
        self.assertEqual(license,meta.license()['name'])

    def test_numReleases(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        rel =  data['releases']
        self.assertEqual(meta.n_releases(),len(rel))
    #TODO
    def no_releases(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        pass
    def test_downloadUrl(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        url = data['download_url'][0]['result']['value']
        self.assertEqual(meta.downloadUrl(),url)
    def test_readmeUrl(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        url = data['readme_url'][0]['result']['value']
        self.assertEqual(meta.readme(),url)
    #TODO
    def test_no_readme(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.readme())
        pass

    def test_last_release(self):

        pass
    def test_logo(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        logo = data['logo'][0]['result']['value']
        self.assertEqual(meta.logo(),logo)
    def test_logo_default(self):
        # This JSON represents a github with only a readme(containing an image)
        path2 = Path(__file__).parent / "json_files" / "testLogo.json"
        with path2.open() as f:
            logo = json.load(f)
        f.close()

        plain = md.metadata(path2, logo)
        self.assertIn(plain.logo(),"img/github-default.svg")

    def test_documentation(self):
        path = Path(__file__).parent / "json_files" / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        self.assertEqual(meta.hasDocumentation(),data['documentation'])
    def test_noDocumenation(self):
        # This JSON represents a github with only a readme(containing an image)
        path2 = Path(__file__).parent / "json_files" / "testLogo.json"
        with path2.open() as f:
            logo = json.load(f)
        f.close()

        plain = md.metadata(path2, logo)
        self.assertIsNone(plain.hasDocumentation())
    #TODO
    def test_citations(self):
        path = Path(__file__).parent / "json_files"  / "somef9.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        pen = meta.citations()
        print(pen['citation'])

        pass
    def test_noCitation(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.citations())
    def test_paper(self):
        #path = Path(__file__).parent / "json_files" / "somef9.json"
        path = Path(__file__).parent / "json_files" / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        self.assertIn("doi.org", meta.paper()[0].link_paper)
    def test_noPaper(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.paper())
    def test_title(self):
        path = Path(__file__).parent / "json_files"  / "oeg-upm_r4r.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        title = data['name'][0]['result']['value']
        self.assertEquals(title,meta.title())
    #TODO
    def test_noTitle(self):
        pass
    def test_owner(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        owner = data['owner'][0]['result']['value']
        self.assertEqual(meta.owner(),owner)
    def test_noOwner(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.hasDocumentation())

    #WIDOCO does not have acknowlegdements
    def test_acknowledgement(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        print(meta.acknowledgement())
        #self.assertEqual(meta.acknowledgement())
    def test_noAcknowlegement(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.acknowledgement())

    def test_repoUrl(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        url = data['code_repository'][0]['result']['value']
        self.assertEqual(meta.repo_url(),url)
    def test_Nourl(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.repo_url())
    def test_identifier(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        id = data['identifier'][0]['result']['value']
        self.assertEqual(meta.identifier(),id)
    def test_noId(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.identifier())

    #TODO
    def test_requirements(self):
        pass
    def test_noRequirements(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.requirements())
    #TODO
    def test_docker(self):
        pass
    def test_noDocker(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.docker())

    #TODO
    def test_installation(self):
        pass

    def test_noInstallation(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        self.assertIsNone(meta.installation())

    def test_languages(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        for lang in meta.languages():
            if lang == "python":
                self.assertTrue()
    def test_noLanguage(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.languages())
    #TODO
    def test_copy_btn(self):
        #print(meta.copy_btn())
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        print(meta.repo_url())
        pass

    def test_status(self):
        path = Path(__file__).parent / "json_files"  / "widoco_9_test.json"
        with path.open() as f:
            data = json.load(f)
        f.close()
        meta = md.metadata(path, data)
        status = data['repository_status']
        self.assertEqual(meta.status(),status)
    def test_noStatus(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.status())

    #TODO
    def test_usage(self):
        path5 = Path(__file__).parent / "json_files" / "somef9.json"
        with path5.open() as f:
            somef9jayson = json.load(f)
        f.close()
        somef9 = md.metadata(path5, somef9jayson)
        #print(somef9.usage())
        pass
    def test_noUsage(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.usage())

    def test_notebook(self):
        path5 = Path(__file__).parent / "json_files" / "somef9.json"
        with path5.open() as f:
            somef9jayson = json.load(f)
        f.close()
        somef9 = md.metadata(path5, somef9jayson)
        #print(somef9.notebook())
        pass
    def test_noNotebook(self):
        mT = json.loads('{"emtpy":"mT"}')
        path = Path("doesntExist")
        empty = md.metadata(path, mT)
        self.assertIsNone(empty.notebook())
        
    def test_repo_type(self):
        path5 = Path(__file__).parent / "json_files" / "somef9.json"
        with path5.open() as f:
            somef9jayson = json.load(f)
        f.close()
        somef9 = md.metadata(path5, somef9jayson)
        #print(somef9.repo_type())
        pass
    def test_repo_type(self):
        path5 = Path(__file__).parent / "json_files" / "somef9.json"
        with path5.open() as f:
            somef9jayson = json.load(f)
        f.close()
        somef9 = md.metadata(path5, somef9jayson)
        kek = somef9.html_repo_type()
        print(kek)
    #TODO
    def test_html_repo_icons(self):
        path = Path(__file__).parent / "json_files" / "oeg-upm_soca.json"
        with path.open() as f:
            somef9jayson = json.load(f)
        f.close()
        somef9 = md.metadata(path, somef9jayson)
        somef9.html_repo_icons()
        pass
    def test_r4r(self):
        path = Path(__file__).parent / "json_files" / "oeg-upm_awesome-semantic-web.json"
        with path.open() as f:
            r4rjayson = json.load(f)
        f.close()
        r4r = md.metadata(path, r4rjayson)
        r4r.html_repo_icons()
        pass


if __name__ == '__main__':
    unittest.main()

