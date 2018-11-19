from tabulator import Loader

import boto3


class S3Loader(Loader):
    options = []

    def __init__(self, bytes_sample_size, **options):
        pass


    def load(self, source, mode='t', encoding=None):
        # load logic
        pass

# with Stream(source, custom_loaders={'custom': CustomLoader}) as stream:
#   stream.read()


class GSLoader(Loader):
    options = []

    def __init__(self, bytes_sample_size, **options):
        pass


    def load(self, source, mode='t', encoding=None):
        # load logic
        pass


