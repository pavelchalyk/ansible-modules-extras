#!/usr/bin/python

# Ansible artifactory ldap module

DOCUMENTATION = """
---
module: artifactory_ldap

short_description: Artifactory module to configure LDAP

description:
    - Provide LDAP Configuration
    - Module will connect to artifactory server and configure LDAP on it

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
    name:
        description:
            - Name of the LDAP Coniguration
        required: true
        default: string
    url:
        description:
            - LDAP URL
        required: true
        default: string
    search_filter:
        description:
            - search_filter for LDAP Configuration
        required: true
        default: string
    search_base:
        description:
            - search_base for LDAP Config
        required: false
        default: string
    manager_dn:
        description:
            - LDAP binding account Username.
        required: true
        default: string
    manager_password:
        description:
            - LDAP binding account Password.
        required: true
        default: string
    email_attribute:
        description:
            - email_attribute for LDAP Configuration.
        required: true
        default: string
    group_name:
        description:
            - group_name for LDAP Configuration
        required: true
        default: string

    group_search_base:
        description:
            - group_search_base for LDAP Configuration
        required: true
        default: string

    group_name_attribute:
        description:
            - group_name_attribute for LDAP Configuration
        required: true
        default: string

    group_member_attribute:
        description:
            - group_member_attribute for LDAP Configuration
        required: true
        default: string

    group_filter:
        description:
            - group_filter for LDAP Configuration
        required: true
        default: string

    description_attribute:
        description:
            - description_attribute for LDAP Configuration
        required: true
        default: string
"""

EXAMPLES = """
---
- hosts: test
  tasks:
  - name: configure LDAP on artifactory
    artifactory_ldap:
      artifactory_url: "http://localhost:8081"
      artifactory_username: "admin"
      artifactory_password: "password"

      action: "create"
      name: "LdapName"
      url: "ldap://ldap.community.company.com:389/DC=community,DC=company,DC=com"
      search_filter: "(&(objectClass=Person)(sAMAccountName={0}))"
      manager_dn: "ldap_username"
      manager_password: "ldap_password"
      email_attribute: "mail"
      group_name: "LdapGroups"
      group_search_base: "OU=Groups"
      group_name_attribute: "cn"
      group_member_attribute: "member:1.2.848.113550.1.4.1971:"
      group_filter: "(objectClass=group)"
      description_attribute: "name"


- hosts: test
  tasks:
  - name: Import dl's as artifactory ldap group
    artifactory_ldap:
      artifactory_url: "http://localhost:8081"
      artifactory_username: "admin"
      artifactory_password: "password"

      action: "import_group"
      ldap_group_name: "LdapGroups"
      ldap_group_list:
          - "dl-project-one"
          - "dl-project-two"
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
            # create ldap params
            name = dict(required=False, type="str"),
            url = dict(required=False, type="str"),
            search_filter = dict(required=False, type="str"),
            search_base = dict(required=False, type="str", default=""),
            manager_dn = dict(required=False, type="str"),
            manager_password = dict(required=False, type="str"),
            email_attribute = dict(required=False, type="str"),
            group_name = dict(required=False, type="str"),
            group_search_base= dict(required=False, type="str"),
            group_name_attribute = dict(required=False, type="str"),
            group_member_attribute = dict(required=False, type="str"),
            group_filter = dict(required=False, type="str"),
            description_attribute = dict(required=False, type="str"),

            # import dl params
            ldap_group_name = dict(required=False, type="str"),
            ldap_group_list = dict(required=False, type="list", default=[]),

            action = dict(required=True, type="str"),
            artifactory_url = dict(required=False, type="str"),
            artifactory_username = dict(required=False, type="str"),
            artifactory_password = dict(required=False, type="str"),
            artifactory_redirect = dict(required=False, type="str", default="artifactory"),
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
            ldap = artifactory.system.configuration.ldap()

            # ldap settings
            ldap.name=module.params.get("name")
            ldap.url=module.params.get("url")
            ldap.search_filter=module.params.get("search_filter")
            ldap.manager_dn=module.params.get("manager_dn")
            ldap.manager_password=module.params.get("manager_password")
            ldap.email_attribute=module.params.get("email_attribute")
            ldap.group_name=module.params.get("group_name")
            ldap.group_search_base=module.params.get("group_search_base")
            ldap.group_name_attribute=module.params.get("group_name_attribute")
            ldap.group_member_attribute=module.params.get("group_member_attribute")
            ldap.group_filter=module.params.get("group_filter")
            ldap.description_attribute=module.params.get("description_attribute")
            response = ldap.update()

            module.exit_json(changed=True, msg=response)

        elif action.lower() == "import_group":
            changed = False
            response = "Groups already imported"

            artifactory_groups = [group.name for group in artifactory.security.groups.list()]
            for dl in module.params.get("ldap_group_list"):
                if dl not in artifactory_groups:
                    changed = True

            if changed:
                ldap_groups = artifactory.ldap_groups.new()
                ldap_groups.group_name = module.params.get("ldap_group_name")
                ldap_groups.group_list = module.params.get("ldap_group_list")
                response = ldap_groups.import_group()

            module.exit_json(changed=changed, msg=response)
    except Exception, e:
        module.fail_json(msg=e)


from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
