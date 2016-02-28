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

        seq_responses = json.loads(batch_requests.content)
        conc_responses = json.loads(threaded_batch_requests.content)

        for idx, seq_resp in enumerate(seq_responses):
            self.assertDictEqual(seq_resp, conc_responses[idx], "Sequential and concurrent response not same!")

    def compare_seq_concurrent_duration(self):
        '''
            Makes the batch requests run sequentially and in parallel and asserts
            parallelism to reduce the total duration time.
        '''
        # Make a batch call for GET, POST and PUT request.
        sleep_2_seconds = ("get", "/sleep/?seconds=1", '', {})
        sleep_1_second = ("get", "/sleep/?seconds=1", '', {})

        # Get the response for a batch request.
        batch_requests = self.make_multiple_batch_request([sleep_2_seconds, sleep_1_second, sleep_2_seconds])
        seq_duration = int(batch_requests._headers.get(br_settings.DURATION_HEADER_NAME)[1])

        # Update the executor settings.
        br_settings.executor = self.get_executor()
        concurrent_batch_requests = self.make_multiple_batch_request([sleep_2_seconds, sleep_1_second, sleep_2_seconds])
        concurrency_duration = int(concurrent_batch_requests._headers.get(br_settings.DURATION_HEADER_NAME)[1])

        self.assertLess(concurrency_duration, seq_duration, "Concurrent requests are slower than running them in sequence.")
