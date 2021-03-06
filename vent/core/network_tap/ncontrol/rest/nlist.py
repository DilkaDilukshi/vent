import docker
import web


class ListR:
    """
    This endpoint is for listing all filter containers
    """

    @staticmethod
    def GET():
        web.header('Content-Type', 'text/html')

        # connect to docker
        try:
            containers = docker.from_env()
        except Exception as e:  # pragma: no cover
            return (False, 'unable to connect to docker because: ' + str(e))

        # search for all docker containers and grab ncapture containers
        container_list = []
        try:
            for c in containers.containers.list(all=True):
                # TODO: maybe find a way to not have to hard code image name
                if c.attrs["Config"]["Image"] == \
                        "cyberreboot/vent-ncapture:master":
                    # the core container is not what we want
                    if "core" not in c.attrs["Config"]["Labels"]\
                       ["vent.groups"]:
                        lst = {}
                        lst['id'] = c.attrs["Id"][:12]
                        lst['status'] = c.attrs["State"]["Status"]
                        lst['args'] = c.attrs['Args']
                        container_list.append(lst)
        except Exception as e:  # pragma: no cover
            return (False, "Failure: " + str(e))

        return (True, container_list)
