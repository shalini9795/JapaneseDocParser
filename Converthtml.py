import os
from lxml import etree
from xml.sax.saxutils import escape, unescape
import lxml.html.clean as clean
import configparser
import logging.config
from datetime import datetime

class Converthtml:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('myconfigpaths.ini')
        config.sections()
        self.path_xbrl = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\"
        self.path_xml = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_xml\\"
        self.path_src = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_xml"
        self.path_html = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_html\\"
        # logging.config.fileConfig('aaa.conf')
        # self.logger = logging.getLogger('MainLogger')
        # fh = logging.FileHandler('C:\logs_xbrl\{:%Y-%m-%d}.log'.format(datetime.now()))
        # formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
        # fh.setFormatter(formatter)
        # self.logger.addHandler(fh)

    def converthtml(self,path):
        try:
            for fname in os.listdir(self.path_src):
                print(fname)
                f = fname.rsplit(".", 1)[0]
                if f==path:
                    pathhtml = self.path_src + '\\' + fname
                    root1 = etree.parse(pathhtml)
                    views = root1.xpath("//xbrl/InformationAboutOfficersTextBlock")
                    for view in views:
                        a = etree.tostring(view, with_tail=False, encoding='unicode')
                    b = unescape(a)
                    safe_attrs = clean.defs.safe_attrs
                    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
                    cleansed = cleaner.clean_html(b)
                    aa = cleansed.encode('utf-8')
                    aa.decode('utf-8')
                    f = fname.rsplit(".", 1)[0]
                    print("f is",f)
                    f = path + ".html"
                    filepath = self.path_html + f
                    print("filepath is",filepath)
                    file = open(filepath, "wb")
                    file.write(aa)
                    file.close()
                    return "Successful"
        except:
            return "UnSuccessful"
if __name__ == '__main__':
    con=Converthtml()
    con.converthtml("226567066")
