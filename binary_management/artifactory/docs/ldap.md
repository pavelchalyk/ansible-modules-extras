### Artifactory LDAP Module


- Configure ldap

        ---
        - hosts: test
          tasks:
          - name: configure LDAP on artifactory
            artifactory_ldap:
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


- Import ldap groups as artifactory groups

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
