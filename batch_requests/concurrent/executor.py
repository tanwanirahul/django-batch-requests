'''
Created on Feb 20, 2016

@author: Rahul Tanwani
'''
from abc import ABCMeta


class Executor(object):
    '''
        Based executor class to encapsulate the job execution.
    '''
    __metaclass__ = ABCMeta

    def execute(self, requests, resp_generator, *args, **kwargs):
        '''
            Calls the resp_generator for all the requests in parallel in an asynchronous way.
        '''
        result_futures = [self.executor_pool.submit(resp_generator, req, *args, **kwargs) for req in requests]
        resp = [res_future.result() for res_future in result_futures]
        return resp


class SequentialExecutor(Executor):
    '''
        Executor for executing the requests sequentially.
    '''

    def execute(self, requests, resp_generator, *args, **kwargs):
        '''
            Calls the resp_generator for all the requests in sequential order.
        '''
        return [resp_generator(request) for request in requests]
