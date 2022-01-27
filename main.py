import sys
import requests
from requests.auth import HTTPDigestAuth
from time import localtime, strftime
import logging
from xml.etree import ElementTree

from constants import DATE_TIME_FORMAT, INCORRECT_ARGUEMENTS, INCORRECT_CREDENTIALS, LOG_FILE, MAX_TEMP, TEMPERATURE_API, TRIGGERED, ZONE_ID

# Logging Parameters
logging.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logging.WARNING)

def main(argv):
    # Check for argument length
    if len(argv) != 3:
        logging.error(INCORRECT_ARGUEMENTS)
        return 0

    # URL Parameters
    url = TEMPERATURE_API.format(argv[0])
    r = requests.get(url, auth=HTTPDigestAuth(argv[1], argv[2]), stream=True)

    if r.status_code != 200:
        logging.error(INCORRECT_CREDENTIALS)
        return 0

    # Parse XML response
    root = ElementTree.fromstring(r.content)
    
    # Init Array
    zoneIDArr = []
    maxTempArr = []
    triggeredArr = []

    for child in root.iter('*'):
        if child.tag == ZONE_ID:
            zoneIDArr.append(child.text)
        
        if child.tag == MAX_TEMP:
            maxTempArr.append(child.text)

        if child.tag == TRIGGERED:
            triggeredArr.append(child.text)

    currentDateTime = strftime(DATE_TIME_FORMAT, localtime())

    # logging loop
    for i in range (0,len(zoneIDArr)):
        response = u'{} : {} - ZoneID: {} - Temperature: {}\N{DEGREE SIGN} - Triggered: {}.'.format(currentDateTime, argv[0], zoneIDArr[i], maxTempArr[i], triggeredArr[i])
        logging.warning(response)

if __name__ == "__main__":
   main(sys.argv[1:])