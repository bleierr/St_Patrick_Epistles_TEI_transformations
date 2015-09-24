"""
Script to apply an XSLT transformation to TEI files
The script was written to as part of a research project at TCD
"""
from lxml import etree
import zipfile, datetime
import os, re, pickle
from StringIO import StringIO
from ezodf import newdoc, Paragraph, Heading, Sheet, text, Span

NSMAP = {"tei": "http://www.tei-c.org/ns/1.0", 
          "xml": "http://www.w3.org/XML/1998/namespace"}


def elements_equal(e1, e2):
    #from http://stackoverflow.com/questions/7905380/testing-equivalence-of-xml-etree-elementtree
    if not isinstance(e1, etree._Element): return False
    if not isinstance(e2, etree._Element): return False
    if e1.tag != e1.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

def open_file(xml_file):
    #do not encode in unicode when opening, e.g. with codecs module
    with open(xml_file, "r") as f:
        try:
            xml = StringIO(f.read())
            parser = etree.XMLParser(encoding="utf-8", resolve_entities=False)
            tree = etree.parse(xml, parser=parser)    
        except etree.XMLSyntaxError as e:
            print e
        return tree

    #xml = StringIO("<surface><l><w n='1'>exam<ex>ABBR</ex>ple</w><w n='2'>Word2</w></l></surface>")
    #tree = etree.parse(xml, parser=parser)
    
       
def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print info.filename
        print '\tComment:\t', info.comment
        print '\tModified:\t', datetime.datetime(*info.date_time)
        print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
        print '\tZIP version:\t', info.create_version
        print '\tCompressed:\t', info.compress_size, 'bytes'
        print '\tUncompressed:\t', info.file_size, 'bytes'
        print

def tei2odf(xml_file, xslt_file, result_file):
    xslt_tree = open_file(xslt_file)
    
    transform = etree.XSLT(xslt_tree)
    
    #transform the TEI transcriptions with XSLT to odt XML format
    doc = open_file(xml_file)
    result_tree = transform(doc)

    #create new odt file
    odt = newdoc(doctype='odt', filename=result_file)
    #add styles to the odt file
    styles = result_tree.xpath("//style:style", namespaces={"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0"})
    for s in styles:
        odt.inject_style(etree.tostring(s, pretty_print = True))

    #add the body/text to the odd file
    text = result_tree.xpath("//office:text/*", namespaces={"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0"})
    
    for idx, t in enumerate(text):
        odt.body.xmlnode.insert(idx,t)

    odt.save()

def addImages2odt(odt_file, picture_dir):
    #add images to the odt file
    z = zipfile.ZipFile(odt_file, mode="a")
    for root, dirs, files in os.walk(picture_dir):
        for file in files:
            z.write(os.path.join(root, file), os.path.join("Pictures", file) ,compress_type=zipfile.ZIP_DEFLATED)

    z.close()


def getReferencesFromAttrib(attrStrg):
    lst = []
    for s in re.split("#", attrStrg):
        if not s.strip() == "":
            lst.append(s.strip())
    return tuple(lst)

def get_elements_between_ids(t, id1, id2, pat="*"):
    #returns a list of all elements between two ids and the elements carrying the ids
    #print (id1, " ", id2)
    e1 = t.findall("//tei:lb[@xml:id='"+id1+"']", namespaces=NSMAP)[0]
    e2 = t.findall("//tei:lb[@xml:id='"+id2+"']", namespaces=NSMAP)[0]
    process_elements = ["{%s}zone" %NSMAP["tei"],
                      "{%s}surface" %NSMAP["tei"],
                      "{%s}line" %NSMAP["tei"]
                      ]
    between = False
    lst = []
    for e in t.findall("//%s" %pat, namespaces=NSMAP):
        if not isinstance(e, etree._Element):
            print "ERROR!!!"
        if elements_equal(e, e1):
            between = True
        if between:
            par = e.getparent()
            if (par.tag == "{%s}line" %NSMAP["tei"]) or (e.tag in process_elements):
                lst.append(e)
        if elements_equal(e, e2):
            return lst

def find_ancestor(ele, ancestor_tag, attrib):
    #if ele.getparent().tag == "{http://www.tei-c.org/ns/1.0}sourceDoc":
    print ("In find_ancestor!")
    for anc in ele.iterancestors(ancestor_tag):
        print ("In find_ancestor iterancestors!")
        print anc
        if not isinstance(anc, etree._Element):
            print "Error in functon find_page: startpage not correct!!!"
        print "before return!"
        return anc.attrib[attrib]
    return None
    
    
