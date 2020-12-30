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

TENANT = 2      # test
SITE = 50       # test
DEVICE_ROLE = 2 # test

nb = pynetbox.api(NB_URL, token = NB_TOKEN)

dl = getList4CSV('devices.csv')
for dev in dl:
    model_slug = dev['model'].lower()
    model_id = nb.dcim.device_types.get(slug = dev['model'].lower())
    print ('='*50)
    if model_id:
        dev_name = dev['name']
        print (f'Import {dev_name}    as      {str(model_id.model)}')
        item = dict (
            name = dev['name'],
            device_type = model_id.id,
            device_role = DEVICE_ROLE,
            tenant = TENANT,
            site = SITE,
        )
        dev_new = nb.dcim.devices.create(item)       
        item_interface = dict (
            device = dev_new.id,
            name = "VLAN"+str(dev['vlan']),
            type = 'virtual',
        )
        dev_int_new = nb.dcim.interfaces.create(item_interface)
        item_ip = dict (
            family = 4,
            address = dev["ip"]+'/24',          # use correct mask
            tenant = TENANT,
            status = 'active',
            interface = dev_int_new.id,
            
        )
        iip = nb.ipam.ip_addresses.create(item_ip)
        dev_new.primary_ip4 = iip
        dev_new.save()
    else:
        print (f'Not found device type with slug {model_slug}')
