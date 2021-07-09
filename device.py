from pprint import pprint

# region Define object Keylists Used for building tables and writing to Excel
nxosDeviceKeylist = [{'name': {'data': 'host_name', 'hl': 'Hostname'}},
                     {'serial': {'data': 'proc_board_id', 'hl': 'S/N'}},
                     {'version': {'data': 'kickstart_ver_str', 'hl': 'Version'}},
                     {'chassis': {'data': 'chassis_id', 'hl': 'Chassis'}},
                     {'uptime': {'data': 'uptime', 'hl': 'Uptime'}}]

nxosVlanKeylist = [{'name': {'data': 'vlanshowbr-vlanname', 'hl': 'VLAN Name'}},
                   {'vlanid': {'data': 'vlanshowbr-vlanid', 'hl': 'VLAN ID'}},
                   {'state': {'data': 'vlanshowbr-vlanstate', 'hl': 'State'}},
                   {'shutstate': {'data': 'vlanshowbr-shutstate', 'hl': 'Shutdown State'}},
                   {'portlist': {'data': 'vlanshowplist-ifidx', 'hl': 'Interfaces'}}]

#Port-map final output
nxosIntKeylist = [{'interface': {'data': 'interface', 'hl': 'Interface'}},
                  {'name': {'data': 'name', 'hl': 'Description'}},
                  {'vlan': {'data': 'vlan', 'hl': 'Routed/VLAN'}},
                  {'state': {'data': 'state', 'hl': 'State'}},
                  {'speed': {'data': 'speed', 'hl': 'Speed'}},
                  {'ip': {'data': 'ip', 'hl': 'IP Address'}},
                  {'mtu': {'data': 'mtu', 'hl': 'MTU'}},
                  {'vrf_name': {'data': 'vrf_name', 'hl': 'VRF'}},
                  {'type': {'data': 'type', 'hl': 'Type'}},
                  {'device_id': {'data': 'device_id', 'hl': 'Neighbor Device'}},
                  {'platform_id': {'data': 'platform_id', 'hl': 'Platform'}},
                  {'port_id': {'data': 'port_id', 'hl': 'Neighbor Port'}},
                  ]

nxosIPIntKeylist = [{'interface': {'data': 'intf-name', 'hl': 'Interface'}},
                    {'ip': {'data': 'prefix', 'hl': 'IP Address'}},
                    {'mtu': {'data': 'mtu', 'hl': 'MTU'}},
                    {'proto-state': {'data': 'proto-state', 'hl': 'Protocol State'}},
                    {'admin-state': {'data': 'admin-state', 'hl': 'Admin State'}}]

nxosVrfIntKeylist = [{'interface': {'data': 'if_name', 'hl': 'Interface'}},
                     {'vrf_name': {'data': 'vrf_name', 'hl': 'VRF'}}]

nxosCDPKeylist = [{'interface': {'data': 'intf_id', 'hl': 'Interface'}},
                  {'device_id': {'data': 'device_id', 'hl': 'Neighbor Device'}},
                  {'platform_id': {'data': 'platform_id', 'hl': 'Platform'}},
                  {'port_id': {'data': 'port_id', 'hl': 'Neighbor Port'}}]



#endregion

def getKeys(dict):
    list = []
    for a in dict.keys():
        list.append(a)
    return list

def copyAttr(obj1, obj2, list):
    for a in list:
        if a == 'keylist':
            pass
        else:
            setattr(obj1, a, getattr(obj2, a))

def initAttr(obj):
    # Initialize variables based on key list
    for a in obj.keylist:
        a_key = a.keys()
        for b in a_key:
            b_key = b
        try:
            d = a[b_key]['data']
            setattr(obj, b_key, obj.data[d])
        except:
            setattr(obj, b_key, '')



