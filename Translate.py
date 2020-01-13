from builtins import Exception, len, range, str, any

import pyodbc as conn
import pandas.io.sql as sql
from pandas import *
import logging.config
import os
import configparser
import pandas as pd
from datetime import datetime



class Translate:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('myconfigpaths.ini')
        config.sections()
        self.filepathtocsv = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_csv\\"
        print("filepath is", self.filepathtocsv)
        self.filepathxlsx = "C:\\Applications\\Data\\ExecCompDownloader\\TempDownload\\output_xlsx\\"
        config.read('myconfigdb.ini')
        self.server = 'DMDEVDB81\DMINPUTDBDEV'
        self.db = 'PersonnelData'
        connection_str = 'Driver={SQL Server};Server=%s;Database=%s;Trusted_Connection=yes;' % (self.server, self.db)
        print("connection string is", connection_str)
        self.connection = conn.connect(connection_str, autocommit=True)
        self.connection.set_attr(conn.SQL_ATTR_TXN_ISOLATION, conn.SQL_TXN_SERIALIZABLE)
        self.connection.autocommit = False
        self.jpn = sql.read_sql_query('select * from [dbo].[JapaneseNameMppingDetail]', self.connection)
        self.jpn_title = sql.read_sql_query('select * from [dbo].[JapaneseNameMppingDetail] where NameType=5',
                                            self.connection)
        # logging.config.fileConfig('aaa.conf')
        # #self.logger = logging.getLogger('MainLogger')
        # fh = logging.FileHandler('C:\logs_xbrl\{:%Y-%m-%d}.log'.format(datetime.now()))
        # formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
        # fh.setFormatter(formatter)
        # #self.logger.addHandler(fh)
        # self.cursor = self.connection.cursor()

    def encode_decode(self, finalstring):
        return (finalstring.encode('utf-8', 'ignore')).decode("utf-8")

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def parsingFailed(self, filingLogId):
        try:
            status = 4
            values = (filingLogId, status)
            print("values", values)
            # self.cursor.execute('exec PersonnelData.[dbo].[Update_FilingStatus] ?,?', values)
            # self.cursor.commit()
            print("cursor executed")
        except Exception as e:
            print("Exception",e)
    # self.logger.debug("Exception in calling the update procedure for filingLogId")
    # self.logger.debug(filingLogId)

    def translatetoxlsx(self, path, filingLogId, company):
        print("here")
        print("filepathtocsv", self.filepathtocsv)
        path = self.filepathtocsv + path + '.csv'
        # self.logger.debug("Inside Translation")
        print(path)
        try:
            data = pd.read_csv(path, encoding='utf-8', header=None)
            print(data.head())
        except Exception as e:
            print(e)
            print("failing here")

        data.dropna(inplace=True)
        print(data.head())

        try:
            data = data[~data[0].str.contains('役名')]
            data = data[~data[2].str.contains('生年月日')]
            data = data[~data[0].str.contains('(監査等委員)')]
            data = data[~data[0].str.contains('監査役')]
            data = data[~data[0].str.contains('監査等委員')]
            print("\n\n")
            print(data.head())
        except:
            print("failed to remove heading")
            # self.logger.debug("Failed to remove heading in dataframe")

        data = data.reset_index(drop=True)
        data['EnglishName'] = [''] * len(data)
        data['EnglishTitle'] = [''] * len(data)
        # data['DocumentId'] = [''] * len(data)
        # print(data)
        data.loc[2, 'EnglishName']
        # print("data.loc[4]",data.loc[4, 'EnglishName'])
        data.loc[4, 'EnglishTitle']
        for i in range(len(data)):
            name = data.iloc[i, 2]
            if self.hasNumbers(str(name)) == True:
                name = data.iloc[i, 1]
            name = name.replace('\xa0', '').strip().split('\u3000')

            print("name is", name)
            if (len(name) == 1):
                print(name)
                print(name[0])
                lname = self.jpn.loc[(self.jpn.JapaneseName == name[0]), 'EnglishName']
                try:
                    data.loc[i, 'EnglishName'] = (lname.values[0])
                    # data.loc[i, 'DocumentId'] = path
                    # self.logger.debug("found EnglishName")
                except:
                    data.loc[i, 'EnglishName'] = ('not found')
                    print(name, ' not found', 'no spaces')
                    # data.loc[i, 'DocumentId'] = path
                    # self.logger.debug("not found")
            elif (len(name) == 2):
                # For space seperated names fname and lname
                lastname = self.jpn.loc[(self.jpn.JapaneseName == name[0]) & (self.jpn.NameType == 3), 'EnglishName']
                firstname = self.jpn.loc[(self.jpn.JapaneseName == name[1]) & (self.jpn.NameType == 1), 'EnglishName']
                try:
                    # self.logger.debug("Firstname is")
                    # self.logger.debug(firstname.values[0])
                    # self.logger.debug("Lastname is ")
                    # self.logger.debug(lastname.values[0])
                    data.loc[i, 'EnglishName'] = (firstname.values[0] + ' ' + lastname.values[0])
                    # data.loc[i, 'DocumentId'] = path
                    # self.logger.debug(data.loc[i, 'EnglishName'])
                    print("translated here", data.loc[i, 'EnglishName'])
                except:
                    data.loc[i, 'EnglishName'] = ('not found')
                    # data.loc[i, 'DocumentId'] = path

            else:
                try:
                    nm = ''
                    # print("length of", name, "is", len(name))
                    if (len(name) > 2):
                        for j in range(len(name)):
                            nm += name[j].lstrip(' ').rstrip(' ')
                            nm = nm.lstrip(' ').rstrip(' ')
                            # print("j is",j)
                        nm = nm.strip()
                        # data.loc[i, 'Fullname'] = (nm)
                        fullname = self.jpn.loc[(self.jpn.JapaneseName == nm) & (self.jpn.NameType == 4), 'EnglishName']
                        data.loc[i, 'EnglishName'] = (fullname.values[0])
                        # data.loc[i, 'DocumentId'] = path
                        # self.logger.debug("fullname is ")
                        # self.logger.debug(fullname)
                except:
                    # #self.logger.debug("name not found for ", fullname.values[0])
                    data.loc[i, 'EnglishName'] = "not found"
                    # data.loc[i, 'DocumentId'] = path

        for i in range(len(data)):
            name = data.iloc[i, 0]
            name = name.replace('\xa0', '').strip().split('\u3000')
            print(name)
            if (len(name) == 1):
                lname = self.jpn_title.loc[(self.jpn_title.JapaneseName == name[0]), 'EnglishName']
                try:
                    data.loc[i, 'EnglishTitle'] = (lname.values[0])
                except:
                    # self.logger.debug("name not found for ")
                    data.loc[i, 'EnglishTitle'] = "not found"

        # f = fname.rsplit(".", 1)[0]
        f = path + ".xlsx"
        filepath = self.filepathxlsx + f
        print("excel filepath is ", filepath)
        data.to_excel(filepath, encoding='utf-8')

        # count = 0
        # try:
        #     print(data.columns)
        #     values = (filingLogId, company)
        #     print(len(data))
        #     self.cursor.execute('exec PersonnelData.[dbo].[Update_OfficerStatus] ?,?', values)
        #     sql = 'exec PersonnelData.[dbo].[Insert_XBRLOfficer] ?,?,?,?,?,?,?,?'
        #     for i in range(len(data)):
        #         if self.hasNumbers(str(data.iloc[i, 2])) == True:
        #             values = (
        #                 filingLogId, company, data.loc[i, 'EnglishName'], data.iloc[i, 1], data.loc[i, 'EnglishTitle'],
        #                 'Yes', data.iloc[i, 0], 0)
        #         else:
        #             values = (
        #             filingLogId, company, data.loc[i, 'EnglishName'], data.iloc[i, 2], data.loc[i, 'EnglishTitle'],
        #             'Yes', data.iloc[i, 0], 0)
        #
        #         print(sql, values)
        #         # self.cursor.execute('exec PersonnelData.[dbo].[Insert_XBRLOfficer] ?,?,?,?,?,?,?,?', values)
        #     my_word = ["not found"]
        #     if data.query("EnglishName=='not found'").empty & data.query("EnglishTitle=='not found'").empty:
        #         status = 3
        #     else:
        #         status = 2
        #     values = (filingLogId, status)
        #     # self.cursor.execute('exec PersonnelData.[dbo].[Update_FilingStatus] ?,?', values)
        #     # self.cursor.commit()
        #     data.drop(data.index, inplace=True)
        # except Exception as e:
        #     self.connection.close()
        #     print("Exception",e)
        #     # self.logger.debug("error saving in excel")
        #     # self.logger.error(e)
            # try:
            #     # self.parsingFailed(filingLogId)
            # except:
            #     print("Exception here")
            # self.logger.debug("error in calling procedure for filingLogId")
            # self.logger.debug(filingLogId)



if __name__ == '__main__':
    t = Translate()
    t.translatetoxlsx('227349160', 420855, 116994)
    # t.translatetoxlsx('226734640',414306,139982)
    # t.translatetoxlsx('226734663',414298,146917)
    # t.translatetoxlsx('226734697',414290,117158)
    # t.translatetoxlsx('226734822',414265,113139)
    # t.translatetoxlsx('226734872',414257,114179)


