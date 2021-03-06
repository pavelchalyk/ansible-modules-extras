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
module: artifactory_group
short_description: Artifactory module to manage groups
description:
    - Create new groups
    - Update groups
    - Remove groups
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
    name:
        description:
            - Group name
        required: true
        default: string
    description:
        description:
            - Group description
        required: false
        default: string
    auto_join:
        description:
            - If group should auto_join
        required: false
        default: bool
    realm:
        description:
            - Realm for the group
        required: false
        default: str
    realm_attributes:
        description:
            - Realm attributes
        required: false
        default: str
"""

EXAMPLES = """
---
- hosts: test
  tasks:
  - name: Create group
    artifactory_group:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        action: "create"
        name: "test_group"
        description: "group for testing"

- hosts: test
  tasks:
  - name: Update group
    artifactory_group:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        action: "update"
        name: "test_group"
        auto_join: True

- hosts: test
  tasks:
  - name: Delete group
    artifactory_group:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        action: "delete"
        name: "test_group"
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
            name = dict(required=True, type="str"),
            description = dict(required=False, type="str"),
            auto_join = dict(required=False, type="bool", default=False),
            realm = dict(required=False, type="str"),
            realm_attributes = dict(required=False, type="str"),
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
        if action.lower() == "create":

            group = artifactory.security.groups.new()
            group.name = module.params.get("name")
            group.description = module.params.get("description")
            group.auto_join = module.params.get("auto_join")
            group.realm = module.params.get("realm")
            group.realm_attributes = module.params.get("realm_attributes")

            response = group.create()
            module.exit_json(changed=True, msg=response)

        elif action.lower() == "update":
            params = module.params

            group = artifactory.security.groups.fetch(
                    params.get("name"))

            if params.get("name"):
                group.name = params.get("name")

            if params.get("description"):
                group.description = params.get("description")

            if params.get("auto_join"):
                group.auto_join = params.get("auto_join")

            if params.get("realm"):
                group.realm = params.get("realm")

            if params.get("realm_attributes"):
                group.realm_attributes = params.get("realm_attributes")
            else:
                group.realm_attributes = ""

            response = group.update()
            module.exit_json(changed=True, msg=response)

        elif action.lower() == "delete":
            group = artifactory.security.groups.fetch(
                    module.params.get("name"))

            response = group.remove()
            module.exit_json(changed=True, msg=response)

    except Exception, e:
        module.fail_json(msg=e)


from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
