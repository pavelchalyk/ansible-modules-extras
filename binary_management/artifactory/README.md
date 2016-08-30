### Ansible Artifactory Modules
Ansible artifactory modules to manage jFrog artifactory


#### Requirements

    pip install git+https://github.com/veritasos/py-artifactory.git


#### Authorization
- You can provides credentials in two ways

    - Directly through modules

            # Define as module arguments
            artifactory_url: "http://localhost:8081"
            artifactory_username: "admin"
            artifactory_password: "password"

            # optional (default is "artifactory")
            artifactory_redirect: "binary_management"
            # this will redirect to http://localhost:8081/binary_management

    - As environment variables

            ARTIFACTORY_URL = "http://localhost:8081"
            ARTIFACTORY_USERNAME = "admin"
            ARTIFACTORY_PASSWORD = "password"

            # optional (default is "artifactory")
            # this will redirect to http://localhost:8081/binary_management
            ARTIFACTORY_REDIRECT = "binary_management"



#### Available artifactory modules
- [Artifactory User](docs/user.md)
- [Artifactory Group](docs/group.md)
- [Artifactory Permission](docs/permission.md)
- [Artifactory Repository](docs/repository.md)
- [Artifactory LDAP](docs/ldap.md)
- [Artifactory User Api Key](docs/apikey.md)


#### Testing

    ansible-playbook -i tests/inventory tests/artifactory_repository.yml


#### Note

- [Artifactory api](https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API) follows camel case but these modules follow snake case.
- Example:

        Artifactory rest api field name: handleSnapshots
        Ansible Module field name: handle_snapshots


#### ToDo
- Add support to update artifactory repository
