import unittest
import kissxml


class TestSimpleXML(unittest.TestCase):
    def assertXMLHasProperties(self, xml, properties):
        for propname, value in properties.iteritems():
            if isinstance(value, tuple):
                value, attrs = value
            else:
                value, attrs = value, {}
            actual = getattr(xml, propname)
            if isinstance(actual, kissxml.XMLTree):
                self.assertTrue(isinstance(value, dict), 'Expected dictionary, got %s (value: %s)' % (type(actual), actual))
                self.assertXMLHasProperties(actual, value)
            elif isinstance(actual, list):
                for idx, item in enumerate(actual):
                    self.assertEquals(value[idx], str(item), 'Expected node value "%s", got "%s"' % (value[idx], item))
            else:
                self.assertEquals(value, str(actual), 'Expected node value "%s", got "%s"' % (value, actual))
            for attrname, attrvalue in attrs.iteritems():
                actualattr = getattr(xml, propname)[attrname]
                self.assertEquals(attrvalue, actualattr, 'Expected attribute value "%s", got "%s"' % (attrvalue, actualattr))

    def test_kissxml(self):
        for name, vals in self.get_tests().iteritems():
            self.assertXMLHasProperties(kissxml.parsestring(vals[1]), vals[0])

    def get_tests(self):
        # Dictionary of tests, keyed by test name.
        # Values: (<expected_value>, <xml>)
        #   <expected_value>: dict(<node>=<value>) or dict(<node>=(<value>,<attrs>)).
        return {
            'basic': ({'name': 'Joe Stump', 'hair': ('Brown', {'style': 'buzzed'}), 'like': ['Beer', 'Bikes', 'Computers']}, '<?xml version="1.0"?><test><name>Joe Stump</name><hair style="buzzed">Brown</hair><like>Beer</like><like>Bikes</like><like>Computers</like></test>'),
            'subitem_name_conflict': ({'type': 'Foo', 'properties': {'type': 'properties', 'foo': 'bar'}}, '<?xml version="1.0"?><item><type>Foo</type><properties><type>properties</type><foo>bar</foo></properties></item>')
        }


class TestXMLNodeComparison(unittest.TestCase):
    def setUp(self):
        self.xml = kissxml.parsestring('''<?xml version="1.0" encoding="UTF-8"?>
            <test>
                <string>Test</string>
                <integer>123</integer>
            </test>
            ''')

    def test_strings(self):
        self.assertEquals('Test', self.xml.string)
        self.assertEquals(u'Test', self.xml.string)
        self.assertNotEquals(123, self.xml.string)

    def test_integers(self):
        self.assertNotEquals('Test', self.xml.integer)
        self.assertEquals(123, self.xml.integer)


class TestXMLNodeGetItem(unittest.TestCase):
    def setUp(self):
        self.xml = kissxml.parsestring('<xml test="attribute"><child></child></xml>')

    def test_in(self):
        self.assertTrue('test' in self.xml)
        self.assertFalse('test-non-existant' in self.xml)

    def test_key(self):
        self.assertEquals(self.xml['test'], 'attribute')
        self.assertEquals(self.xml['test-non-existant'], None)


if __name__ == '__main__':
    unittest.main()
