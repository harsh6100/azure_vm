#!/usr/bin/env python2

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

from st2common.runners.base_action import Action

class MyEchoAction(Action):
	def run(self,sub_id,group_name,location,vm_name,client_id1,secret1,tenant1):
		SUBSCRIPTION_ID = sub_id
		GROUP_NAME = group_name
		LOCATION = location
		VM_NAME = vm_name

		def get_credentials():
			credentials = ServicePrincipalCredentials(
				client_id = client_id1,
				secret =  secret1,
				tenant = tenant1)
			return credentials
	
		def stop_vm(compute_client):
			print('VM Stopped')
			compute_client.virtual_machines.power_off(GROUP_NAME, VM_NAME)
		
		credentials = get_credentials()
		resource_group_client = ResourceManagementClient(credentials,SUBSCRIPTION_ID)
		network_client = NetworkManagementClient(credentials,SUBSCRIPTION_ID)
		compute_client = ComputeManagementClient(credentials,SUBSCRIPTION_ID)
		stop_vm(compute_client)
