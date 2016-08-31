#!/usr/bin/python

# Ansible artifactory permission module

DOCUMENTATION = """
---
module: artifactory_permission

short_description: Artifactory module to manager permission

description:
    - Create new permissions
    - Update permissions
    - Remove permissions

version_added: "0.1"

author: "Veritas"

requirements:
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
    path:
        description:
            - Path to yaml file for bulk create/update/delete
        required: true
        default: string
    name:
        description:
            - Name of permission
        required: true
        default: string
    repositories:
        description:
            - Repositories to add permissions to
        required: false
        default: list
    permissions:
        description:
            - User and group permissions
        required: false
        default: dict
"""

EXAMPLES = """
---
- hosts: test
  tasks:
  - name: Create permission
    artifactory_permission:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"

        action: "create"
        name: "test_permissions"
        repositories: ["test-local-repo"]

        permissions:
            users:
                first.last: ["r","w","m"]
            groups:
                readers: ["r"]

- hosts: test
  tasks:
  - name: Update permission
    artifactory_permission:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"

        action: "update"
        name: "test_permissions"
        repositories: ["test-local-repo", "ANY"]

        permissions:
            users:
                first.last: ["r"]
            groups:
                readers: ["r"]

- hosts: test
  tasks:
  - name: Delete permission
    artifactory_permission:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"

        action: "delete"
        name: "test_permissions"

- hosts: test
  tasks:
  - name: Bulk create permissions
    artifactory_permission:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"

        action: "bulk_create"
        path: "samples/artifactory_permissions.yml"

- hosts: test
  tasks:
  - name: Bulk update permissions
    artifactory_permission:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"

        action: "bulk_create"
        path: "samples/artifactory_permissions.yml"

- hosts: test
  tasks:
  - name: Bulk delete permissions
    artifactory_permission:
        artifactory_url: "http://localhost:8081"
        artifactory_username: "admin"
        artifactory_password: "password"

        action: "bulk_delete"
        path: "samples/artifactory_permissions.yml"
"""

# stdlib imports
import os
import yaml

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


def create_permission(artifactory, params):
    permission = artifactory.security.permissions.new()
    permission.name = params.get("name", "") + params.get("suffix")
    if params.get("suffix"):
        permission.repositories = [repo + params.get("suffix") for repo in params.get("repositories", [])]
    else:
        permission.repositories = params.get("repositories", [])
    permission.principals = params.get("permissions", {})
    permission.includes_pattern = params.get("includes_pattern", "**")
    permission.excludes_pattern = params.get("excludes_pattern", "")
    return permission.create()


def update_permission(artifactory, params):
    permission = artifactory.security.permissions.fetch(
            params.get("name", ""))

    if params.get("repositories"):
        permission.repositories = params.get("repositories")

    if params.get("permissions"):
        permission.principals = params.get("permissions")

    if params.get("includes_pattern"):
        permission.includes_pattern = params.get("includes_pattern")

    if params.get("excludes_pattern"):
        permission.excludes_pattern = params.get("excludes_pattern")

    return permission.update()


def main():

    module = AnsibleModule(
        argument_spec = dict(
            artifactory_url = dict(required=False, type="str"),
            artifactory_username = dict(required=False, type="str"),
            artifactory_password = dict(required=False, type="str"),
            artifactory_redirect = dict(required=False, type="str", default="artifactory"),
            path = dict(required=False, type="str"),

            action = dict(required=True, type="str"),
            name = dict(required=False, type="str"),
            repositories = dict(required=False, type="list"),
            includes_pattern = dict(required=False, type="str", default="**"),
            excludes_pattern = dict(required=False, type="str", default=""),
            permissions = dict(required=False, type="dict", default={}),
            suffix = dict(required=False, type="str", default=""),
        ),
        supports_check_mode=True

    )

    if not HAS_ARTIFACTORY:
        module.fail_json(msg=INSTALL_ARTIFACTORY_MSG)

    action = module.params.get("action")
    suffix = module.params.get("suffix")
    artifactory_url = os.environ.get("ARTIFACTORY_URL", module.params.get("artifactory_url"))
    artifactory_username = os.environ.get("ARTIFACTORY_USERNAME", module.params.get("artifactory_username"))
    artifactory_password = os.environ.get("ARTIFACTORY_PASSWORD", module.params.get("artifactory_password"))
    artifactory_redirect = os.environ.get("ARTIFACTORY_REDIRECT", module.params.get("artifactory_redirect"))

    path = module.params.get("path")
    if path:
        path = os.path.abspath(path)

    # create a artifactory client instance
    artifactory = Artifactory(
        url=artifactory_url,
        username=artifactory_username,
        password=artifactory_password,
        redirect=artifactory_redirect,
        )

    try:
        if action.lower() == "create":
            changed = False
            try:
                artifactory.security.permissions.fetch(module.params.get("name"))
                response = "Permission {0} already exists".format(
                        module.params.get("name"))
            except:
                response = create_permission(artifactory, module.params)
                changed = True

            module.exit_json(changed=changed, msg=response)

        elif action.lower() == "update":
            response = update_permission(artifactory, module.params)
            module.exit_json(changed=True, msg=response)

        elif action.lower() == "delete":
            changed = False
            try:
                permission = artifactory.security.permissions.fetch(
                        module.params.get("name"))
                response = permission.remove()
                changed = True
            except:
                response = "Permission {0} does not exists".format(
                        module.params.get("name"))

            module.exit_json(changed=changed, msg=response)

        elif action.lower() == "bulk_create":
            changed = False
            response = []
            params = yaml.load(open(path, 'r'))

            for project_name, services in params.get("projects").iteritems():

                if services.get("artifactory").get("permissions"):
                    for permission_params in services.get("artifactory").get("permissions"):

                        try:
                            artifactory.security.permissions.fetch(
                                    permission_params.get("name"))
                            response.append("Permission {0} already exists".format(
                                    permission_params.get("name")))
                        except:
                            response.append(create_permission(
                                artifactory, permission_params))
                            changed = True

            module.exit_json(changed=changed, msg=response)

        elif action.lower() == "bulk_update":
            response = []
            params = yaml.load(open(path, 'r'))

            for project_name, services in params.get("projects").iteritems():

                if services.get("artifactory").get("permissions"):
                    for permission_params in services.get("artifactory").get("permissions"):
                        response.append(update_permission(
                            artifactory, permission_params))

            module.exit_json(changed=True, msg=response)

        elif action.lower() == "bulk_delete":
            changed = False
            response = []
            params = yaml.load(open(path, 'r'))

            for project_name, services in params.get("projects").iteritems():

                if services.get("artifactory").get("permissions"):
                    for permission_params in services.get("artifactory").get("permissions"):
                        try:
                            permission = artifactory.security.permissions.fetch(
                                    permission_params.get("name"))
                            response.append(permission.remove())
                            changed = True
                        except Exception:
                            response.append("Permission {0} does not exists".format(
                                    permission_params.get("name")))

            module.exit_json(changed=changed, msg=response)
    except Exception, e:
        module.fail_json(msg=e)


from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
