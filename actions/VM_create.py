import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from st2common.runners.base_action import Action

class MyEchoAction(Action):
   def run(self, Subcription_Id, Group_Name, Location, VM_Name, Client_Id, Secret, Tenant_Id):

        SUBSCRIPTION_ID = '2f50f202-0a84-4c8c-a929-fcc5a3174590'
        GROUP_NAME = 'myResourceGroup'
        LOCATION = 'West India'
        VM_NAME = 'VM61'


        def create_availability_set(compute_client):
            avset_params = {
                'location': LOCATION,
                'sku': { 'name': 'Aligned' },
                'platform_fault_domain_count': 2
                }
            availability_set_result = compute_client.availability_sets.create_or_update(
                GROUP_NAME,
                'myAVSet',
                avset_params
                )

        def create_resource_group(resource_group_client):
            resource_group_params = { 'location':LOCATION }
            resource_group_result = resource_group_client.resource_groups.create_or_update(
                GROUP_NAME,
                resource_group_params
            )

        def get_credentials():
            credentials = ServicePrincipalCredentials(
                client_id = '211c9188-812b-4fa9-9fc7-c455f2e8ad9d',
                secret = '9ns1@vspcC46PV+Q-su?=g?tg5[:3-XB',
                tenant = 'd5656af4-b7b3-45b9-9346-fb0547921fb7'
            )

            return credentials
        def create_public_ip_address(network_client):
            public_ip_addess_params = {
                'location': LOCATION,
                'public_ip_allocation_method': 'Dynamic'
            }
            creation_result = network_client.public_ip_addresses.create_or_update(
                GROUP_NAME,
                'myIPAddress',
                public_ip_addess_params
            )

            return creation_result.result()

        def create_vnet(network_client):
            vnet_params = {
                'location': LOCATION,
                'address_space': {
                    'address_prefixes': ['10.0.0.0/16']
                }
            }
            creation_result = network_client.virtual_networks.create_or_update(
                GROUP_NAME,
                'myVNet',
                vnet_params
            )
            return creation_result.result()

        def create_subnet(network_client):
            subnet_params = {
                'address_prefix': '10.0.0.0/24'
            }
            creation_result = network_client.subnets.create_or_update(
                GROUP_NAME,
                'myVNet',
                'mySubnet',
                subnet_params
            )

            return creation_result.result()

        def create_nic(network_client):
            subnet_info = network_client.subnets.get(
                GROUP_NAME,
                'myVNet',
                'mySubnet'
            )
            publicIPAddress = network_client.public_ip_addresses.get(
                GROUP_NAME,
                'myIPAddress'
            )
            nic_params = {
                'location': LOCATION,
                'ip_configurations': [{
                    'name': 'myIPConfig',
                    'public_ip_address': publicIPAddress,
                    'subnet': {
                        'id': subnet_info.id
                    }
                }]
            }
            creation_result = network_client.network_interfaces.create_or_update(
                GROUP_NAME,
                'myNic',
                nic_params
            )

            return creation_result.result()

          def create_vm(network_client, compute_client):
            nic = network_client.network_interfaces.get(
                GROUP_NAME,
                'myNic'
            )
            avset = compute_client.availability_sets.get(
                GROUP_NAME,
                'myAVSet'
            )
            vm_parameters = {
                'location': LOCATION,
                'os_profile': {
                    'computer_name': VM_NAME,
                    'admin_username': 'azureuser',
                    'admin_password': 'Azure12345678'
                },
                'hardware_profile': {
                    'vm_size': 'Standard_A0'
                },
                'storage_profile': {
                    'image_reference': {
                        'publisher': 'MicrosoftWindowsServer',
                        'offer': 'WindowsServer',
                        'sku': '2012-R2-Datacenter',
                        'version': 'latest'
                    }
                },
                'network_profile': {
                    'network_interfaces': [{
                        'id': nic.id
                    }]
                },
                'availability_set': {
                    'id': avset.id
                }
            }
            creation_result = compute_client.virtual_machines.create_or_update(
                GROUP_NAME,
                VM_NAME,
                vm_parameters
            )

            return creation_result.result()
          
       
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

          create_resource_group(resource_group_client)      

          create_availability_set(compute_client)
         
          creation_result = create_public_ip_address(network_client)
         
          creation_result = create_vnet(network_client)         

          creation_result = create_subnet(network_client)
         
          creation_result = create_nic(network_client)        

          creation_result = create_vm(network_client, compute_client)         
          
          print("VM created Successfully")
