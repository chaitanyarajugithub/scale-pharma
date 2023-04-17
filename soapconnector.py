import time
import requests
import random
import string
from datetime import datetime, timedelta


# get the current date and time
now = datetime.now()
# format the current date and time as a string
datetoday_str = now.strftime('%Y-%m-%d %H:%M:%S +05:30')
# get the date and time 10 days from now
dateafter10days = now + timedelta(days=10)
# format the date and time 10 days from now as a string
dateafter10days_str = dateafter10days.strftime('%Y-%m-%d %H:%M:%S +05:30')


def createdata(username):
    # create some sample JSON values and append them to the array
    json_value1 = {
        "EMPlanNumber": ''.join(random.choices(string.digits, k=random.randint(7, 10))),
        "SampleNumber": ''.join(random.choices(string.digits, k=random.randint(7, 10))),
        "TestNumber": ''.join(random.choices(string.digits, k=random.randint(7, 10))),
        "Datetoday": datetoday_str,
        "Dateafter10days": dateafter10days_str,
        "site": 'WEST_POINT_QO',
        "user1": username,
    }
    return json_value1


def addsceduledsample(soapconnectorurl, filedata):
    with open("sceduledsample.xml", "r") as f:
        xmldata = f.read()
    time.sleep(2)
    data = {
        "EMPlanNumber": filedata["EMPlanNumber"],
        "SampleNumber": filedata["SampleNumber"],
        "TestNumber": filedata["TestNumber"],
        "Datetoday": filedata["Datetoday"],
        "Dateafter10days": filedata["Dateafter10days"],
        "site": filedata["site"],
        "user1": filedata["user1"],
    }
    def replaceData(xml, data):
        result = xml
        for key in data:
            result = result.replace("{{" + key + "}}", data[key])
        return result
    xmlBody = replaceData(xmldata, data)
    headers = {
        "Content-Type": "application/xml",
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJQSEFTT0FQWDM1NUszWSIsInNlY3JldEtleSI6IlNPQVA1RTYzNyIsImlhdCI6MTU4Mjc3MjE5M30.cvi09hvgH-w1Gq_gACvsvCIRrL3pL4-2wFfBw270wVY"
    }
    response = requests.post(soapconnectorurl + "/api/v1/glims/schedule-sample", headers=headers, data=xmlBody)
    print(response.json())
    assert response.status_code == 200