'''
@author: Rahul Tanwani

@summary: Test cases to make sure sequential execution and process based concurrent execution return
          the same response.
'''
from tests.test_concurrency_base import TestBaseConcurrency
from batch_requests.concurrent.executor import ProcessBasedExecutor


class TestProcessConcurrency(TestBaseConcurrency):
    '''
        Tests sequential and concurrent process based execution.
    '''
    def get_executor(self):
        '''
            Returns the executor to use for running tests defined in this suite.
        '''
        return ProcessBasedExecutor(self.number_workers)

    def test_thread_concurrency_response(self):
        '''
            Make a request with sequential and process based concurrent executor and compare
            the response.
        '''
        self.compare_seq_and_concurrent_req()

    def test_duration(self):
        '''
            Compare that running tests with ProcessBasedConcurreny return faster than running
            them sequentially.
        '''
        self.compare_seq_concurrent_duration()
