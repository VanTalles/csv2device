import csv
import pynetbox
from collections import Counter

def getList4CSV(csv_file,delim):
    dev_list = list()
    obj = open(csv_file)
    reader = csv.DictReader(obj, delimiter = delim)
    for line in reader:
        item = dict (
            name = line['name'],
            model = line['model'],
            vlan = line['vlan'],
            ip = line['ip'],
        )
        dev_list.append(item)
    return (dev_list)


def check_model(mlist):
    NB_URL = 'https://*****************'
    NB_TOKEN = '*****************'
    lip_nb = pynetbox.api(NB_URL,token = NB_TOKEN)
    lip_nb.http_session.verify = False 
    result = []
    for model in mlist:
        model_nb = lip_nb.dcim.device_types.get(slug = model.lower())
        if model_nb:
            res_str =  (f'MODEL: {model}  Manufacturer {model_nb.manufacturer.slug}')
        else:
            res_str = (f'Model {model} not found')
        result.append(res_str)
    return result


if __name__ == '__main__':
    dev_list = getList4CSV('devices.csv',',')
    #print (dev_list)
    model_list = []
    for dev in dev_list:
        if dev['model'] not in model_list:
            model_list.append(dev['model'])
    res = check_model(model_list)
    for line in res:
        print (line)
   
