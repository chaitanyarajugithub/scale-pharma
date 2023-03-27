import time
from faker import Faker
from faker.generator import random
from api_requests import *

state = '[{"id":"currenttime","value":""},{"id":"Timezone","value":""},{"id":"DevieState","value":"ready"},{"id":"Methodname","value":"Dynamic Weighing"},{"id":"MethodType","value":"General Weighing"},{"id":"targetWeight","value":""},{"id":"lowerTolerance","value":""},{"id":"upperTolerance","value":""},{"id":"toleranceunit","value":""},{"id":"applytolerance","value":"no"},{"id":"TaskLabel1","value":"USER SAMPLE ID"},{"id":"TaskValue1","value":"S432"},{"id":"TaskLabel2","value":"METHOD/SPECIES"},{"id":"TaskValue2","value":"bee"},{"id":"TaskLabel3","value":"STUDY NO."},{"id":"TaskValue3","value":"00000421"},{"id":"ResultLabel1","value":"ANIMAL ID"},{"id":"ResultValue1","value":"1"},{"id":"ResultLabel2","value":""},{"id":"ResultValue2","value":""},{"id":"ResultLabel3","value":""},{"id":"ResultValue3","value":""},{"id":"Weight","value":"19.222"},{"id":"totalprotocols","value":"0"},{"id":"addProtocoltext1","value":""},{"id":"addProtocoltext2","value":""},{"id":"addProtocoltext3","value":""},{"id":"addProtocoltext4","value":""}]'
faker = Faker()
SAMPLEID = 'Auto'+str(random.randint(1, 9999))
METHODSPECIES = 'MSP'+str(random.randint(1, 9999))
STUDYNO = 'ST'+str(random.randint(1, 9999))
ANIMALID = random.randint(1000, 9999)
WEIGHT = random.randint(100, 999)

data = f'[{{"id":"currenttime","value":""}},{{"id":"Timezone","value":""}},{{"id":"DevieState","value":"ready"}},{{"id":"Methodname","value":"Dynamic Weighing"}},{{"id":"MethodType","value":"General Weighing"}},{{"id":"targetWeight","value":""}},{{"id":"lowerTolerance","value":""}},{{"id":"upperTolerance","value":""}},{{"id":"toleranceunit","value":""}},{{"id":"applytolerance","value":"no"}},{{"id":"TaskLabel1","value":"USER SAMPLE ID"}},{{"id":"TaskValue1","value":"{SAMPLEID}"}},{{"id":"TaskLabel2","value":"METHOD/SPECIES"}},{{"id":"TaskValue2","value":"{METHODSPECIES}"}},{{"id":"TaskLabel3","value":"STUDY NO."}},{{"id":"TaskValue3","value":"{STUDYNO}"}},{{"id":"ResultLabel1","value":"ANIMAL ID"}},{{"id":"ResultValue1","value":"{ANIMALID}"}},{{"id":"ResultLabel2","value":""}},{{"id":"ResultValue2","value":""}},{{"id":"ResultLabel3","value":""}},{{"id":"ResultValue3","value":""}},{{"id":"Weight","value":"{WEIGHT}"}},{{"id":"totalprotocols","value":"0"}},{{"id":"addProtocoltext1","value":""}},{{"id":"addProtocoltext2","value":""}},{{"id":"addProtocoltext3","value":""}},{{"id":"addProtocoltext4","value":""}}]'


def setdevicestate(simui):
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=SetDevieState&p2=' + state)


def loadmethod(simui):
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=Loadmethod&p2=' + data)


def startmethod(simui):
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=StartMethod&p2=' + data)


def addprotocol(simui):
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=AddProtocol&p2=' + data)
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=AddProtocol&p2=' + data)


def export(simui):
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=Export&p2=' + data)


def complete(simui):
    time.sleep(3)
    request_api_call(simui + '/uicallback?p1=Complete&p2=' + data)


def addprotocolexportandcomplete(simui):
    setdevicestate(simui)
    loadmethod(simui)
    startmethod(simui)
    addprotocol(simui)
    export(simui)
    complete(simui)