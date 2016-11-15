class Delete(object):
    def run(self, parameters):
        parameters['crud'].delete(parameters['Pool.pool_id'])
        return True
