'''
@author: Rahul Tanwani

@summary: Contains base test case for concurrency related tests.
'''
import json

from tests.test_base import TestBase
from batch_requests.settings import br_settings


class TestBaseConcurrency(TestBase):
    '''
        Base class for all reusable test methods related to concurrency.
    '''
    # FIXME: Find the better way to manage / update settings.
    def setUp(self):
        '''
            Change the concurrency settings.
        '''
        self.number_workers = 10
        self.orig_executor = br_settings.executor

    def tearDown(self):
        # Restore the original batch requests settings.
        br_settings.executor = self.orig_executor

    def compare_seq_and_concurrent_req(self):
        '''
            Make a request with sequential and concurrency based executor and compare
            the response.
        '''
        data = json.dumps({"text": "Batch"})

        # Make a batch call for GET, POST and PUT request.
        get_req = ("get", "/views/", '', {})
        post_req = ("post", "/views/", data, {"content_type": "text/plain"})
        put_req = ("put", "/views/", data, {"content_type": "text/plain"})

        # Get the response for a batch request.
        batch_requests = self.make_multiple_batch_request([get_req, post_req, put_req])

        # FIXME: Find the better way to manage / update settings.
        # Update the settings.
        br_settings.executor = self.get_executor()
        threaded_batch_requests = self.make_multiple_batch_request([get_req, post_req, put_req])

        self.assertEqual(batch_requests.content, threaded_batch_requests.content, "Sequential and concurrent response not same!")