def create_section_xml(chapt_nr, lst): 
    xslt_file = "tei2odf_linelevel.xsl"
    
    xslt_line_trans = open_file(xslt_file)
    
    transform = etree.XSLT(xslt_line_trans)
    p = Paragraph()
    if chapt_nr:
        p.append_text(chapt_nr + ". ")
    
    #lines = [l for l in lst if l.tag == "{%s}line" %NSMAP["tei"]]
    for ele in lst:
        if ele.tag == "{%s}space" %NSMAP["tei"]:
            next_ele = ele.getnext()
            if next_ele != None:
                if next_ele.tag != "{%s}pc" %NSMAP["tei"]:
                    p.append_text(" ") 
        else:
            xslttree = transform(ele)
            result = etree.fromstring(str(xslttree))
            p.xmlnode.append(result)
    return p
    

if __name__ == "__main__":
    
    file_path = ["C:", "Users","Rombli","Dropbox","XML","Patrick Epistles","transcriptions"]

    #xslt_file = "tei2odf-Freeman.xsl"

    """dublin_tcd_library_ms_52",
    "london_british_library_ms_cotton_nero_E1",
    "paris_BnF_ms_lat17626"""


    xml_dirs = [
        "dublin_tcd_library_ms_52",
    "london_british_library_ms_cotton_nero_E1",
    "paris_BnF_ms_lat17626",
    "rouen_bm_ms_1391",
    "salisbury_cathedral_library_ms_221",
    "salisbury_cathedral_library_ms_223"
    ]
    
    
    link_group_white = os.sep.join(file_path) + os.sep + "includes" + os.sep + "link_group_white" +".xml"
    print link_group_white
        
    t1 = open_file(link_group_white)
    mapping = t1.xpath("//tei:link", namespaces={"tei": "http://www.tei-c.org/ns/1.0"})
    
    style_xml = open_file("styles.xml")
    styles = style_xml.xpath("//style:style", namespaces={"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0"})
        
    for d in xml_dirs:
        sections = []
        xml_file = os.sep.join(file_path) + os.sep + d +".xml"
        print xml_file
        
        t2 = open_file(xml_file)
        lst = []
        for e in mapping:
            id1, id2 = getReferencesFromAttrib(e.attrib["target"])
            chapt_nr = e.attrib["n"]
            lst.append((chapt_nr, get_elements_between_ids(t2, id1, id2)))
            
        print len(lst)
        
        for num, l in lst:
            #l is a tuple of chapt_nr and list of chapter elements
            sections.append(create_section_xml(num, l))
            
        print len(sections)
        
        
        #create new odt file
        fname = d+".odf"
        if os.path.isfile(fname):
            os.remove(fname)
            print "File %s removed!" %fname
        odt = newdoc(doctype='odt', filename=fname)
        print "File %s created!" %fname
        
        #add styles to the odt file
        for s in styles:
            odt.inject_style(etree.tostring(s, pretty_print = True))
        print "Styles added to file %s!" %fname
        
        #add title
    
        #add first folio nr
    
    
        for idx, p in enumerate(sections):
            print "Adding paragraph %s!" %idx
            if idx == 0:
                num, l = lst[0]
                print "before ancestor found!"
                aid = find_ancestor(l[0], "{http://www.tei-c.org/ns/1.0}surface", "{%s}id" %NSMAP["xml"])
                print "ancestor found!"
                page_nr = aid.split("-")[-1]
                print "page number!"
                s = Span("(%s)" %page_nr)
                print "created span!"
                p.insert(0,s)
            odt.body.append(p)
        print "Paragraphs added to file %s!" %fname
        odt.save()
        

    print "Done!"
    print "File " 
    
    """
    for d in xml_dirs:
        xml_file = file_path + os.sep + d + os.sep + d + ".xml"
        result_file = d + ".odt"
        picture_dir = file_path + os.sep + d + os.sep + "characters"

        print xml_file
        tei2odf(xml_file, xslt_file, result_file)
        
        #addImages2odt(result_file, picture_dir)
        
        #print a report of the content of the odt file
        #print_info(result_file)
    """
    
    
