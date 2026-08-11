rgs = {
  rg1 = {
    rg_name  = "bipin1"
    location = "SouthAfricaNorth"
  }
  rg = {
    rg_name  = "bipin2"
    location = "SouthAfricaNorth"
  }
}


vnets = {
  vnet2 = {
    vnet_name     = "vbipin1"
    location      = "SouthAfricaNorth"
    rg_name       = "bipin1"
    address_space = ["10.0.0.0/22"]

  }
}

snet = {
  subnet1 = {
    vnet_name        = "vbipin1"
    snet_name        = "frontendsubnet1"
    location         = "SouthAfricaNorth"
    rg_name          = "bipin1"
    address_prefixes = ["10.0.1.0/26"]
  }
  subnet2 = {
    vnet_name        = "vbipin1"
    snet_name        = "backendsubnet1"
    location         = "SouthAfricaNorth"
    rg_name          = "bipin1"
    address_prefixes = ["10.0.2.0/26"]
  }
}

nics = {
  nic1 = {
    vnet_name                     = "vbipin1"
    nic_name                      = "bipin1nic"
    location                      = "SouthAfricaNorth"
    rg_name                       = "bipin1"
    ip_configuration_name         = "internal"
    private_ip_address_allocation = "Dynamic"
    snet_name                     = "frontendsubnet1"



  }
  nic2 = {
    nic_name                      = "bipin1nic2"
    location                      = "SouthAfricaNorth"
    rg_name                       = "bipin1"
    ip_configuration_name         = "internal"
    private_ip_address_allocation = "Dynamic"
    snet_name                     = "backendsubnet1"
    vnet_name                     = "vbipin1"


  }
}

vms = {
  vm1 = {

    vm_name                         = "frontendvm"
    rg_name                         = "bipin1"
    location                        = "SouthAfricaNorth"
    vm_size                         = "Standard_DS1_v2"
    admin_username                  = "bipin1"
    admin_password                  = "Admin@2123456"
    disable_password_authentication = "false"
    caching                         = "ReadWrite"
    storage_account_type            = "Standard_LRS"
    publisher                       = "Canonical"
    offer                           = "0001-com-ubuntu-server-jammy"
    sku                             = "22_04-lts"
    version                         = "latest"
    nic_name                        = "bipin1nic"
  }
  vm2 = {

    vm_name                         = "backendvm"
    rg_name                         = "bipin1"
    location                        = "SouthAfricaNorth"
    vm_size                         = "Standard_DS1_v2"
    admin_username                  = "bipin1"
    admin_password                  = "Admin@2123456"
    disable_password_authentication = "false"
    caching                         = "ReadWrite"
    storage_account_type            = "Standard_LRS"
    publisher                       = "Canonical"
    offer                           = "0001-com-ubuntu-server-jammy"
    sku                             = "22_04-lts"
    version                         = "latest"
    nic_name                        = "bipin1nic2"
  }
}


nsgs = {
  nsg1 = {
    nsg_name                   = "bipinnsg"
    location                   = "SouthAfricaNorth"
    resource_group_name        = "bipin1"
    tets_name                  = "testbipin"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
