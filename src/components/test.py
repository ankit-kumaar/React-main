from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
#29, 30, 31


def connect_to_esxi(host_details):
    """
    Establish a connection to the ESXi host.

    :param host_details: A dictionary containing ESXi host details.
                         It should have the following keys:
                         - 'ip_address': IP address of the ESXi host
                         - 'username': Username for authentication
                         - 'password': Password for authentication
    :return: A connection object to the ESXi host
    """
    si = SmartConnect(
        host=host_details['ip_address'],
        user=host_details['username'],
        pwd=host_details['password'],
        disableSslCertValidation=True
    )
    atexit.register(Disconnect, si)
    return si

def create_vm(vm_spec, content, datacenter, cluster):
    """
    Create a virtual machine in the vCenter.

    :param vm_spec: A dictionary containing VM specifications.
                    It should have the following keys:
                    - 'vm_name': Name of the virtual machine
                    - 'cpu_count': Number of CPU cores
                    - 'memory_size_gb': Memory size in GB
                    - 'disk_size_gb': Disk size in GB
                    - 'network_config': A dictionary containing network configurations
    :param content: A connection object to the ESXi host
    :param datacenter: A datacenter object
    :param cluster: A cluster object
    :return: A virtual machine object
    """
    # Create a new VM configuration
    vm_conf = vim.vm.ConfigInfo()
    vm_conf.name = vm_spec['vm_name']
    vm_conf.numCPUs = vm_spec['cpu_count']
    vm_conf.memoryMB = vm_spec['memory_size_gb'] * 1024

    # Create a new disk configuration
    disk_conf = vim.vm.device.VirtualDeviceSpec()
    disk_conf.device = vim.vm.device.VirtualDisk()
    disk_conf.device.capacityInKB = vm_spec['disk_size_gb'] * 1024 * 1024

    # Create a new network configuration
    network_conf = vim.vm.device.VirtualDeviceSpec()
    network_conf.device = vim.vm.device.VirtualVmxnet3()
    network_conf.device.deviceInfo = vim.Description()
    network_conf.device.deviceInfo.label = 'Network Interface 1'
    network_conf.device.deviceInfo.summary = 'Network Interface 1'
    network_conf.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    network_conf.device.connectable.startConnected = True
    network_conf.device.connectable.allowGuestControl = True

    # Get the network object
    network = next((network for network in content.viewManager.CreateContainerView(
        content.rootFolder, [vim.Network], True).view
                    if network.name == vm_spec['network_config']['network_name']), None)
    if network:
        network_conf.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        network_conf.device.backing.network = network
        network_conf.device.backing.useAutoDetect = False

    # Add devices to the VM configuration
    vm_conf.deviceChange = [disk_conf, network_conf]

    # Create the VM
    folder = datacenter.vmFolder
    task = folder.CreateVM_Task(config=vm_conf, pool=cluster)
    task.Wait()
    return task.info.result

def deploy_vm_vcenter(esxi_host_details, vm_specs):
    """
    Deploy multiple virtual machines within a VMware vCenter environment.

    :param esxi_host_details: A dictionary containing ESXi host details.
                              It should have the following keys:
                              - 'ip_address': IP address of the ESXi host
                              - 'username': Username for authentication
                              - 'password': Password for authentication
    :param vm_specs: A list of dictionaries containing VM specifications.
                     Each dictionary should have the following keys:
                     - 'vm_name': Name of the virtual machine
                     - 'cpu_count': Number of CPU cores
                     - 'memory_size_gb': Memory size in GB
                     - 'disk_size_gb': Disk size in GB
                     - 'network_config': A dictionary containing network configurations
    :return: A list of virtual machine objects
    """
    si = connect_to_esxi(esxi_host_details)
    content = si.RetrieveContent()
    datacenter = content.rootFolder.childEntity[0]
    cluster = datacenter.hostFolder.childEntity[0]

    vm_list = []
    for vm_spec in vm_specs:
        vm = create_vm(vm_spec, content, datacenter, cluster)
        vm_list.append(vm)

    return vm_list

# Example usage
if __name__ == "__main__":
    esxi_host_details = {
        'ip_address': '192.168.1.100',
        'username': 'your_username',
        'password': 'your_password'
    }
    vm_specs = [
        {
            'vm_name': 'VM1',
            'cpu_count': 2,
            'memory_size_gb': 4,
            'disk_size_gb': 100,
            'network_config': {
                'network_name': 'VM Network',
                'ip_address': '192.168.1.10'
            }
        },
        {
            'vm_name': 'VM2',
            'cpu_count': 4,
            'memory_size_gb': 8,
            'disk_size_gb': 200,
            'network_config': {
                'network_name': 'VM Network',
                'ip_address': '192.168.1.11'
            }
        }
    ]

    deployed_vms = deploy_vm_vcenter(esxi_host_details, vm_specs)
    print("Deployed VMs:")
    for vm in deployed_vms:
        print(vm.name)