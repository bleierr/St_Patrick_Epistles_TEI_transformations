'''
Created on 1 Jul 2015

@author: Rombli
'''
from lxml import etree
from StringIO import StringIO
import re

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
            
def get_elements_to_compare(xml_tree_element, xpath_condition):
    return xml_tree_element.xpath(xpath_condition)

def compare_two_elements(e1, e2):
    return e1.text == e2.text



def slice_strg(strg, pat):
    return re.split(pat, strg)

def apply_xslt(xml, xslt):
    xslt_root = etree.XML(xslt)
    transform = etree.XSLT(xslt_root)
    return transform(xml)
                

    
    









if __name__ == '__main__':
    pass