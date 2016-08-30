### Artifactory Users Module


- Create user

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


- Update user

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


- Delete user

        - hosts: test
          tasks:
          - name: Delete user
            artifactory_user:
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                action: "delete"
                name: "first.last"


- Module supports all fields provided by [artifactory api](https://www.jfrog.com/confluence/display/RTF/Security+Configuration+JSON)
- Use fields in snake case rather than in camel case
