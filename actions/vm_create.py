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
