from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from st2common.runners.base_action import Action

class MyEchoAction(Action):
    def run(self, SUBSCRIPTION_ID, GROUP_NAME, LOCATION, VM_NAME, client_id, secret, tenant):
        SUBSCRIPTION_ID = SUBSCRIPTION_ID
        GROUP_NAME = GROUP_NAME
        LOCATION = LOCATION
        VM_NAME = VM_NAME
        
        def get_credentials():
            credentials = ServicePrincipalCredentials(
                client_id = client_id,
                secret = secret,
                tenant = tenant
            )
        
            return credentials
        
        def delete_resources(resource_group_client):
            resource_group_client.resource_groups.delete(GROUP_NAME)

        credentials = get_credentials()
        resource_group_client = ResourceManagementClient(
            credentials,
            SUBSCRIPTION_ID
        )
        network_client = NetworkManagementClient(
            credentials,
            SUBSCRIPTION_ID
        )
        compute_client = ComputeManagementClient(
            credentials,
            SUBSCRIPTION_ID
        )

        delete_resources(resource_group_client)
