def copyAttr(obj1, obj2, list):
    for a in list:
        obj1.setattr(a, obj2.getattr(a))

class nxosDevice:
    # Cisco Nexus Device
    def __init__(self, json_data):
        try:
            self.name = json_data['show_hostname']['hostname']
        except:
            print('Hostname not found...Skipping')
            self.name = 'xyz'
        try:
            self.serial = json_data['show_version']['proc_board_id']
        except:
            print('Serial not found...Skipping')
            self.serial = '123456'
        self.data = json_data
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
                vl = nxosVlan(a)
                for b in self.vlanInt:
                    vlanIntId = b.interface.lstrip('Vlan')
                    if vl.vlanId == vlanIntId:
                        vl.setattr(vlanInt, b)
                    self.vlan.append(vl)
        except:
            print('VLANs Issues')

    def getInterfaces(self):
        try:
            for a in self.data['show_int_status']['TABLE_interface']['ROW_interface']:
                int = nxosInterface(a)
                # Sort Interfaces Ethernet, Loopback, Vlan, nve, etc.
                if 'Eth' in int.interface:
                    self.eth.append(int)
                elif 'port-channel' in int.interface:
                    self.portchannel.append(int)
                elif 'Vlan' in int.interface:
                    self.vlanInt.append(int)
                elif 'loopback' in int.interface:
                    self.lo.append(int)
                elif 'nve' in int.interface:
                    self.nve.append(int)
                elif 'mgmt' in ipInt.interface:
                    self.mgmt.append(int)
                else:
                    self.miscInt.append(int)
                    print(f'Found undefined Interface {int.interface}')

            for a in self.data['show_ip_int']['TABLE_intf']:
                ipInt = nxosIpInterface(a['ROW_intf'])
                list = ['ip', 'subnet', 'masklen', 'mtu', 'protostate', 'adminstate', 'linkstate']
                if 'Eth' in ipInt.interface:
                    for b in self.eth:
                        if b.interface == ipInt.interface:
                            copyAttr(b, ipInt, list)
                elif 'port-channel' in ipInt.interface:
                    for b in self.portchannel:
                        if b.interface == ipInt.interface:
                            copyAttr(b, ipInt, list)
                elif 'Vlan' in ipInt.interface:
                    for b in self.vlanInt:
                        if b.interface == ipInt.interface:
                            copyAttr(b, ipInt, list)
                elif 'loopback' in ipInt.interface:
                    for b in self.lo:
                        if b.interface == ipInt.interface:
                            copyAttr(b, ipInt, list)
                elif 'nve' in ipInt.interface:
                    for b in self.nve:
                        if b.interface == ipInt.interface:
                            copyAttr(b, ipInt, list)
                elif 'mgmt' in ipInt.interface:
                    for b in self.mgmt:
                        if b.interface == ipInt.interface:
                            copyAttr(b, ipInt, list)
                else:
                    self.miscInt.append(int)
                    print(f'Found undefined Interface {int.interface}')

        except:
            print(f'Get Interface failed for {self.name}')




class nxosVlan:

    def __init__(self, json_data):
        try:
            self.data = json_data
            self.vlanId = json_data['vlanshowbr-vlanid']
            self.name = json_data['vlanshowbr-vlanname']
            self.state = json_data['vlanshowbr-vlanstate']
            self.shutstate = json_data['vlanshowbr-shutstate']
            self.portlist = json_data['vlanshowplist-ifidx']
        except:
            print(f'Failed to Create NXOS VLAN')

class nxosInterface:
    # Cisco Nexus Interface
    def __init__(self, json_data):

        try:
            self.interface = json_data['interface']
            try:
                self.name = json_data['name']
            except:
                print(f'No Description defined for {self.interface}')
                self.name = ''
            try:
                self.state = json_data['state']
            except:
                print(f'No State defined for {self.interface}')
                self.state = ''
            try:
                self.speed = json_data['speed']
            except:
                print(f'No Speed defined for {self.interface}')
                self.speed = ''
            try:
                self.type = json_data['type']
            except:
                print(f'No Type defined for {self.interface}')
                self.type = ''
            try:
                self.vlan = json_data['vlan']
            except:
                print(f'No Vlan defined for {self.interface}')
                self.vlan = ''
        except:
            print('Data not found...Skipping')
            self.name = 'Not Found'
        self.data = json_data

class nxosIpInterface:
    def __init__(self, json_data):
        try:
            self.data = json_data
            self.interface = json_data['intf-name']
            self.protostate = json_data['proto-state']
            self.linkstate = json_data['link-state']
            self.adminstate = json_data['admin-state']
            self.ip = json_data['prefix']
            self.subnet = json_data['subnet']
            self.masklen = json_data['masklen']
            self.numAddr = json_data['num-addr']
            self.mtu = json_data['mtu']
        except:
            print('Failed to process IP Interface Data')


def nxosBuildDevice(json_data):
    device = nxosDevice(json_data)
    device.getInterfaces()
    device.getVlans()
    return device


