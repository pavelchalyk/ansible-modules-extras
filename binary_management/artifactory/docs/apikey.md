### Artifactory User Api Key Module


- Get api key for logged in user

        - hosts: test
          tasks:
          - name: Get api key
            artifactory_apikey:
                action: "get"
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"


- Create api key for logged in user

        - hosts: test
          tasks:
          - name: Create api key
            artifactory_apikey:
                action: "create"
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                api_key: "my-key"


- Revoke api key for logged in user

        - hosts: test
          tasks:
          - name: Revoke api key
            artifactory_apikey:
                action: "revoke"
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"


- Revoke api key for other users (admin only)

        - hosts: test
          tasks:
          - name: Revoke api key for other users (admin only)
            artifactory_apikey:
                action: "revoke"
                artifactory_url: "http://localhost:8081"
                artifactory_username: "admin"
                artifactory_password: "password"

                user: "anonymous"


- Module supports all fields provided by [artifactory api](https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-GetAPIKey)
- Use fields in snake case rather than in camel case
