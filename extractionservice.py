from flask import Flask, jsonify, request
from Convert import Convert
from Converthtml import Converthtml
from ParseExtract import ParseExtract
from Translate import Translate
from GenerateFile import GenerateFile
import logging.config
from datetime import datetime
import threading

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks/savetodb', methods=['GET'])
def savetodb():
    # logging.config.fileConfig('aaa.conf')
    # #logger = logging.get#logger('Main#logger')
    # fh = logging.FileHandler('C:\logs_xbrl\{:%Y-%m-%d}.log'.format(datetime.now()))
    # formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    # fh.setFormatter(formatter)
    #logger.addHandler(fh)
    try:
        path=request.args.get('path')
        filingLogId=request.args.get('filingLogId')
        company=request.args.get('company')
        convert = Convert()
        converthtml = Converthtml()
        parse = ParseExtract()
        translate = Translate()
        response="file not found"
        try:
            response=convert.convertxml(path)
            #logger.debug("Conversion to xml")
            response = converthtml.converthtml(path)
            #logger.debug("Conversion to html  for docid is")
            #logger.debug(response)
            response = parse.parsetocsv(path)
            #logger.debug("Conversion to dataframe for docid is ")
            #logger.debug(path)
            response = translate.translatetoxlsx(path, filingLogId, company)
            #logger.debug("Conversion to excel for docid is ")
            ##logger.debug(path)
            return jsonify({'response': response})
        except:
            translate.parsingFailed(filingLogId)
            ##logger.error(response)
            return jsonify({'response': "Exception in parsing"})
    except Exception as e:
        translate.parsingFailed(filingLogId)
        print("Exception is ",e)
        ##logger.debug("Exception occured in the service")
        ##logger.debug(e)
        return jsonify({'response': "Exception in parsing"})


def allsteps(path,filingLogId,company):
    convert = Convert()
    converthtml = Converthtml()
    parse = ParseExtract()
    translate = Translate()
    response=convert.Convert(path)
    response=converthtml.converthtml(path)
    response=parse.parsetocsv(path)
    response=translate.translatetoxlsx(path,filingLogId,company)
    return response


if __name__ == '__main__':
    print("start")
    #app.run(host='10.90.213.139', port=8089)
    # LISTEN = ('10.90.213.139', 8089)
    # http_server = WSGIServer(LISTEN, app)
    # http_server.serve_forever()
