import argparse
import xml.etree.ElementTree as ET
import re



def ArgumentParser() :
    parser = argparse.ArgumentParser(description = 'This is a program to read certain data from xml file.')
    parser.add_argument('-path_xml', '-xml', help = 'Type path to xml file including file name.')
    global args
    args = parser.parse_args()



def RetrieveGovernments() :
    governments = set()          #Create set to store unique values.
    try :
        with open(args.path_xml, 'r') as xml_file :       #Open and read xml file.
            xml_data = xml_file.read()
            xml_data = ET.fromstring(xml_data)
            countries = xml_data.findall('country')       #Find all tags "country" in xml file.

            for country in countries :                    #Under each tag "country" find "name" and get value from it.
                country_name = country.get('name')
                if re.search(' ', country_name) :         #If "name" consists of more than one word - find "description" and get value from it.
                    governments.add(country.get('government').strip())      #Add value to set. Also remove extra spaces at the begin and at the end of "description" value (if exist).

        governments_str = re.sub("['{}]", "", str(governments))         #Convert completed set to string, remove needless symbols.
        print(governments_str)                                          #Print result.
    except :
        print("Can't work with xml file. Check the path and file name.")



if __name__ == '__main__' :
    ArgumentParser()
    RetrieveGovernments()
