# Configuration file for Jupyter Hub

c = get_config()

import re
import docker




from dockerspawner import DockerSpawner

class DemoFormSpawner(DockerSpawner):



    def _options_form_default(self):
        client_docker = docker.from_env()
        listImages = client_docker.images.list()
        listJupyter = []

        matchImg = re.compile(r'(?:jupyter\/)')
        parseImg = re.compile(r"'(.*?)'")
        for image in listImages:
            if matchImg.search(str(image)):
                parse = parseImg.findall(str(image))
                listJupyter.extend(parse)
        inserted_list = ('\n\t'.join(['<option value="' + image + '">' + image + '</option>' for image in listJupyter]))
        default_stack = "jupyter/minimal-notebook"
        return """
        <label for="stack">Select your desired stack</label>
        <select name="stack" size="1">
        %s
        </select>
        """%inserted_list.format(stack=default_stack)







    def options_from_form(self, formdata):
        options = {}
        options['stack'] = formdata['stack']
        container_image = ''.join(formdata['stack'])
        print("SPAWN: " + container_image + " IMAGE" )
        self.container_image = container_image
        return options


c.JupyterHub.spawner_class = DemoFormSpawner



# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

# spawn with Docker
#      c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.spawner_class = DemoFormSpawner


c.DockerSpawner.container_ip = "0.0.0.0"

#        c.DockerSpawner.container_image = 'jupyter/minimal-notebook'

# Have the Spawner override the Docker run command
c.DockerSpawner.extra_create_kwargs.update({
    'command': '/usr/local/bin/start-singleuser.sh'
})

# The docker instances need access to the Hub, so the default loopback port doesn't work:
#   from jupyter_client.localinterfaces import public_ips
#   c.JupyterHub.hub_ip = public_ips()[0]

# OAuth with GitHub
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.JupyterHub.confirm_no_ssl = True
