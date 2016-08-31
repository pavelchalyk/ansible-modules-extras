#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Veritas LLC
#
# This file is part of Ansible.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = """
---
module: artifactory_apikey
short_description: Artifactory module to manage user api keys
description:
    - Get api key
    - Create new api key
    - Revoke api key
    - Revoke api key for other users
version_added: "2.2"
author: "Prathamesh Nevagi (@pratz)"
requirements:
    - python 2.x (2.4, 2.5, 2.6, 2.7)
    - https://github.com/veritasos/py-artifactory.git
options:
    artifactory_url:
        description:
            - Artifactory url
        required: false
        default: string
    artifactory_username:
        description:
            - Artifactory username
        required: false
        default: string
    artifactory_password:
        description:
            - Artifactory password
        required: false
        default: string
    action:
        description:
            - Action to perform
        required: true
        default: string
    api_key:
        description:
            - Api key to set
        required: false
        default: string
    user:
        description:
            - Revoke api key for provided user
        required: false
        default: string
"""

EXAMPLES = """
---
- hosts: test
  tasks:
  - name: Get api key
    artifactory_apikey:
        action: "get"
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"


- hosts: test
  tasks:
  - name: Create api key
    artifactory_apikey:
        action: "create"
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        api_key: "my-key"


- hosts: test
  tasks:
  - name: Revoke api key
    artifactory_apikey:
        action: "revoke"
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"


- hosts: test
  tasks:
  - name: Revoke api key for other users (admin only)
    artifactory_apikey:
        action: "revoke"
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        user: "anonymous"
"""

RETURN = """
response:
    description: Response retured from Artifactory server
    type: string
"""

# stdlib imports
import os

# 3rd-party imports
try:
    from artifactory import Artifactory
    HAS_ARTIFACTORY = True
except:
    HAS_ARTIFACTORY = False
    INSTALL_ARTIFACTORY_MSG = """
    Python artifactory package required
    pip install git+https://github.com/veritasos/py-artifactory.git
    """


def main():

    module = AnsibleModule(
        argument_spec = dict(
            artifactory_url = dict(required=False, type="str"),
            artifactory_username = dict(required=False, type="str"),
            artifactory_password = dict(required=False, type="str"),
            artifactory_redirect = dict(required=False, type="str", default="artifactory"),

            action = dict(required=True, type="str"),
            api_key = dict(required=False, type="str", default=""),
            user = dict(required=False, type="str", default=""),
        ),
        supports_check_mode=True
    )

    if not HAS_ARTIFACTORY:
        module.fail_json(msg=INSTALL_ARTIFACTORY_MSG)

    action = module.params.get("action")
    artifactory_url = os.environ.get("ARTIFACTORY_URL", module.params.get("artifactory_url"))
    artifactory_username = os.environ.get("ARTIFACTORY_USERNAME", module.params.get("artifactory_username"))
    artifactory_password = os.environ.get("ARTIFACTORY_PASSWORD", module.params.get("artifactory_password"))
    artifactory_redirect = os.environ.get("ARTIFACTORY_REDIRECT", module.params.get("artifactory_redirect"))

    # create a artifactory client instance
    artifactory = Artifactory(
        url=artifactory_url,
        username=artifactory_username,
        password=artifactory_password,
        redirect=artifactory_redirect,
        )


    try:
        if action.lower() == "get":

            apikey = artifactory.security.apikeys.fetch()
            module.exit_json(changed=True, msg="")

        elif action.lower() == "create":

            apikey = artifactory.security.apikeys.new()
            apikey.api_key = module.params.get("api_key")
            apikey = apikey.create()

            module.exit_json(changed=True, msg=apikey.api_key)

        elif action.lower() == "revoke":

            response = artifactory.security.apikeys.revoke(
                    module.params.get("user"))
            module.exit_json(changed=True, msg=response)

    except Exception, e:
        module.fail_json(msg=e)


from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
