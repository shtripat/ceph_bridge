import gevent.event
import traceback
import zerorpc

from salt.key import Key
import salt.config

from cthulhu.manager import config
from cthulhu.log import log
from cthulhu.manager.types import OsdMap, SYNC_OBJECT_STR_TYPE, OSD, POOL, CLUSTER, CRUSH_RULE


class NotFound(Exception):
    def __init__(self, object_type, object_id):
        self.object_type = object_type
        self.object_id = object_id

    def __str__(self):
        return "Object of type %s with id %s not found" % (self.object_type, self.object_id)


class RpcInterface(object):
    def __init__(self, manager):
        self._manager = manager

    def __getattribute__(self, item):
        """
        Wrap functions with logging
        """
        if item.startswith('_'):
            return object.__getattribute__(self, item)
        else:
            attr = object.__getattribute__(self, item)
            if callable(attr):
                def wrap(*args, **kwargs):
                    log.debug("RpcInterface >> %s(%s, %s)" % (item, args, kwargs))
                    try:
                        rc = attr(*args, **kwargs)
                        log.debug("RpcInterface << %s" % item)
                    except:
                        log.exception("RpcInterface !! %s" % item)
                        raise
                    return rc
                return wrap
            else:
                return attr

    def _fs_resolve(self, fs_id):
        try:
            return self._manager.clusters[fs_id]
        except KeyError:
            raise NotFound(CLUSTER, fs_id)

    def _osd_resolve(self, cluster, osd_id):
        osdmap = cluster.get_sync_object(OsdMap)
        if osdmap is None:
            raise NotFound(OSD, osd_id)

        for osd in osdmap['osds']:
            if osd['osd'] == osd_id:
                return osd
        raise NotFound(OSD, osd_id)

    def _pool_resolve(self, cluster, pool_id):
        osdmap = cluster.get_sync_object(OsdMap)
        if osdmap is None:
            raise NotFound(POOL, pool_id)

        for pool in osdmap['pools']:
            if pool['pool'] == pool_id:
                return pool
        raise NotFound(POOL, pool_id)

    def get_cluster(self, fs_id):
        """
        Returns a dict, or None if not found
        """
        try:
            cluster = self._manager.clusters[fs_id]
        except KeyError:
            return None
        else:
            return {
                'id': cluster.fsid,
                'name': cluster.name,
                'update_time': cluster.update_time.isoformat()
            }

    def list_clusters(self):
        result = []
        for fsid in self._manager.clusters.keys():
            result.append(self.get_cluster(fsid))
        return result

    def delete_cluster(self, fs_id):
        # Clear out records of services belonging to the cluster
        self._manager.servers.delete_cluster(fs_id)
        # Clear out records of the cluster itself
        self._manager.delete_cluster(fs_id)

    def get_sync_object(self, fs_id, object_type):
        """
        Get one of the objects that ClusterMonitor keeps a copy of from the mon, such
        as the cluster maps.

        :param fs_id: The fsid of a cluster
        :param object_type: String, one of SYNC_OBJECT_TYPES
        """
        return self._fs_resolve(fs_id).get_sync_object(SYNC_OBJECT_STR_TYPE[object_type])

    def get_derived_object(self, fs_id, object_type):
        """
        Get one of the objects that ClusterMonitor generates from the sync objects, typically
        something in a "frontend-friendly" format or augmented with extra info.

        :param fs_id: The fsid of a cluster
        :param object_type: String, name of the derived object
        """
        return self._fs_resolve(fs_id).get_derived_object(object_type)

    def update(self, fs_id, object_type, object_id, attributes):
        """
        Modify an object in a cluster.
        """
        cluster = self._fs_resolve(fs_id)

        if object_type == OSD:
            # Run a resolve to throw exception if it's unknown
            self._osd_resolve(cluster, object_id)
            if not 'id' in attributes:
                attributes['id'] = object_id

            return cluster.request_update(OSD, object_id, attributes)
        elif object_type == POOL:
            if not 'id' in attributes:
                attributes['id'] = object_id

            return cluster.request_update(POOL, object_id, attributes)
        else:
            raise NotImplementedError(object_type)

    def create(self, fs_id, object_type, attributes):
        """
        Create a new object in a cluster
        """
        cluster = self._fs_resolve(fs_id)

        if object_type == POOL:
            return cluster.request_create(POOL, attributes)
        else:
            raise NotImplementedError(object_type)

    def delete(self, fs_id, object_type, object_id):
        cluster = self._fs_resolve(fs_id)

        if object_type == POOL:
            return cluster.request_delete(POOL, object_id)
        else:
            raise NotImplementedError(object_type)

    def get(self, fs_id, object_type, object_id):
        """
        Get one object from a particular cluster.
        """

        cluster = self._fs_resolve(fs_id)
        if object_type == OSD:
            return self._osd_resolve(cluster, object_id)
        elif object_type == POOL:
            return self._pool_resolve(cluster, object_id)
        else:
            raise NotImplementedError(object_type)

    def list(self, fs_id, object_type):
        """
        Get many objects
        """

        cluster = self._fs_resolve(fs_id)
        osd_map = cluster.get_sync_object(OsdMap)
        if osd_map is None:
            return []
        if object_type == OSD:
            return osd_map['osds']
        elif object_type == POOL:
            return osd_map['pools']
        elif object_type == CRUSH_RULE:
            return osd_map['crush']['rules']
        else:
            raise NotImplementedError(object_type)

    def get_request(self, fs_id, request_id):
        """
        Get a JSON representation of a UserRequest
        """
        cluster = self._fs_resolve(fs_id)
        request = cluster.get_request(request_id)
        return {
            'id': request.id,
            'state': request.state,
            'error': request.error
        }

    def list_requests(self, fs_id):
        cluster = self._fs_resolve(fs_id)
        requests = cluster.list_requests()
        return [{'id': r.id, 'state': r.state} for r in requests]

    @property
    def salt_key(self):
        return Key(salt.config.master_config(config.get('cthulhu', 'salt_config_path')))

    def minion_status(self, status_filter):
        """
        Return a list of salt minion keys

        :param minion_status: A status, one of acc, pre, rej, all
        """

        # FIXME: I think we're supposed to use salt.wheel.Wheel.master_call
        # for this stuff to call out to the master instead of touching
        # the files directly (need to set up some auth to do that though)

        keys = self.salt_key.list_keys()
        result = []

        key_to_status = {
            'minions_pre': 'pre',
            'minions_rejected': 'rejected',
            'minions': 'accepted'
        }

        for key, status in key_to_status.items():
            for minion in keys[key]:
                if not status_filter or status == status_filter:
                    result.append({
                        'id': minion,
                        'status': status
                    })

        return result

    def minion_accept(self, minion_id):
        """
        :param minion_id: A minion ID, or a glob
        """
        return self.salt_key.accept(minion_id)

    def minion_reject(self, minion_id):
        """
        :param minion_id: A minion ID, or a glob
        """
        return self.salt_key.reject(minion_id)

    def minion_delete(self, minion_id):
        """
        :param minion_id: A minion ID, or a glob
        """
        return self.salt_key.delete_key(minion_id)

    def minion_get(self, minion_id):
        result = self.salt_key.name_match(minion_id, full=True)
        if not result:
            return None

        if 'minions' in result:
            status = "accepted"
        elif "minions_pre" in result:
            status = "pre"
        elif "minions_rejected" in result:
            status = "rejected"
        else:
            raise ValueError(result)

        return {
            'id': minion_id,
            'status': status
        }

    def server_get(self, fqdn):
        return self._manager.servers.dump(self._manager.servers.get_one(fqdn))

    def server_list(self):
        return [self._manager.servers.dump(s) for s in self._manager.servers.get_all()]

    def server_get_cluster(self, fqdn, fsid):
        return self._manager.servers.dump_cluster(self._manager.servers.get_one(fqdn), self._manager.clusters[fsid])

    def server_list_cluster(self, fsid):
        return [
            self._manager.servers.dump_cluster(s, self._manager.clusters[fsid])
            for s in self._manager.servers.get_all_cluster(fsid)
        ]


class RpcThread(gevent.greenlet.Greenlet):
    """
    Present a ZeroRPC API for users
    to request state changes.
    """
    def __init__(self, manager):
        super(RpcThread, self).__init__()
        self._manager = manager
        self._complete = gevent.event.Event()
        self._server = zerorpc.Server(RpcInterface(manager))
        self._bound = False

    def stop(self):
        log.info("%s stopping" % self.__class__.__name__)

        self._complete.set()
        if self._server:
            self._server.stop()

    def bind(self):
        log.info("%s bind..." % self.__class__.__name__)
        self._server.bind(config.get('cthulhu', 'rpc_url'))
        self._bound = True

    def _run(self):
        assert self._bound

        try:
            log.info("%s run..." % self.__class__.__name__)
            self._server.run()
        except:
            log.error(traceback.format_exc())
            raise

        log.info("%s complete..." % self.__class__.__name__)
