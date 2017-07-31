import ast
import docker
import web

from nlist import ListR


class StopR:
    """
    This endpoint is for stopping a network tap filter container
    """

    @staticmethod
    def POST():
        """
        Send a POST request with a docker container ID and it will be stopped.
        Can also send 'all' as the ID and every network tap container will be
        stopped.

        Example input: {'id': "12345"}, {'id': ["123", "456"], or {'id': "all"}
        """
        web.header('Content-Type', 'application/json')

        # verify user input
        data = web.data()
        payload = {}
        try:
            payload = ast.literal_eval(data)
        except Exception as e: # pragma: no cover
            return 'malformed payload : ' + str(e)

        # verify payload has a container ID
        if 'id' not in payload:
            return 'payload missing container id'

        # connect to docker and stop the given container
        c = None
        try:
            c = docker.from_env()
        except Exception as e: # pragma: no cover
            return 'unable to connect to docker because: ' + str(e)

        # stop all network tap containers if keyword 'all' is given
        # TODO: figure out how to implement all without reinventing the wheel
        # if payload['id'] == 'all':
        #    try:
        #        network_containers = ListR.GET()
        #        for container in network_containers:
        #           c.containers.get(container['id']).stop()
        #    except Exception as e: # pragma no cover
        #        return 'unable to stop multiple containers because: ' + \
        #               str(e)

        # if user gives a list of id, delete them all
        if type(payload['id']) == list:
            try:
                for container_id in payload['id']:
                    c.containers.get(container_id).stop()
            except Exception as e: # pragma: no cover
                return 'unable to stop list of containers because: ' + str(e)

        # if user gives just one id, delete it
        else:
            try:
                c.containers.get(payload['id']).stop()
            except Exception as e: # pragma: no cover
                return 'unable to stop container because: ' + str(e)

        return ('container successfully stopped: ' + str(payload['id']))
