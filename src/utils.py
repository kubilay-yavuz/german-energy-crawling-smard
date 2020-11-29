import time
from dateutil import tz
from datetime import datetime


def timer(print_args=True):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = get_local_current_time()
            process_start = time.process_time()
            if print_args:
                print('Function {}, started at {} with parameters args: {}, kwargs: {}'
                      .format(function.__name__, start, args, kwargs))
            else:
                print('Function {}, started at {}'
                      .format(function.__name__, start))
            result = function(*args, **kwargs)
            process_end = time.process_time()
            end = get_local_current_time()
            total_time = (end - start).seconds
            cpu_time = round(process_end - process_start, 2)
            io_time = total_time - cpu_time
            print('Function {}, ended at {}. TOTAL TIME: {}, CPU TIME: {}, IO TIME: {} seconds.'
                  .format(function.__name__, end, total_time, cpu_time, io_time))
            return result

        return wrapper

    return decorator


def cache(func):
    def wrapper(self, *args, **kwargs):
        __hash_name__ = func.__name__ + str(kwargs) + str(args)
        if __hash_name__ not in self.func_dict.keys():
            self.func_dict[__hash_name__] = func(self, *args, **kwargs)
        return self.func_dict[__hash_name__]

    return wrapper


def get_local_current_time(tz_name='Europe/Istanbul'):
    time_zone = tz.gettz(tz_name)
    return datetime.now(time_zone).replace(tzinfo=None)
