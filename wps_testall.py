import os
import time
import json
import requests
from lxml import etree
from pywps import Process, get_format, configuration
from pywps import ComplexOutput

# Example usage:
# localhost:8009/pywps?service=WPS&request=execute&version=1.0.0&identifier=testall&DataInputs=

output_path = configuration.get_config_value('server', 'outputpath')
json_format = get_format('JSON')
wps_host = os.environ['WPS_HOST']


class WPSError(Exception):
    pass


def wpsread(xml_text):
    root_xml = etree.fromstring(xml_text)
    # check that this is a wps response
    if not (root_xml.tag.split('}')[-1] == 'ExecuteResponse'):
        raise TypeError("Not an ExecuteResponse xml file.")
    outputs_lvl = []
    for item in root_xml.iterchildren():
        outputs_lvl.append(item)
    status_lvl = []
    for item in outputs_lvl[1].iterchildren():
        status_lvl.append(item)
        if not (status_lvl[0].tag.split('}')[-1] == 'ProcessSucceeded'):
            raise WPSError("Did not get ProcessSucceeded response.")
    single_output_lvl = []
    for item in outputs_lvl[2].iterchildren():
        single_output_lvl.append(item)
    d = {}
    for single_output in single_output_lvl:
        output_info = []
        for item in single_output.iterchildren():
            output_info.append(item)
        for info in output_info:
            if info.tag.split('}')[-1] == 'Identifier':
                d[info.text] = {}
                identifier = info.text
        for info in output_info:
            if info.tag.split('}')[-1] == 'Data':
                data_lvl = []
                for item in info.iterchildren():
                    data_lvl.append(item)
                d[identifier] = data_lvl[0].text
    return d


class TestAll(Process):
    def __init__(self):
        outputs = [ComplexOutput('tests_results',
                                 'Tests results',
                                 supported_formats=[json_format],
                                 as_reference=True)]

        super(TestAll, self).__init__(
            self._handler,
            identifier='testall',
            title='Test all processes',
            version='0.1',
            inputs=[],
            outputs=outputs)

    def _handler(self, request, response):
        test_results = {}

        # test_simplesttest
        for i in range(10):
            try:
                r = requests.get('http://{0}/pywps?service=WPS&request=execute&version=1.0.0&identifier=simplesttest&DataInputs=one_integer=42'.format(wps_host))
                if r.status_code == 500:
                    test_results['simplesttest'] = 'FAIL: 500 error.'
                    break
                wps_response = wpsread(r.text)
                if wps_response['repeated_integer'] == '42':
                    test_results['simplesttest'] = 'SUCCESS'
                else:
                    test_results['simplesttest'] = 'FAIL: {0}'.format(
                        wps_response['repeated_integer'])
            except Exception as e:
                test_results['simplesttest'] = 'FAIL: {0}'.format(str(e))
            time.sleep(1)

        # output tests results
        time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        output_file_name = "tests_results_%s.json" % (time_str,)
        output_file = os.path.join(output_path, output_file_name)
        f1 = open(output_file, 'w')
        f1.write(json.dumps(test_results))
        f1.close()
        response.outputs['tests_results'].file = output_file
        response.outputs['tests_results'].output_format = json_format
        return response
