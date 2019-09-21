import argparse
import os
import xml.dom.minidom
import re



def ArgumentParser() :
    parser = argparse.ArgumentParser(description = 'This is a program to read certain data from xml files.')
    parser.add_argument('-folder_xml', '-folder', '-fol', help = 'Type path to the folder contains xml files')
    global args
    args = parser.parse_args()



def FolderItemsListing() :
    global folder_items
    folder_items = os.listdir(args.folder_xml)



def XMLParser() :
    output_file = open(args.folder_xml + '\\' + 'Output.txt', 'w')
    for item in folder_items :
        if item.endswith('.item') :
            xml_file_path = args.folder_xml + '\\' + item
            output_file.write(xml_file_path + '\n'*3)

            with open(xml_file_path, 'r') as xml_file :
                xml_data = xml.dom.minidom.parse(xml_file)
                nodes = xml_data.getElementsByTagName('node')

                for node in nodes :
                    component_name = node.getAttribute('componentName').lower()

                    if re.search('as400input', component_name) :
                        ElementParameters = node.getElementsByTagName('elementParameter')

                        for ElementParameter in ElementParameters :
                            ElementParameter_Name = ElementParameter.getAttribute('name').lower()

                            if re.search('trim', ElementParameter_Name) :
                                ElementParameter_Attributes = ElementParameter.attributes.items()
                                ElementParameter_Children = ElementParameter.childNodes
                                output_file.write(str(ElementParameter_Attributes) + '\n')

                                for ElementParameter_Child in ElementParameter_Children :
                                    if ElementParameter_Child.nodeType == ElementParameter_Child.ELEMENT_NODE :
                                        ElementParameter_Child_Attributes = ElementParameter_Child.attributes.items()
                                        output_file.write(str(ElementParameter_Child_Attributes) + '\n')

                                output_file.write('\n')

            output_file.write('\n'*3)

    output_file.close()



if __name__ == '__main__' :
    ArgumentParser()
    try :
        FolderItemsListing()
        XMLParser()
    except :
        print("Can't find or create file. Check the path.")
