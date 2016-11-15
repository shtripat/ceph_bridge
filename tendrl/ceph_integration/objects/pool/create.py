class Create(object):
    def run(self, parameters):
        attrs = dict(name=parameters['Pool.poolname'],
                     pg_num=parameters['Pool.pg_num'],
                     min_size=parameters['Pool.min_size'])
        # need fsid
        self.parameters['crud'].create()