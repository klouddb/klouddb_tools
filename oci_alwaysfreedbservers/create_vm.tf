data "oci_identity_availability_domain" "ad" {
  compartment_id = "${var.compartment_ocid}"
  ad_number      = "${var.ad_region_mapping[var.region]}"
}

locals {
  ssh_key = "${file("/home/ubuntu/.ssh/id_rsa.pub")}"
}


module "vcn" {
  source  = "oracle-terraform-modules/vcn/oci"
  version = "1.0.3"

  compartment_id           = var.compartment_ocid
  region                   = var.region
  vcn_dns_label            = "testvcn"
  vcn_name                 = "testVCN"
  internet_gateway_enabled = true
  nat_gateway_enabled      = false
  service_gateway_enabled  = false
  vcn_cidr                 = "10.1.0.0/16"
}

resource "oci_core_subnet" "demo_subnet" {
  cidr_block        = "10.1.20.0/24"
  display_name      = "demoSubnet"
  dns_label         = "demosubnet"
  security_list_ids = ["${oci_core_security_list.demo_security_list.id}"]
  compartment_id    = var.compartment_ocid
  vcn_id            = module.vcn.vcn_id
  route_table_id    = module.vcn.ig_route_id
}

resource "oci_core_security_list" "demo_security_list" {
  compartment_id = var.compartment_ocid
  vcn_id         = module.vcn.vcn_id
  display_name   = "demoSecurityList"

  egress_security_rules {
    protocol    = "6"
    destination = "0.0.0.0/0"
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      max = "22"
      min = "22"
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      max = "3000"
      min = "3000"
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      max = "3005"
      min = "3005"
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      max = "80"
      min = "80"
    }
  }
}

resource "oci_core_instance" "demo_instances" {
  count               = 2
  availability_domain = data.oci_identity_availability_domain.ad.name
  compartment_id      = var.compartment_ocid
  display_name        = "demoInstance-${count.index}"
  shape               = "VM.Standard.E2.1.Micro"

  create_vnic_details {
    subnet_id        = oci_core_subnet.demo_subnet.id
    display_name     = "primaryvnic"
    assign_public_ip = true
    hostname_label   = "demoinstance-${count.index}"
  }

  source_details {
    source_type = "image"
    source_id   = var.images[var.region]
  }

  metadata = {
    ssh_authorized_keys = "${local.ssh_key}"
  }
}
