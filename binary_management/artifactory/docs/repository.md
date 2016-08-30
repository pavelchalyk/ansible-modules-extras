### Artifactory Repository Module


- Create local repo

        ---
        - hosts: test
          tasks:
          - name: Create local repository
            artifactory_repository:
                action: "create"
                type: "local"
                key: "test-local-repo"
                package_type: "maven"


- Create remote repo

        - hosts: test
          tasks:
          - name: Create remote repository
            artifactory_repository:
                action: "create"
                type: "remote"
                key: "test-remote-repo"
                package_type: "docker"
                url: "http://hub.docker.com"


- Create virtual repo

        - hosts: test
          tasks:
          - name: Create virtual repository
            artifactory_repository:
                action: "create"
                type: "virtual"
                key: "test-virtual-repo"
                package_type: "maven"
                repositories: ["test-remote-repo"]


- Delete local/remote/virtual repos

        - hosts: test
          tasks:
          - name: Delete local/remote/virtual repository
            artifactory_repository:
                action: "delete"
                key: "test-remote-repo"


- Create repositories in bulk

        - hosts: test
          tasks:
          - name: Bulk create local/remote/virtual repositories
            artifactory_repository:
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                action: "bulk_create"
                path: "samples/artifactory_repositories.yml"


- Delete repositories in bulk

        - hosts: test
          tasks:
          - name: Bulk delete local/remote/virtual repositories
            artifactory_repository:
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                action: "bulk_delete"
                path: "samples/artifactory_repositories.yml"


- Sample yml file to create/delete repositories in bulk

        ---
        projects:
          silicon_valley:
             artifactory:
                 repository:
                     local:
                         - key: "silicon_valley-local1-repo"
                           package_type: "maven"
                           handle_snapshots: false
                         - key: "silicon_valley-local2-repo"
                           package_type: "docker"
                     remote:
                         - key: "silicon_valley-remote1-repo"
                           package_type: "maven"
                           url: "http://hub.docker.com"
                         - key: "silicon_valley-remote2-repo"
                           package_type: "docker"
                           url: "http://hub.docker.com"
                     virtual:
                         - key: "silicon_valley-virtual1-repo"
                           package_type: "maven"
                           repositories: ["silicon_valley-local1-repo"]

          mr_robot:
             artifactory:
                 repository:
                     local:
                         - key: "mr_robot-local1-repo"
                           package_type: "maven"
                         - key: "mr_robot-local2-repo"
                           package_type: "docker"
                     remote:
                         - key: "mr_robot-remote1-repo"
                           package_type: "maven"
                           url: "http://hub.docker.com"
                         - key: "mr_robot-remote2-repo"
                           package_type: "docker"
                           url: "http://hub.docker.com"
                     virtual:
                         - key: "mr_robot-virtual1-repo"
                           package_type: "maven"
                           repositories: ["mr_robot-local1-repo"]


- Module supports all fields provided by [artifactory api](https://www.jfrog.com/confluence/display/RTF/Repository+Configuration+JSON)
- Use fields in snake case rather than in camel case
