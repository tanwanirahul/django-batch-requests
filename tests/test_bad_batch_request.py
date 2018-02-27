'''
@author: Rahul Tanwani

@summary: Test cases to check  the behavior when the batch request is
          not constructed properly.
'''
import json

from django.test import TestCase


class TestBadBatchRequest(TestCase):

    '''
        Check the behavior of bad batch request.
    '''

    def _batch_request(self, method, path, data, headers={}):
        '''
            Prepares a batch request.
        '''
        return {"url": path, "method": method, "headers": headers, "body": data}

    def test_invalid_http_method(self):
        '''
            Make a batch request with invalid HTTP method.
        '''
        resp = self.client.post("/api/v1/batch/", json.dumps({'batch': [self._batch_request("select", "/views", "", {})]}),
                                content_type="application/json")

        self.assertEqual(resp.status_code, 400, "Method validation is broken!")
        self.assertEqual(resp.content.lower(), b"invalid request method.", "Method validation is broken!")

    def test_missing_http_method(self):
        '''
            Make a batch request without HTTP method.
        '''
        resp = self.client.post("/api/v1/batch/", json.dumps({'batch': [{"body": "/views"}]}), content_type="application/json")

        self.assertEqual(resp.status_code, 400, "Method & URL validation is broken!")
        self.assertEqual(resp.content.lower(), b"request definition should have url, method defined.",
                         "Method validation is broken!")

    def test_missing_url(self):
        '''
            Make a batch request without the URL.
        '''
        resp = self.client.post("/api/v1/batch/", json.dumps({'batch': [{"method": "get"}]}), content_type="application/json")

        self.assertEqual(resp.status_code, 400, "Method & URL validation is broken!")
        self.assertEqual(resp.content.lower(), b"request definition should have url, method defined.",
                         "Method validation is broken!")

    def test_invalid_batch_request(self):
        '''
            Make a batch request without wrapping in the list.
        '''
        resp = self.client.post("/api/v1/batch/", json.dumps({'batch': {"method": "get", "url": "/views/"}}),
                                content_type="application/json")

        print(resp.content)
        self.assertEqual(resp.status_code, 400, "Batch requests should always be in list.")
        self.assertEqual(resp.content.lower(), b"the body of batch request should always be list!",
                         "List validation is broken!")

    def test_view_that_raises_exception(self):
        '''
            Make a batch request to a view that raises exception.
        '''
        resp = self.client.post("/api/v1/batch/", json.dumps({'batch': [{"method": "get", "url": "/exception/"}]}),
                                content_type="application/json")

        resp = json.loads(resp.content)[0]
        self.assertEqual(resp['status_code'], 500, "Exceptions should return 500.")
        self.assertEqual(resp['body'].lower(), "exception", "Exception handling is broken!")
