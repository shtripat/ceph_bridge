class RequestStateError(Exception):
    def __init___(self, err):
        self.message = "Request state error. Error:" + \
                       " %s".format(err)
