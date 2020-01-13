import os
import configparser
from bs4 import BeautifulSoup
import logging.config
from datetime import datetime

class ParseExtract:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('myconfigpaths.ini')
        config.sections()
        self.filepathtohtml ="C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_html"
        print("filepathhtml", self.filepathtohtml)
        self.filepathcsv = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_csv\\"
        # logging.config.fileConfig('aaa.conf')
        # logger = logging.getLogger('MainLogger')
        # fh = logging.FileHandler('C:\logs_xbrl\{:%Y-%m-%d}.log'.format(datetime.now()))
        # formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

    def parsetocsv(self,path):
            for fname in os.listdir(self.filepathtohtml):
                print(fname)
                f = fname.rsplit(".", 1)[0]
                if f == path:
                    pathcsv=self.filepathtohtml+'\\'+fname
                    file = open(pathcsv, 'r', encoding='utf-8')
                    content = file.read()
                    reader = BeautifulSoup(content, "lxml")
                    csv_data = ""
                    tables = reader.find_all('table')
                    for table in tables:
                        for tr in table.find_all('tr'):
                            tds = tr.find_all('td')
                            if tr.text.strip != '':
                                if len(tds) >= 3:
                                    for td in tds[:3]:
                                        if td.text != '':
                                            csv_data += td.text.replace('\n', '') + ', '
                                        else:
                                            csv_data += ', '

                                    csv_data += '\n'

                    f = fname.rsplit(".", 1)[0]
                    f = path + ".csv"
                    filepath = self.filepathcsv + f
                    open(filepath, 'w', encoding='utf-8').write(csv_data)
                    return "Successful"

if __name__ == '__main__':
    con=ParseExtract()
    con.parsetocsv("226567066")
