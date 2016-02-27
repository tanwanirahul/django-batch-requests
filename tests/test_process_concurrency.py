'''
@author: Rahul Tanwani

@summary: Test cases to make sure sequential execution and process based concurrent execution return
          the same response.
'''
from tests.test_concurrency_base import TestBaseConcurrency
from batch_requests.concurrent.executor import ProcessBasedExecutor


class TestThreadConcurrency(TestBaseConcurrency):
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
