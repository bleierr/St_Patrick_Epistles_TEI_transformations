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
                    <lb xml:id="lb1"/>
                    <w xml:id="w1-1" lemma="per" type="prep">per</w>
                    <lb xml:id="lb2"/>
                    <w xml:id="w1-2" lemma="nomen" type="noun">nomen</w>
                    <lb xml:id="lb3"/>
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
                    <lb xml:id="lb1"/>
                    <w xml:id="w2-1" lemma="per" type="prep">per</w>
                    <w xml:id="w2-2" lemma="Patricius" type="name">Patricius</w>
                    <lb xml:id="lb2"/>
                    <w xml:id="w2-3" lemma="nomen" type="noun">nominis</w>
                    <lb xml:id="lb3"/>
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
        e2.text = "som ext"
        r = glg.compare_two_elements(e1, e2)
        self.assertFalse(r, "Error: function compare_two_elements with the param ({0}, {1}) should return False, but returned: {2}".format(e1.text, e2.text, r))
        e2.text = "some text"
        r = glg.compare_two_elements(e1, e2)
        self.assertTrue(r, "Error: function compare_two_elements with the param ({0}, {1}) should return True, but returned: {2}".format(e1.text, e2.text, r))
        
    
    def test_slice_strg(self):
        pat = """<lb xml:id="lb\d"/>"""
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
        xslt_root = etree.XML(xslt_1)
        x = glg.apply_xslt(t1, xslt_root)
        self.assertTrue(isinstance(x, etree._XSLTResultTree), "The variable x should be a lxml _XSLTResultTree, but is: {}".format(x))
        w13 = x.xpath("//w")[2]
        self.assertEqual("w", w13.tag, "Error: the element tag of p13 should be 'w', but is: {0}".format(w13.tag))
        self.assertEqual("w1-3", w13.attrib["{%s}id" % xml_ns], "Error: the value of attribute @xml:id should be 'w1-3', but is: {0}".format(w13.attrib["{%s}id" % xml_ns]))
        self.assertEqual("Per", w13.text, "Error: the content of the element should be the sting 'Per', but is: '{0}'".format(w13.text))
        #print(t1.xpath("//w[3]/text()"))
        #print(etree.tostring(p13))
        self.assertEqual("""<w xml:id="w1-3" lemma="per" type="prep">Per</w>""", etree.tostring(w13).strip(), """Error: the converstion of p13
                            to string should result in the string '<w xml:id="w1-3" lemma="per" type="prep">Per</w>', but is: '{0}'""".format(etree.tostring(w13).strip()))

    def test_split_on_lbs(self):
        t1 = glg.open_xml_file(xml_file_1)

        lbs = t1.xpath("//lb")
        xml_strg = etree.tostring(t1)
        d = glg.split_on_lbs(xml_strg)

        #test amount lbs in dictionary
        num_lbs = len(d)
        exp = 3
        self.assertEqual(exp, num_lbs, "Error: "
                        "expected result was the the number '{0}',"
                        "but was: {1}".format(exp, num_lbs))
        for lb in lbs:
            in_lst = lb.attrib["{%s}id" % xml_ns] in d
            self.assertTrue(in_lst, "Error: "
                        "the key '{0}' is not in the dictionary of"
                        " linebreaks".format(lb.attrib["{%s}id" % xml_ns]))
        res = d["lb3"]
        self.assertEqual("line", res.tag, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format("line", res.tag))
        #test amount child elements
        res_num_child = len(res.getchildren())
        exp = 3
        self.assertEqual(exp, res_num_child, "Error: "
                        "expected result was the the number '{0}',"
                        "but was: {1}".format(exp, res_num_child))
        #test text of first child
        res_w = res.getchildren()[0]
        res_w_text = res_w.getchildren()[0].tail
        exp = "er"
        self.assertEqual(exp, res_w_text, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_text))
        #test child of first child
        res_w = res.getchildren()[0]
        res_w_g = res_w.getchildren()[0]
        res_w_g_text = res_w_g.text
        exp = "P"
        self.assertEqual(exp, res_w_g_text, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_g_text))
        #test attr @lemma
        res_w_lemma = res.getchildren()[0].attrib["lemma"]
        exp = "per"
        self.assertEqual(exp, res_w_lemma, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_lemma))



        

    def test_generate_valid_xml_line(self):
        t1 = etree.fromstring("""<text>
                                <lb/>
                                <w xml:id="w1" lemma="pro" type="prep">First word</w>
                                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
                                <lb/>
                                </text>""")

        lbs = t1.xpath("//lb")
        strg = """<w xml:id="w1" lemma="pro" type="prep">First word</w>
                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
                """
                                
        res = etree.fromstring(glg.generate_valid_xml_line(strg, lbs[0], lbs[1]))
        """The expected result is:
        <line>
            <w xml:id="w1" lemma="pro" type="prep">First word</w>
            <w xml:id="w2" lemma="venire" type="verb">Second word</w>
        </line>
        """
        self.assertEqual("line", res.tag, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format("line", res.tag))
        #test amount child elements
        res_num_child = len(res.getchildren())
        exp = 2
        self.assertEqual(exp, res_num_child, "Error: "
                        "expected result was the the number '{0}',"
                        "but was: {1}".format(exp, res_num_child))
        #test text of first child
        res_w_text = res.getchildren()[0].text
        exp = "First word"
        self.assertEqual(exp, res_w_text, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_text))
        #test attr @lemma
        res_w_lemma = res.getchildren()[0].attrib["lemma"]
        exp = "pro"
        self.assertEqual(exp, res_w_lemma, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_lemma))
        ##### test lb in word #####
        t2 = etree.fromstring("""<text>
                                <w xml:id="w1" lemma="pro" type="prep">First<lb/>word</w>
                                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
                                <lb/>
                                </text>""")

        lbs = t2.xpath("//lb")
        strg = """word</w>
                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
                """
        res = etree.fromstring(glg.generate_valid_xml_line(strg, lbs[0], lbs[1]))
        """Expected result is:
            <line>
                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
            </line>
            """
        
        #test amount child elements
        res_num_child = len(res.getchildren())
        exp = 1
        self.assertEqual(exp, res_num_child, "Error: "
                        "expected result was the the number '{0}',"
                        "but was: {1}".format(exp, res_num_child))
        #test text of first child
        res_w_text = res.getchildren()[0].text
        exp = "Second word"
        self.assertEqual(exp, res_w_text, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_text))
        #test attr @lemma
        res_w_lemma = res.getchildren()[0].attrib["lemma"]
        exp = "venire"
        self.assertEqual(exp, res_w_lemma, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_lemma))

        ##### test end linebreak #####
        t3 = etree.fromstring("""<tei><text>
                                <w xml:id="w1" lemma="pro" type="prep">First<lb/>word</w>
                                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
                                </text></tei>""")
        lbs = t3.xpath("//lb")
        strg = """word</w>
                <w xml:id="w2" lemma="venire" type="verb">Second word</w></text></tei>
                """
        res = etree.fromstring(glg.generate_valid_xml_line(strg, lbs[0]))
        """Expected result is:
            <line>
                <w xml:id="w2" lemma="venire" type="verb">Second word</w>
            </line>
            """
        #test amount child elements
        res_num_child = len(res.getchildren())
        exp = 1
        self.assertEqual(exp, res_num_child, "Error: "
                        "expected result was the the number '{0}',"
                        "but was: {1}".format(exp, res_num_child))
        #test text of first child
        res_w_text = res.getchildren()[0].text
        exp = "Second word"
        self.assertEqual(exp, res_w_text, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_text))
        #test attr @lemma
        res_w_lemma = res.getchildren()[0].attrib["lemma"]
        exp = "venire"
        self.assertEqual(exp, res_w_lemma, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res_w_lemma))

        

    def test_remove_closing_tag(self):
        strg = "<w>remove the text element</w></text>"

        result_strg = glg.remove_closing_tag(strg)

        self.assertEqual("<w>remove the text element</w>", result_strg, "Error: "
                        "expected result was the string '<w>remove the text element</w>',"
                        "but was: {0}".format(result_strg))

        strg2 = ""
        res = glg.remove_closing_tag(strg2)
        exp = ""
        self.assertEqual(res, exp, "Error: "
                        "expected result was the string '{0}',"
                        "but was: {1}".format(exp, res))
        

    def test_compare_root_element(self):
        #trailing end-tag without start tag
        strg = """<w xml:id="w1" lemma="pro" type="prep">First<lb/>word</w></text>"""
        res = glg.compare_root_element(strg)
        self.assertFalse(res, "Error: "
                        "expected result for string '<w>remove the text element</w></text>' was False,"
                        "but was: {0}".format(res))
        #correct root element
        strg = """<text type="root"><w xml:id="w1" lemma="pro" type="prep">First<lb/>word</w></text>"""
        res = glg.compare_root_element(strg)
        self.assertTrue(res, "Error: "
                        "expected result for string '<text><w>remove the text element</w></text>' was True,"
                        "but was: {0}".format(res))
        #only one element with text
        strg = """<w xml:id="w2" lemma="venire" type="verb">Second word</w>"""
        res = glg.compare_root_element(strg)
        self.assertTrue(res, "Error: "
                        "expected result for string '<w xml:id=\"w2\" lemma=\"venire\" type=\"verb\">Second word</w>' was True,"
                        "but was: {0}".format(res))
        #empty string
        strg = ""
        res = glg.compare_root_element(strg)
        self.assertTrue(res, "Error: "
                        "expected result for an empty string was True,"
                        "but was: {0}".format(res))
        
    def test_similar_element_in_lst(self):
        line = """<line>
            <w xml:id="w1" lemma="pro" type="prep">pro</w>
            <w xml:id="w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="w3" lemma="a" type="prep">a</w>
            <w xml:id="w4" lemma="pre" type="prep">pre</w>
            <w xml:id="w5" lemma="venire" type="verb">uenio</w>
            </line>"""
        t = etree.fromstring(line)
        lst = [w for w in t]
        ele = etree.fromstring("""<w xml:id="w4" lemma="pre" type="prep">pre</w>""")
        
        res = glg.similar_element_in_lst(lst, ele)
        self.assertEqual(res, [3], "Error: testing the word 'pre'"
                        "expected is the number 1, but got {0}".format(res))
        
        ele = etree.fromstring("""<w xml:id="w2" lemma="venire" type="verb">uentum</w>""")
        
        res = glg.similar_element_in_lst(lst, ele)
        self.assertEqual(res, [1, 4], "Error: testing the @lemma "
                        "expected is the number 1, but got {0}".format(res))
        
        ele = etree.fromstring("""<w xml:id="w2" lemma="unknown" type="verb">uentum</w>""")
        
        res = glg.similar_element_in_lst(lst, ele)
        self.assertEqual(res, [1, 4], "Error: testing if @lemma='unknown' "
                        "expected is the number 1, but got {0}".format(res))
        #Error handling if None is provided
        res = glg.similar_element_in_lst(lst, None)
        self.assertEqual(res, None, "Error: testing if wrong type of parameter is detected "
                        "expected is the return value 'None', but got {0}".format(res))
        
    
    def test_compare_lines(self):
        line1 = etree.fromstring("""<line>
            <w xml:id="l1w1" lemma="pro" type="prep">pro</w>
            <w xml:id="l1w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l1w3" lemma="a" type="prep">a</w>
            <w xml:id="l1w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l1w5" lemma="venire" type="verb">uenio</w>
            </line>""")
        
        line2 = etree.fromstring("""<line>
            <w xml:id="l2w1" lemma="pro" type="prep">pro</w>
            <w xml:id="l2w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l2w3" lemma="a" type="prep">a</w>
            <w xml:id="l2w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l2w5" lemma="dico" type="verb">dico</w>
            </line>""")
            
        line3 = etree.fromstring("""<line>
            <w xml:id="l3w1" lemma="patricius" type="name">patricius</w>
            <w xml:id="l3w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l3w3" lemma="a" type="prep">a</w>
            <w xml:id="l3w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l3w5" lemma="venire" type="verb">uenio</w>
            </line>""")
        
        l = [line1, line2, line3]
        
        id = "line x"
        
        res = glg.compare_lines(id, *l)
        
        self.assertEqual(len(res[0]), 1, "Error: testing if the length of the first list (word 'patricius') "
                        "expected is the number 1, but got {0}".format(len(res[0])))
        
        self.assertEqual(len(res[4]), 3, "Error: testing if the length of the fifth list (word 'pre') "
                        "expected is the number 3, but got {0}".format(len(res[2])))
        for lst in res[4]:
            for e in lst:
                self.assertTrue(e.text, "pre", "Error: testing if all elements in list 4 contain the same text, "
                        "all should be 'pre', but got {0}".format(e))
                
        #Test multiple times same word in line, venio - venit
        self.assertEqual(len(res[2]), 3, "Error: testing if the length of the third list (word 'uenit')"
                        "expected is the number 3, but got {0}".format(len(res[2])))
        self.assertEqual(len(res[6]), 2, "Error: testing if the length of the seventh list (word 'uenio')"
                        "expected is the number 2, but got {0}".format(len(res[6])))
        self.assertEqual(res[5][0].text, "dico", "Error: testing if the text of the sixth list (word 'dico')"
                        "expected is the string 'dico, but got {0}".format(res[5][0].text))
        

    def test_generate_linking_groups(self):
        line1 = etree.fromstring("""<line>
            <w xml:id="l1w1" lemma="pro" type="prep">pro</w>
            <w xml:id="l1w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l1w3" lemma="a" type="prep">a</w>
            <w xml:id="l1w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l1w5" lemma="venire" type="verb">uenio</w>
            </line>""")
        
        line2 = etree.fromstring("""<line>
            <w xml:id="l2w1" lemma="pro" type="prep">pro</w>
            <w xml:id="l2w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l2w3" lemma="a" type="prep">a</w>
            <w xml:id="l2w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l2w5" lemma="dico" type="verb">dico</w>
            </line>""")
        
        res = glg.compare_lines(line1, line2)
        
        s = glg.generate_linking_groups(res)
        
    def test_is_correct_line(self):
        line1 = etree.fromstring("""<line>
            <w xml:id="l1w1" lemma="pro" type="prep">pro</w>
            <w xml:id="l1w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l1w3" lemma="a" type="prep">a</w>
            <w xml:id="l1w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l1w5" lemma="venire" type="verb">uenio</w>
            </line>""")
        line2 = etree.fromstring("<line></line>")
        line3 = ""
        line4 = etree.fromstring("""<line>
            <seg xml:id="l1w1" lemma="pro" type="prep">pro</seg>
            <w xml:id="l1w2" lemma="venire" type="verb">uenit</w>
            <w xml:id="l1w3" lemma="a" type="prep">a</w>
            <w xml:id="l1w4" lemma="pre" type="prep">pre</w>
            <w xml:id="l1w5" lemma="venire" type="verb">uenio</w>
            </line>""")
        
        res = glg.is_correct_line(line1)
        self.assertTrue(res, "Error: the first line resulted to False, but should be True.")
        res = glg.is_correct_line(line2)
        self.assertFalse(res, "Error: the second line resulted to True, but should be False.")
        res = glg.is_correct_line(line3)
        self.assertFalse(res, "Error: the third line resulted to True, but should be False.")
        res = glg.is_correct_line(line4)
        self.assertFalse(res, "Error: the fourth line resulted to True, but should be False.")


if __name__ == "__main__":
    unittest.main()
