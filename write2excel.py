from write_pyxl_nxos import mkXLSX, Headline, write_hl_category


deviceHeadline = Headline()
deviceHeadline.keylist = []
deviceHeadline.namelist = ['Hostname', 'S/N', 'Version']


def build_workbook(filename, TAB='HW List'):
    wb = mkXLSX(filename, TAB)



def writeDevice(device):
    ROW = 0
    COL = 1
    filename = device.name + '-' + device.serial + '.xlsx'
    TAB = 'System'
    wb = mkXLSX(filename, TAB)
    system = wb.active
    ROW = write_hl_category(system, ROW, COL, 'System', deviceHeadline.namelist)
    wb.save(filename)


def writePortMap(device):
    pass

