'''
Created on 1 Jul 2015

@author: Rombli
'''
from lxml import etree
from StringIO import StringIO
import re, os

xml_ns = "http://www.w3.org/XML/1998/namespace"

#error_log is a list of tuples that collects error that have to be checked by human
error_log = []


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
    #comparison of elements
    #they do not have to be identical
    try: 
        if e1.text == e2.text:
            return True
        elif e1.attrib["lemma"] == e2.attrib["lemma"]:
            if e1.text[:2] == e2.text[:2]:
                return True
            else:
                error_log.append((e1.attrib["{%s}id" % xml_ns], e2.attrib["{%s}id" % xml_ns])) 
                return True
        elif e1.attrib["lemma"] == "unknown" and (e1.text[:2] == e2.text[:2]):
            error_log.append(("@lemma is unknown", e1.attrib["{%s}id" % xml_ns])) 
            return True
        elif e2.attrib["lemma"] == "unknown" and (e1.text[:2] == e2.text[:2]):
            error_log.append(("@lemma is unknown", e2.attrib["{%s}id" % xml_ns])) 
            return True
        else:
            return False
    except KeyError:
        try:
            error_log.append((e1.attrib["{%s}id" % xml_ns], e2.attrib["{%s}id" % xml_ns]))
        except KeyError:
            error_log.append(("xml:id error", e1.text, e2.text))
        

def similar_element_in_lst(lst, ele):
    #returns the position of the element
    loc = []
    for idx, item in enumerate(lst):
        if compare_two_elements(item, ele):
            loc.append(idx)
    if len(loc) == 0:
        return None
    elif len(loc)>0:
        return loc       
    else:
        print "Error: there is something wrong: {}".format(loc)


def compare_lines(*lines):
    #lines is a certain amount of etree xml objects containing lines
    matches = []
    for line in lines:
        if len(matches) == 0:
            for idx, ele in enumerate(line):
                if ele.tag == "w":
                    matches.append([ele])
        else:
            for idx, ele in enumerate(line):
                if ele.tag == "w": 
                    locs = similar_element_in_lst([m[0] for m in matches], ele)
                    
                    if not locs:
                        matches = matches[:idx] + [[ele]] + matches[idx:]
                    else:
                        locs_in_line = similar_element_in_lst(line, ele)
                    if ele == line[locs_in_line[0]]:
                        if len(locs) == 1:
                            matches[locs[0]].append(ele)
                        elif len(locs) > 1:
                            
                            if len(locs_in_line) == len(locs):
                                for i, l in enumerate(locs):
                                    matches[l].append(line[locs_in_line[i]])
                            elif len(locs_in_line) > len(locs):
                                dif = len(locs_in_line) - len(locs)
                                for i, l in enumerate(locs):
                                    matches[l].append(line[i]) 
                                for lil in locs_in_line[-dif:]:
                                    matches = matches[:lil] + [[ele]] + matches[lil:]
                            elif len(locs_in_line) < len(locs):
                                dif = len(locs_in_line) - len(locs)
                                for i, l in enumerate(locs[:-dif]):
                                    matches[l].append(line[locs_in_line[i]])
                            else:
                                print "Something is wrong in function compare lines"
                        
                        
    return matches                
                
                        
            
def generate_linking_groups(matches, file_name=None):
    if not file_name:
        res_strg = ""
    
    
    for m in matches:
        strg = "{0}: {1}\n"
        strg = strg.format(", ".join([e.text for e in m]), ", ".join([e.attrib["{%s}id" % xml_ns] for e in m]))
        
        if file_name:
            if os.path.isfile(file_name):
                with open(file_name, "w") as f:
                    f.write(strg)
            else:
                print("Error: the variable 'file_name' is no valid file_name")
        else:
            res_strg += strg
    
    if not file_name:       
        return res_strg
    else:
        print("Linking groups have been written to file: ".format(file_name))
            
        
            
        
        
        
    
    

def slice_strg(strg, pat):
    return re.split(pat, strg)

def apply_xslt(xml, xslt):
    #xslt_root = etree.XML(xslt)
    transform = etree.XSLT(xslt)
    return transform(xml)
     

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
            print("Strg: {}".format(strg))
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
    elif line_strg.strip() == "":
        #empty string
        return """<line>{0}</line>""".format(line_strg)
    else:
        print("Error: The variable line_strg is {}, but should be a string".format(type(line_strg)))
        

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
    
    wit_lst = []
    
    #linux home
    path = [os.sep + "home", "roman", "Dropbox", "XML", "Transcriptions", "Masterfiles"]
    
    s = os.sep.join(path)
    #print(os.path.isdir(s))
    #print(os.getcwd())
    
    
    xml_files = ["dublin_tcd_library_ms_52", "london_british_library_ms_cotton_nero_E1"] 
    xslt_file = os.sep.join(path[:-1]) + os.sep + "makeLinkingGroups.xsl"
    
    #print(os.path.isfile(xslt_file))
    
    for xml_file in xml_files:
        full_path = os.sep.join(path) + os.sep + xml_file + os.sep + xml_file + ".xml"
        #print(os.path.isfile(full_path))
        print(full_path)
        tei = open_xml_file(full_path)
        xslt = open_xml_file(xslt_file)
        res_tree = apply_xslt(tei, xslt)
        #print(etree.tostring(res_tree))
        with open("resttree.xml", "w") as f:
            f.write(etree.tostring(res_tree))
        #namespaces = {'tei' : 'http://www.tei-c.org/ns/1.0'}
        d = split_on_lbs(etree.tostring(res_tree), "//lb")
        wit_lst.append(d)
        print len(d)
    
       
    lbs = res_tree.xpath("//lb")
    print(len(lbs))
    for lb in lbs:
        lbid = lb.attrib["{%s}id" % xml_ns]
        for w in wit_lst:
            line = w[lbid]
            compare_lines(etree.fromstring(line))
        
        
        
        
    print("Finish!")