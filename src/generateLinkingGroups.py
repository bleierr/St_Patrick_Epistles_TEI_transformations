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

def contains_xml_tags(strg):

    pat = r"<\/\w+>"

    r = re.findall(pat, strg)
    if r:
        return True
    else:
        return False


def remove_closing_tag(strg):
    strg = strg.strip()
    try:
        pat = r"<\/\w+>"
        r = re.findall(pat, strg)
        if not r:
            return strg
        tag = r[-1]
        l = len(tag)
        if strg[-l:] == tag:
            return strg[:-l]
        else:
            print("Tag does not match end of string.")
            print("Tag: {}".format(tag))
            return strg
    except TypeError as e:
        print e
        print "Param strg was: {}".format(strg)
    except IndexError as e:
        print "Param r was: {}".format(r)
        print e
        raise IndexError
        

def compare_root_element(strg):
    strg = strg.strip()
    if strg == "":
        return True
    try:
        pat = r"<\/\w+>"
        r = re.findall(pat, strg)
        close_tag = r[-1]
        start_tag = "<" + close_tag[2:-1]
        l = len(start_tag)
        if strg[:l] == start_tag:
            return True
        else:
            return False
    except TypeError as e:
        print e
        print "Param strg was: {}".format(strg)
    except IndexError as e:
        print e
        print "Param r was: {}".format(r)
        
    

def generate_valid_xml_line(line_strg, lb1, lb2=None):
    p1 = lb1.getparent() 

    #Error handling in case if the lbs are not correctly nested
    if p1.tag not in ["text", "w"]:
        print("Error: lb {} is not correctly nested!".format(lb1.attrib["{%s}id" % xml_ns]))
        print(p1.tag)
    else:
        if p1.tag == "w":
            lst = re.split("</w>", line_strg)
            line_strg = "</w>".join(lst[1:])
        
    if lb2 is not None:
        p2 = lb2.getparent()
        if p2.tag not in ["text", "w"]:
            print("Error: lb {} is not correctly nested!".format(lb1.attrib["{%s}id" % xml_ns]))
            print(p2.tag)
        if p2.tag == "w":
            line_strg = """{0}</w>""".format(line_strg.strip())

    #print(line_strg)
    if isinstance(line_strg, str) and contains_xml_tags(line_strg):
        while(not compare_root_element(line_strg)):
            line_strg = remove_closing_tag(line_strg)

        return """<line>{0}</line>""".format(line_strg)
    else:
        print("Error: The variable line_strg is {}, but should be a string".format(line_strg))
        return """<line>{0}</line>""".format(line_strg)

def split_on_lbs(strg, lb_pat="//lb"):
    """@param lb_pat should be an XPath expression addressing a lb"""
    lines = {}
    t = etree.fromstring(strg)
    lbs = t.xpath(lb_pat)
    
    for idx, lb1 in enumerate(lbs):
        if idx < len(lbs)-1:
            lb2 = lbs[idx+1]
            after = slice_strg(strg, etree.tostring(lb1))[1]
            before = slice_strg(after, etree.tostring(lb2))[0]
            lines[lb1.attrib["{%s}id" % xml_ns]] = generate_valid_xml_line(before, lb1, lb2)
        elif idx == len(lbs)-1:
            after = slice_strg(strg, etree.tostring(lb1))[1]
            lines[lb1.attrib["{%s}id" % xml_ns]] = generate_valid_xml_line(after, lb1)
        else:
            print("Error: The variable idx should be < or == to len(lbs)") 
    return lines

    



if __name__ == '__main__':
    xml_files = []
    xslt_file = ""

    for xml_file in xml_files:
        tei = open_xml_file(xml_file)
        xslt = open_xml_file(xslt_file)
        res_tree = apply_xslt(tei, xslt)

        d = split_on_lbs(etree.tostring(res_tree, "//lb[@ed='White'"))

        print len(d)
            

    

    

            

        

        


    
