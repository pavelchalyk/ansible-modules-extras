### Artifactory Permissions Module


- Permission abbreviation

        r=read
        w=deploy
        n=annotate
        d=delete
        m=admin


- Create permissions

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


- Update permissions

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


- Delete permissions

        - hosts: test
          tasks:
          - name: Delete permission
            artifactory_permission:
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                action: "delete"
                name: "test_permissions"


- Create/update/delete bulk permissions

        - hosts: test
          tasks:
          - name: Bulk create permissions
            artifactory_permission:
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                action: "bulk_create"  # bulk_create, bulk_update, bulk_delete
                path: "samples/artifactory_permissions.yml"


- Sample yml file for bulk permissions

        ---
        projects:
          silicon_valley:
             artifactory:
                 permission:
                     - name: "silicon_valley_permission"
                       repositories: ["test-local-repo"]

                       permissions:
                           users:
                               first.last: ["d", "r","w","m"]
                               anonymous: ["d", "r","w","m"]

          mr_robot:
             artifactory:
                 permission:
                     - name: "mr_robot_permission1"
                       repositories: ["test-local-repo"]

                       permissions:
                           users:
                               first.last: ["r","w","m"]
                           groups:
                               readers: ["r"]

                     - name: "mr_robot_permission2"
                       repositories: ["test-local-repo"]

                       permissions:
                           groups:
                               readers: ["r"]


- Module supports all fields provided by [artifactory api](https://www.jfrog.com/confluence/display/RTF/Security+Configuration+JSON)
- Use fields in snake case rather than in camel case
