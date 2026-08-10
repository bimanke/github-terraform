resource "azurerm_linux_virtual_machine" "vm" {
    for_each = var.vms
  name                = each.value.vm_name
  resource_group_name = each.value.rg_name
  location            = each.value.location
  size                = each.value.vm_size 
  admin_username      = each.value.admin_username
  admin_password = each.value.admin_password
  network_interface_ids = [data.azurerm_network_interface.nicdata[each.key].id]
  disable_password_authentication = "false"

  os_disk {
    caching              = each.value.caching
    storage_account_type = each.value.storage_account_type
  }

  source_image_reference {
    publisher = each.value.publisher
    offer     = each.value.offer
    sku       = each.value.sku
    version   = each.value.version
  }
}

data "azurerm_network_interface" "nicdata" {
  for_each = var.vms
  name                = each.value.nic_name
  resource_group_name = each.value.rg_name
}