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
module: artifactory_user
short_description: Artifactory module to manage users
description:
    - Create new users
    - Update users
    - Remove users
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
            - Artifactory permissions action
        required: true
        default: string
    name:
        description:
            - User name
        required: true
        default: string
    email:
        description:
            - User email address
        required: true
        default: string
    password:
        description:
            - User password
        required: true
        default: string
    groups:
        description:
            - Groups to include user in
        required: false
        default: list
    admin:
        description:
            - If user should be admin
        required: false
        default: bool
    profile_updatable:
        description:
            - If user profile is updatable
        required: false
        default: bool
"""

EXAMPLES = """
---
- hosts: test
  tasks:
  - name: Create user
    artifactory_user:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        action: "create"
        name: "first.last"
        password: "test"
        email: "first.last@testartifactory.com"
        groups:
            - "readers"

- hosts: test
  tasks:
  - name: Update user
    artifactory_user:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        action: "update"
        name: "first.last"
        password: "test"  # password is required to update account details
        admin: True

- hosts: test
  tasks:
  - name: Delete user
    artifactory_user:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"
        action: "delete"
        name: "first.last"
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
            email = dict(required=False, type="str"),
            password = dict(required=False, type="str"),

            groups = dict(required=False, type="list", default=[]),
            admin = dict(required=False, type="bool", default=False),
            profile_updatable = dict(required=False, type="bool", default=True),
            internal_password_disabled = dict(required=False, type="bool", default=False),
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

            user = artifactory.security.users.new()
            user.name = module.params.get("name")
            user.password = module.params.get("password")
            user.email = module.params.get("email")
            user.groups = module.params.get("groups")
            user.admin = module.params.get("admin")
            user.profile_updatable = module.params.get("profile_updatable")
            user.internal_password_disabled = module.params.get("internal_password_disabled")

            response = user.create()
            module.exit_json(changed=True, msg=response)

        elif action.lower() == "update":
            params = module.params

            user = artifactory.security.users.fetch(
                    params.get("name"))

            if params.get("name"):
                user.name = params.get("name")

            if params.get("password"):
                user.password = params.get("password")
            else:
                user.password = ""

            if params.get("email"):
                user.email = params.get("email")

            if params.get("groups"):
                user.groups = params.get("groups")

            if params.get("admin"):
                user.admin = params.get("admin")

            if params.get("profile_updatable"):
                user.profile_updatable = params.get("profile_updatable")

            if params.get("internal_password_disabled"):
                user.internal_password_disabled = params.get("internal_password_disabled")
            else:
                user.internal_password_disabled = False

            response = user.update()
            module.exit_json(changed=True, msg=response)

        elif action.lower() == "delete":
            user = artifactory.security.users.fetch(
                    module.params.get("name"))

            response = user.remove()
            module.exit_json(changed=True, msg=response)

    except Exception, e:
        module.fail_json(msg=e)


from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
