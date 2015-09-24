'''
Created on 24 Sep 2015

@author: Rombli
'''
from lxml import etree
import zipfile, datetime
import os, re, pickle
from StringIO import StringIO
from ezodf import newdoc, Paragraph, Heading, Sheet, text, Span

NSMAP = {"tei": "http://www.tei-c.org/ns/1.0", 
          "xml": "http://www.w3.org/XML/1998/namespace",
          "office" :"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
          "text" : "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
          }

def open_xmlf(xml_file):
    #do not encode in unicode when opening, e.g. with codecs module
    with open(xml_file, "r") as f:
        try:
            xml = StringIO(f.read())
            parser = etree.XMLParser(encoding="utf-8", resolve_entities=False)
            tree = etree.parse(xml, parser=parser)
            #tree.xinclude()
            return tree   
        except etree.XMLSyntaxError as e:
            print e
            
            
def create_paragraphs(strg, linkGrp):
    ps = []
    first = True
    for start, end, n in linkGrp:
        if first:
            frags = strg.split("{{"+start+"}}")
            strg = frags[1]
            first = False
        parts = strg.split("{{"+end+"}}")
        if len(parts) == 2:
            ps.append("<text:p>" + n + ". " + parts[0] + "</text:p>")
            strg = parts[1]
        else:
            print "ERROR!"
    return ps


if __name__ == '__main__':
    file_path = ["C:", "Users","Rombli","Dropbox","XML","Patrick Epistles","transcriptions"]

    #xslt_file = "tei2odf-Freeman.xsl"

    xml_dirs = [
        "dublin_tcd_library_ms_52",
        "paris_BnF_ms_lat17626",
        "london_british_library_ms_cotton_nero_E1",
        "rouen_bm_ms_1391",
        "salisbury_cathedral_library_ms_221",
        "salisbury_cathedral_library_ms_223",
        "arras_bm_ms_450"
    ]
    
    style_xml = open_xmlf("styles.xml")
    styles = style_xml.xpath("//style:style", namespaces={"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0"})
    
    xslt_file = "tei2odf.xsl"
    print xslt_file
    xslt_line_trans = open_xmlf(xslt_file)
    
    transform = etree.XSLT(xslt_line_trans)
    
    flink = os.sep.join(file_path) + os.sep + "link_group_white" + ".xml"
    t = open_xmlf(flink)
    linkGrp = [tuple(l.attrib["target"].strip("#").split(" #")+[l.attrib["n"]]) 
                  for l in t.xpath("//tei:link", namespaces=NSMAP)]
        
    docs = {}
    
    for name in xml_dirs:
        tei = os.sep.join(file_path) + os.sep + name +".xml"
        fresult = os.sep.join(file_path[:-1]) + os.sep + "pdf" + os.sep + name +".txt"
        doc = open_xmlf(tei)
        
        result = transform(doc)
        result.write(fresult)
        docs[name] = fresult
        
      
    for name, fresult in docs.items():
        
        with open(fresult, 'r') as f:
            doc = f.read()
        
        ps = create_paragraphs(doc, linkGrp)
        
        #the whole doc needs to be read again
        with open(fresult, 'r') as f:
            doc = f.read()
        
        ftemp = os.sep.join(file_path[:-1]) + os.sep + "pdf" + os.sep + name + ".temp"
        with open(ftemp, "w") as f:
            head = doc.split("<office:text>")[0]
            f.write(head+"<office:text>")
        
        
        for p in ps:
            pat = "{{[\w\.]+}}"
            p = ''.join(re.split(pat, p))
            with open(ftemp, 'a') as f:
                f.write(p)
        
        with open(ftemp, 'a') as f:
            tail = doc.split("</office:text>")[1]
            f.write("</office:text>" + tail)
        
        
        #create new odt file 
        fname = os.sep.join(file_path[:-1]) + os.sep + "pdf" + os.sep + name + ".odf"
        odt = newdoc(doctype='odt', filename=fname)
        
        #add styles to the odt file
        for s in styles:
            odt.inject_style(etree.tostring(s, pretty_print = True))
           
        odt_result = open_xmlf(ftemp)
        txt = odt_result.xpath("//office:text", namespaces=NSMAP)
        for idx, t in enumerate(txt[0].iterchildren()):
            odt.body.xmlnode.insert(idx, t)
        odt.save()
        print "File %s created!" %fname
        

    print "Done!"
    
    
    