class nxosDevice:
    # Cisco Nexus Device
    def __init__(self, json_data):
        self.keylist = nxosDeviceKeylist
        # process uptime
        time = json_data['show_version']['kern_uptm_hrs'] + ':' + \
               json_data['show_version']['kern_uptm_mins'] + ':' + \
               json_data['show_version']['kern_uptm_secs']

        uptime = json_data['show_version']['kern_uptm_days'] + ', ' + time
        json_data['show_version'].update({'uptime': uptime})
        self.data = json_data
        self.name = json_data['show_hostname']['hostname']
        self.serial = json_data['show_version']['proc_board_id']
        self.version = json_data['show_version']['kickstart_ver_str']
        self.chassis = json_data['show_version']['chassis_id']
        self.uptime = time
        self.eth = []
        self.portchannel = []
        self.lo = []
        self.vlanInt = []
        self.vlan = []
        self.nve = []
        self.miscInt = []
        self.mgmt = []


    def getVlans(self):
        try: # Create Interface Objects
            for a in self.data['show_vlan']['TABLE_vlanbrief']['ROW_vlanbrief']:
                vl = nxosSubObj(a, nxosVlanKeylist)
                for b in self.vlanInt:
                    vlanIntId = b.interface.lstrip('Vlan')
                    if vl.vlanId == vlanIntId:
                        vl.setattr('vlanInt', b)
                    self.vlan.append(vl)
        except:
            print('VLANs Issues')

    def getInterfaces(self):
        #try:
        for a in self.data['show_int_status']['TABLE_interface']['ROW_interface']:
            int = nxosSubObj(a, nxosIntKeylist)
            # Sort Interfaces Ethernet, Loopback, Vlan, nve, etc.
            if 'Eth' in int.interface:
                print('Appending Eth')
                self.eth.append(int)
            elif 'port-channel' in int.interface:
                self.portchannel.append(int)
            elif 'Vlan' in int.interface:
                self.vlanInt.append(int)
            elif 'loopback' in int.interface:
                self.lo.append(int)
            elif 'nve' in int.interface:
                self.nve.append(int)
            elif 'mgmt' in int.interface:
                self.mgmt.append(int)
            else:
                self.miscInt.append(int)
                print(f'Found undefined Interface {int.interface}')
        nxosIntObj(self, self.data['show_ip_int']['TABLE_intf'], nxosIPIntKeylist, extendedkey='ROW_intf')
        nxosIntObj(self, self.data['show_vrf_interface']['TABLE_if']['ROW_if'], nxosVrfIntKeylist)
        pprint(self.data['show_cdp_nei'])
        nxosIntObj(self, self.data['show_cdp_nei']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info'],
                   nxosCDPKeylist)


    def newattr(self, key, attrlist):
        for a in attrlist:
            try:
                for b in a.keys():
                    c = a[b]['data']
                    new = self.data[key][c]
                setattr(self, b, new)
            except:
                print(f'Failed to find Key {a} in {key}')

def nxosIntObj(obj1, data, keylist, extendedkey = 'none'):
    for a in data:
        if extendedkey != 'none':
            z = a[extendedkey]
        else:
            z = a
        nxosObj = nxosSubObj(z, keylist)
        tmp_list = vars(nxosObj)
        list = tmp_list.keys()
        if 'Eth' in nxosObj.interface:
            for b in obj1.eth:
                if b.interface == nxosObj.interface:
                    copyAttr(b, nxosObj, list)
        elif 'port-channel' in nxosObj.interface:
            for b in obj1.portchannel:
                if b.interface == nxosObj.interface:
                    copyAttr(b, nxosObj, list)
        elif 'Vlan' in nxosObj.interface:
            for b in obj1.vlanInt:
                if b.interface == nxosObj.interface:
                    copyAttr(b, nxosObj, list)
        elif 'loopback' in nxosObj.interface:
            for b in obj1.lo:
                if b.interface == nxosObj.interface:
                    copyAttr(b, nxosObj, list)
        elif 'nve' in nxosObj.interface:
            for b in obj1.nve:
                if b.interface == nxosObj.interface:
                    copyAttr(b, nxosObj, list)
        elif 'mgmt' in nxosObj.interface:
            for b in obj1.mgmt:
                if b.interface == nxosObj.interface:
                    copyAttr(b, nxosObj, list)
        else:
            obj1.miscInt.append(nxosObj)
            print(f'Found undefined Interface IP {nxosObj.interface}')
    '''except:
        print(f'Get Interface failed for {self.name}')'''

class nxosSubObj:
    # Cisco Nexus Interface
    def __init__(self, json_data, keylist):
        self.keylist = keylist
        self.data = json_data
        initAttr(self)


class xlsxObj:
    def __init__(self, json_data):
        pass


def nxosBuildDevice(json_data):
    device = nxosDevice(json_data)
    device.getInterfaces()
    device.getVlans()
    return device



