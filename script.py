import pynetbox
import csv

def getList4CSV(csv_file):
    dev_list = list()
    obj = open(csv_file)
    reader = csv.DictReader(obj, delimiter = ';')
    for line in reader:
        item = dict (
            name = line['name'],
            model = line['model'],
            vlan = line['vlan'],
            ip = line['ip'],
        )
        dev_list.append(item)
    return (dev_list)
    

NB_URL = '******************'
NB_TOKEN = '******************'

TENANT = 2
SITE = 50
DEVICE_ROLE = 2

nb = pynetbox.api(NB_URL, token = NB_TOKEN)

dl = getList4CSV('devices.csv')
for dev in dl:
    model_id = nb.dcim.device_types.get(slug = dev['model'].lower())
    dev_name = dev['name']
    #print (f'{dev_name}          {str(model_id.id)}')
    item = dict (
        name = dev['name'],
        device_type = model_id.id,
        device_role = DEVICE_ROLE,
        tenant = TENANT,
        site = SITE,
    )
    dev_new = nb.dcim.devices.create(item)
    print (dev_new)
    item_interface = dict (
        device = dev_new.id,
        name = "VLAN"+str(dev['vlan']),
        type = 'virtual',
    )
    dev_int_new = nb.dcim.interfaces.create(item_interface)
    print (dev_int_new.id)
    item_ip = dict (
        family = 4,
        address = dev["ip"]+'/24',
        tenant = TENANT,
        status = 'active',
        assigned_object_id = dev_int_new.id,
        assigned_object_type = 'dcim.interface',
    )

    iip = nb.ipam.ip_addresses.create(item_ip)
