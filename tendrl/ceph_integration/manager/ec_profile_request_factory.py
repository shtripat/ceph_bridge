import logging

from tendrl.ceph_integration.manager.request_factory import RequestFactory
from tendrl.ceph_integration.manager.user_request import ECProfileCreatingRequest
from tendrl.ceph_integration.manager.user_request import ECProfileModifyingRequest


class ECProfileRequestFactory(RequestFactory):
    def create(self, attributes):
        commands = [
            'osd', 'erasure-code-profile', 'set', attributes['name'],
            'directory=%s' % attributes['directory'],
            'plugin=%s' % attributes['plugin'],
            'k=%s' % str(attributes['k']),
            'm=%s' % str(attributes['m'])
        ]

        return ECProfileCreatingRequest(
            "Creating ec profile '{name}'".format(name=attributes['name']),
            attributes['name'], commands)

    def delete(self, ec_profile_name):
        commands = [
            'osd', 'erasure-code-profile', 'rm', ec_profile_name
        ]

        return ECProfileModifyingRequest(
            "Deleting ec profile '{name}'".format(name=ec_profile_name),
            commands
        )
