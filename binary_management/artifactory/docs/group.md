### Artifactory Groups Module


- Create group

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


- Update group

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


- Delete group

        - hosts: test
          tasks:
          - name: Delete group
            artifactory_group:
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                action: "delete"
                name: "test_group"


- Module supports all fields provided by [artifactory api](https://www.jfrog.com/confluence/display/RTF/Security+Configuration+JSON)
- Use fields in snake case rather than in camel case
