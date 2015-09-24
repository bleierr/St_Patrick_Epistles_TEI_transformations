'''
Created on 12 Aug 2015

@author: Rombli
'''
from lxml import etree
from StringIO import StringIO
import re, os

def open_xml_file(xml_file):
    #do not encode in unicode when opening, e.g. with codecs module
    with open(xml_file, "r") as f:
        try:
            xml = StringIO(f.read())
            parser = etree.XMLParser(encoding="utf-8", resolve_entities=False)
            tree = etree.parse(xml, parser=parser)
            return tree
        except etree.XMLSyntaxError as e:
            print "Error in open_xml_file function:"
            print e

def compareIDS(t, s):
    """ t: a etree element with IDs on each element
        s: a string containing IDs of the above etree element (t)
        
    """
    xml_ns = "http://www.w3.org/XML/1998/namespace"
    tei_ns = "http://www.tei-c.org/ns/1.0"
    rom_ns = "romansStyle"
    root = t.getroot()
    ids = root.xpath("//tei:w/@xml:id", namespaces={"tei":tei_ns, "xml":xml_ns, "rom":rom_ns})
    
    print len(ids)
    
    error_lst = []
        
    for item in ids:
        pat = item + "[\"\s]"
        m = re.findall(pat, s)
        if m:
            if len(m) != 1:
                error_lst.append(item)
        else:
            error_lst.append(item)
        
    return error_lst
     
    
    




if __name__ == '__main__':
    #linux home
    #path = [os.sep + "home", "roman", "Dropbox", "XML", "Transcriptions", "Masterfiles"]
    #win home
    path = ["C:", "Users", "Rombli", "Dropbox", "XML", "Transcriptions", "Masterfiles"]

    xml_files = ["dublin_tcd_library_ms_52", 
                 "london_british_library_ms_cotton_nero_E1",
                 "paris_BnF_ms_lat17626", 
                 "arras_bm_ms_450",
                 "rouen_bm_ms_1391", 
                 "salisbury_cathedral_library_ms_221",
                 "salisbury_cathedral_library_ms_223"                 
                 ]
    
    total_errors = []
    
    for xml_file in xml_files:
        full_path = os.sep.join(path) + os.sep + xml_file + os.sep + xml_file + ".xml"
        
        link_group = os.sep.join(path[:-1]) + os.sep + "generatedLinkingGroups.xml"
        
        with open(link_group, "r") as f:
            s = f.read()
        
        t = open_xml_file(full_path)

        error_lst = compareIDS(t, s)
        
        error_file = os.sep.join(path[:-1]) + os.sep + xml_file+"_link_errors.txt"
        
        with open(error_file, "w") as f:
            f.write("\n".join(error_lst))
    
    print "Done!"
    


