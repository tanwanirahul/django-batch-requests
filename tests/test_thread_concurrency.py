'''
@author: Rahul Tanwani

@summary: Test cases to make sure sequential execution and concurrent execution return
          the same response.
'''
import json
from tests.test_base import TestBase
from batch_requests.settings import br_settings
from batch_requests.concurrent.executor import ThreadBasedExecutor


class TestThreadConcurrency(TestBase):
    '''
        Tests sequential and concurrent execution.
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

    def test_thread_concurrency_response(self):
        '''
            Make a request with sequential and thread based executor and compare
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
        br_settings.executor = ThreadBasedExecutor(self.number_workers)
        threaded_batch_requests = self.make_multiple_batch_request([get_req, post_req, put_req])

        self.assertEqual(batch_requests.content, threaded_batch_requests.content, "Sequential and concurrent response not same!")
