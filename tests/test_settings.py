'''
@author: Rahul Tanwani

@summary: Test cases for configured settings.
'''
import json

from django.conf import settings
from batch_requests.settings import br_settings
from django.test import TestCase


class TestSettings(TestCase):

    '''
        Tests cases to make sure settings are working as configured.
    '''

    def test_max_limit(self):
        '''
            Test max_limit should enforced.
        '''
        data = json.dumps({"text": "test max limit"})

        # Make a batch call for requests > MAX_LIMIT (3).
        get_req = ("get", "/views/", '', {})
        post_req = ("post", "/views/", data, {"content_type": "text/plain"})
        put_req = ("put", "/views/", data, {"content_type": "text/plain"})
        get_req2 = ("get", "/views/", '', {})

        # Get the response for a batch request.
        batch_requests = self._make_multiple_batch_request([get_req, post_req, put_req, get_req2])

        # Assert we get a bad request.
        self.assertEqual(batch_requests.status_code, 400, "MAX_LIMIT setting not working.")
        self.assertTrue(batch_requests.content.lower().startswith("you can batch maximum of"))

    def test_custom_header(self):
        '''
            Tests the custom header to be present in individual request.
        '''
        # Define the header and its value
        header = "X_CUSTOM"
        value = "custom value"

        # Make a batch request querying for that particular header.
        batch_req = self._make_a_batch_request("get", "/echo/?header=HTTP_%s" % (header), "", headers={header: value})
        batch_resp = json.loads(batch_req.content)[0]

        self.assertEqual(batch_resp['body'], value, "Custom header not working")

    def test_use_https_setting(self):
        '''
            Tests the scheme for individual requests to be https as defined in settings.
        '''
        # Define the header and its value
        header = "scheme"
        value = "https"

        # Make a batch request querying for that particular header.
        batch_req = self._make_a_batch_request("get", "/echo/?header=%s" % (header), "", headers={})
        batch_resp = json.loads(batch_req.content)[0]

        self.assertEqual(batch_resp['body'], value, "Custom header not working")

    def test_http_default_content_type_header(self):
        '''
            Tests the default content type to be as per settings.DEFAULT_CONTENT_TYPE.
        '''
        data = json.dumps({"text": "content type"})

        # Define the header and its value
        header = "CONTENT_TYPE"
        value = settings.BATCH_REQUESTS.get("DEFAULT_CONTENT_TYPE")

        # Make a batch request querying for that particular header.
        batch_req = self._make_a_batch_request("post", "/echo/?header=%s" % (header), data, headers={})
        batch_resp = json.loads(batch_req.content)[0]

        self.assertEqual(batch_resp['body'], value, "Default content type not working.")

    def test_duration_header(self):
        '''
            Tests that duration header be present in all the requests.
        '''
        # Make a batch call to any API.
        get_req = ("get", "/views/", '', {})

        # Get the response for a batch request.
        batch_requests = self._make_multiple_batch_request([get_req])

        # Make sure we have the header present in enclosing batch response and all individual responses.
        self.assertIn(br_settings.DURATION_HEADER_NAME, batch_requests._headers,
                      "Enclosing batch request does not contain duration header.")

        self.assertIn(br_settings.DURATION_HEADER_NAME, json.loads(batch_requests.content)[0]['headers'],
                      "Individual batch request does not contain duration header.")

    def _batch_request(self, method, path, data, headers={}):
        '''
            Prepares a batch request.
        '''
        return {"url": path, "method": method, "headers": headers, "body": data}

    def _make_a_batch_request(self, method, url, body, headers={}):
        '''
            Makes a batch request using django client.
        '''
        return self.client.post("/api/v1/batch/", json.dumps([self._batch_request(method, url, body, headers)]),
                                content_type="application/json")

    def _make_multiple_batch_request(self, requests):
        '''
            Makes multiple batch request using django client.
        '''
        batch_requests = [self._batch_request(method, path, data, headers) for method, path, data, headers in requests]
        return self.client.post("/api/v1/batch/", json.dumps(batch_requests), content_type="application/json")
