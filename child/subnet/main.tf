resource "azurerm_subnet" "sub" {
    for_each = var.snet
  name = each.value.snet_name
  virtual_network_name = each.value.vnet_name
  resource_group_name = each.value.rg_name
  address_prefixes =  each.value.address_prefixes
  
  
}