'''
Created on 1 Jul 2015

@author: Rombli
'''
from lxml import etree
from StringIO import StringIO
import re

xml_ns = "http://www.w3.org/XML/1998/namespace"

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
            

def compare_two_elements(e1, e2):
    return e1.text == e2.text



def slice_strg(strg, pat):
    return re.split(pat, strg)

def apply_xslt(xml, xslt):
    xslt_root = etree.XML(xslt)
    transform = etree.XSLT(xslt_root)
    return transform(xml)

def apply_filter(xml, pat):
    return xml_tree_element.xpath(xpath_condition)
                

def generate_valid_xml(strg, tag_lst):
    for tag in tag_lst:

        strg = "".format()
        try:
            tree = etree.fromstring(strg)
            return tree
        except etree.XMLSyntaxError as e:
            print "Error in generate_valid_xml function:"
            print e
            
            continue
    

def generate_valid_xml_line(line_strg, lb1, lb2=None):
    p1 = lb1.getparent() 

    if p1.tag not in ["text", "w"]:
        print("Error: lb {} is not correctly nested!".format(lb1.attrib["{%s}id" % xml_ns]))
        print(p1.tag)
    else:
        if p1.tag == "w":
            pline = p1.getparent()
            line_strg = """<w xml:id="{0}" lemma="{1}"
                        type="{2}">{3}""".format(p1.attrib["{%s}id" % xml_ns],
                                                 p1.attrib["lemma"],
                                                 p1.attrib["type"],
                                                 line_strg)
        
    if lb2 is not None:
        p2 = lb2.getparent()
        if p2.tag not in ["text", "w"]:
            print("Error: lb {} is not correctly nested!".format(lb1.attrib["{%s}id" % xml_ns]))
            print(p2.tag)
        if p2.tag == "w":
            line_strg = """{0}</w>""".format(line_strg)
    
            
    return """<line>{0}</line>""".format(line_strg)




if __name__ == '__main__':
    xml_files = []

    wit = {}
    for x in xml_files:
        tree = open_xml_file(x)
        lbs = tree.xpath("\\lb[@ed='White']")

        wit[x] = {}
        for idx, lb in enumerate(lbs):

            with open(x, "r") as f:
                xml_strg = f.read()
                rest_strg = slice_strg(xml_strg, etree.tostring(lb))[1]
                line_strg = slice_strg(rest_strg, etree.tostring(lbs[idx+1]))[0]

            following_lb = lbs[idx+1]

            line_strg = generate_valid_xml_line(lb, following_lb)
 
            wit[x][lb.attrib["xml:id"]] = line_strg

            

        

        


    
