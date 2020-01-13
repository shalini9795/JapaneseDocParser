import logging.config

from logging import getLogger, StreamHandler, Formatter, DEBUG
from datetime import datetime
import time

class GenerateFile:

    def __init__(self):
        logging.config.fileConfig('aaa.conf')
        logger = logging.getLogger('MainLogger')
        fh = logging.FileHandler('C:\Shalini\Projects\Parsers_NonFundamental\XBRL parsers\Logs\{:%Y-%m-%d}.log'.format(datetime.now()))
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    def generatefile(self,path):
        timestr = time.strftime("%Y%m%d%H%M%S")
        path=path+'_'+timestr
        print("path is",path)
        self.logger.debug("path is %s",{path})
        return path

if __name__ == '__main__':
    gen=GenerateFile()
    gen.generatefile("1234556")
