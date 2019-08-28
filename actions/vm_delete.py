import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from st2common.runners.base_action import Action

class MyEchoAction(Action):              
        
        def run(self, Subcription_id, Group_Name, Location, VM_Name, Client_Id, Secret, Tenant_Id):
            
            SUBSCRIPTION_ID = Subcription_id
            GROUP_NAME = Group_Name
            LOCATION = Location
            VM_NAME = VM_Name
            def get_credentials():
                credentials = ServicePrincipalCredentials(client_id = Client_Id,secret = Secret,tenant = Tenant_Id)        
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
