module "rg" {
source =   "../child/rg"
rgs = var.rgs
}

module "vn" {
    depends_on = [ module.rg ]
    source = "../child/vnet"
    vnets = var.vnets
  
}
module "snet" {
    depends_on = [ module.vn , module.rg ]
    source = "../child/subnet"
    snet = var.snet
  
}
module "nic" {
    depends_on = [ module.vn ,module.snet ]
    source = "../child/nic"
    nics = var.nics
  
}
module "vm" {
    depends_on = [ module.nic , module.snet ]
    source = "../child/vm"
    vms = var.vms
  
}