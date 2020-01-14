import time
import logging

# 打印执行时间
def func_timer(func):
    def wrapper_timer(*args,**kwargs):
        t_begin = time.time()
        result = func(*args,**kwargs)
        t_end = time.time()
        print('Function [{}] Processing Duration: {:.4}(s).'.format(func.__name__,float(t_end - t_begin)))
        return result
    return wrapper_timer

#打印log信息
def logger(log_path):
    def func_log(func):
        def wrapper_log(*args,**kwargs):
            logging.basicConfig(level=logging.INFO,
                                format= '%(asctime)s %(levelname)s [%(message)s]',
                                datefmt='%Y-%m-%d %a %H:%M:%S',
                                filename=log_path,
                                filemode='a')
            logging.info(func.__name__ + ' is executing......')
            result = func(*args, **kwargs)
            logging.info(func.__name__ + ' executing finished.')
            return result
        return wrapper_log
    return func_log