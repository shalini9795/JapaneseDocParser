import os
from lxml import etree, objectify
import configparser
import logging.config
from datetime import datetime

class Convert:

    def __init__(self):
        self.path_xbrl = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\"
        self.path_xml = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_xml\\"
        self.path_src = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_xml"
        # logging.config.fileConfig('aaa.conf')
        # self.logger = logging.getLogger('MainLogger')
        # fh = logging.FileHandler('C:\logs_xbrl\{:%Y-%m-%d}.log'.format(datetime.now()))
        # formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
        # fh.setFormatter(formatter)
        # self.logger.addHandler(fh)

    def convertxml(self,path):
        pathxbrl = self.path_xbrl + path
        try:
            for root, dirs, files in os.walk(pathxbrl):
                for fname in files:
                    if fname.endswith('.xbrl') and "aud" not in fname :
                        parser = etree.XMLParser(remove_blank_text=True)
                        pathxbrl = os.path.join(root, fname)
                        print(pathxbrl)
                        tree = etree.parse(pathxbrl, parser)
                        root1 = tree.getroot()
                        for elem in root1.getiterator():
                            if not hasattr(elem.tag, 'find'): continue
                            i = elem.tag.find('}')
                            if i >= 0:
                                elem.tag = elem.tag[i + 1:]
                        objectify.deannotate(root1, cleanup_namespaces=True)
                        f = fname.rsplit(".", 1)[0]
                        f = path + ".xml"
                        self.path_xml = self.path_xml + f
                        tree.write(self.path_xml, pretty_print=True, xml_declaration=True, encoding='UTF-8')
                    # self.logger.debug("conversion successful to xml")
            return "Successful"
        except Exception as e:
            print("Exception",e)
            # self.logger.debug("Converting unsuccessful")
            return "UnSuccessful"

if __name__ == '__main__':
    con=Convert()
    con.convertxml("205657681_21650871")
