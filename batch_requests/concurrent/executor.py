'''
Created on Feb 20, 2016

@author: Rahul Tanwani
'''
from abc import ABCMeta
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor


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


class ThreadBasedExecutor(Executor):
    '''
        An implementation of executor using threads for parallelism.
    '''
    def __init__(self, num_workers):
        '''
            Create a thread pool for concurrent execution with specified number of workers.
        '''
        self.executor_pool = ThreadPoolExecutor(num_workers)


class ProcessBasedExecutor(Executor):
    '''
        An implementation of executor using process(es) for parallelism.
    '''
    def __init__(self, num_workers):
        '''
            Create a process pool for concurrent execution with specified number of workers.
        '''
        self.executor_pool = ProcessPoolExecutor(num_workers)
