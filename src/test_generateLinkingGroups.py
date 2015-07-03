'''
Created on 1 Jul 2015

@author: Rombli
'''
import unittest
import os
import generateLinkingGroups as glg
from lxml import etree

xml_ns = "http://www.w3.org/XML/1998/namespace"

xml_1 = """<?xml version="1.0" encoding="UTF-8" ?>
            
            <tei>
                <header><title>example text 1</title></header>
                <text>
                    <lb xml:id="lb1" ed="white"/>
                    <w xml:id="w1-1" lemma="per" type="prep">per</w>
                    <lb xml:id="lb2" ed="white"/>
                    <w xml:id="w1-2" lemma="nomen" type="noun">nomen</w>
                    <lb xml:id="lb3" ed="white"/>
                    <w xml:id="w1-3" lemma="per" type="prep"><g>P</g>er</w>
                    <w xml:id="w1-4" lemma="rusticus" type="adj"><g>r</g>usticus</w>
                    <w xml:id="w1-5" lemma="unknown" type="unknown">patricii</w>
                </text>
            </tei>
            """
            
xml_2 = """<?xml version="1.0" encoding="UTF-8" ?>
            
            <tei>
                <header><title>example text 1</title></header>
                <text>
                    <lb xml:id="lb1" ed="white"/>
                    <w xml:id="w2-1" lemma="per" type="prep">per</w>
                    <w xml:id="w2-2" lemma="Patricius" type="name">Patricius</w>
                    <lb xml:id="lb2" ed="white"/>
                    <w xml:id="w2-3" lemma="nomen" type="noun">nominis</w>
                    <lb xml:id="lb3" ed="white"/>
                    <w xml:id="w2-4" lemma="unknown" type="unknown">per</w>
                    <w xml:id="w2-5" lemma="rusticus" type="adj">rusticussimus</w>
                </text>
            </tei>
            """
            
xslt_1 = """<?xml version="1.0" encoding="UTF-8"?>
            <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
            <xsl:template match="@*|node()">
                <xsl:copy>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:copy>
            </xsl:template>
            
            <xsl:template match="header">
            </xsl:template>

            <xsl:template match="g">
                <xsl:apply-templates />
            </xsl:template>

            <xsl:template match="ex">
                <xsl:apply-templates />
            </xsl:template>
            
            </xsl:stylesheet>
        """

level_of_comparison = "//p"

            
cur_dir = os.getcwd()

xml_file_1 = cur_dir + os.sep + "xml_test_1.xml"

xml_file_2 = cur_dir + os.sep + "xml_test_2.xml"

class Test(unittest.TestCase):


    def setUp(self):
        with open(xml_file_1, "w") as f:
            f.write(xml_1)
        with open(xml_file_2, "w") as f:
            f.write(xml_2)


    def tearDown(self):
        os.remove(xml_file_1)
        os.remove(xml_file_2)
        


    def test_xml_1_file_import(self):
        t1 = glg.open_xml_file(xml_file_1)
        self.assertTrue(isinstance(t1, etree._ElementTree), "The variable t should be a lxml _ElementTree element but is: {}".format(t1))


    def test_xml_2_file_import(self):
        t2 = glg.open_xml_file(xml_file_2)
        self.assertTrue(isinstance(t2, etree._ElementTree), "The variable t should be a lxml _ElementTree element but is: {}".format(t2))

    def test_compare_two_elements(self):
        e1 = etree.Element("p")
        e1.text = "some text"
        e2 = etree.Element("p")
        e2.text = "some ext"
        r = glg.compare_two_elements(e1, e2)
        self.assertFalse(r, "Error: function compare_two_elements with the param ({0}, {1}) should return False, but returned: {2}".format(e1.text, e2.text, r))
        e2.text = "some text"
        r = glg.compare_two_elements(e1, e2)
        self.assertTrue(r, "Error: function compare_two_elements with the param ({0}, {1}) should return True, but returned: {2}".format(e1.text, e2.text, r))
        
    
    def test_slice_strg(self):
        pat = """<lb xml:id="lb\d" ed="\w+"/>"""
        with open(xml_file_1, "r") as f:
            strgs = glg.slice_strg(f.read(), pat)
        self.assertTrue(isinstance(strgs, list), "The variable strgs should be a list, but is: {}".format(strgs))
        for s in strgs:
            self.assertTrue(isinstance(s, str), "The variable r should be a list, but is: {}".format(s))
            
        
        #the first element contains all the xml data before the first <lb/> element
        self.assertEqual(strgs[1].strip(), """<w xml:id="w1-1" lemma="per" type="prep">per</w>""", """Error: the string {0} does not match
                                    <w xml:id="w1-1" lemma="per" type="prep">per</w>""".format(strgs[1].strip()))
        
    def test_apply_xslt(self):
        t1 = glg.open_xml_file(xml_file_1)
        x = glg.apply_xslt(t1, xslt_1)
        self.assertTrue(isinstance(x, etree._XSLTResultTree), "The variable x should be a lxml _XSLTResultTree, but is: {}".format(x))
        w13 = x.xpath("//w")[2]
        self.assertEqual("w", w13.tag, "Error: the element tag of p13 should be 'w', but is: {0}".format(w13.tag))
        self.assertEqual("w1-3", w13.attrib["{%s}id" % xml_ns], "Error: the value of attribute @xml:id should be 'w1-3', but is: {0}".format(w13.attrib["{%s}id" % xml_ns]))
        self.assertEqual("Per", w13.text, "Error: the content of the element should be the sting 'Per', but is: '{0}'".format(w13.text))
        #print(t1.xpath("//w[3]/text()"))
        #print(etree.tostring(p13))
        self.assertEqual("""<w xml:id="w1-3" lemma="per" type="prep">Per</w>""", etree.tostring(w13).strip(), """Error: the converstion of p13
                            to string should result in the string '<w xml:id="w1-3" lemma="per" type="prep">Per</w>', but is: '{0}'""".format(etree.tostring(w13).strip()))

    def test_generate_valid_xml_line(self):
        t1 = glg.open_xml_file(xml_file_1)

        lbs = t1.xpath("//lb")
        xml_strg = etree.tostring(t1)
        lst = []

        for idx, lb in enumerate(lbs):
            lb1 = lb
            print (idx)
            print (idx < len(lbs))
            if idx < len(lbs)-1:
                lb2 = lbs[idx+1]
                rest_strg = glg.slice_strg(xml_strg, etree.tostring(lb1))[1]
                line_strg = glg.slice_strg(rest_strg, etree.tostring(lb2))[0]
                lst.append(glg.generate_valid_xml_line(line_strg, lb1, lb2))
            elif idx == len(lbs)-1:
                rest_strg = glg.slice_strg(xml_strg, etree.tostring(lb1))[1]
                lst.append(glg.generate_valid_xml_line(rest_strg, lb1))
        
        print(lst)
        
        
    

if __name__ == "__main__":
    unittest.main()
