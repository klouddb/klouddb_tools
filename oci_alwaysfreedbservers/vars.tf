variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "compartment_ocid" {}
variable "region" {}

variable "ad_region_mapping" {
  type = map

  default = {
    us-seattle-1 = 2
    us-sanjose-1 = 1
  }
}

variable "images" {
  type = map

  default = {
    # See https://docs.us-phoenix-1.oraclecloud.com/images/
    # Oracle-provided image "Oracle-Linux-7.5-2018.10.16-0"
    us-phoenix-1 = "ocid1.image.oc1.phx.aaaaaaaadtmpmfm77czi5ghi5zh7uvkguu6dsecsg7kuo3eigc5663und4za"

    us-ashburn-1 = "ocid1.image.oc1.iad.aaaaaaaayuihpsm2nfkxztdkottbjtfjqhgod7hfuirt2rqlewxrmdlgg75q"
    us-sanjose-1 = "ocid1.image.oc1.us-sanjose-1.aaaaaaaabzxj3lv6j623p2dqmjolk4zslnssbr3qhlmoef6numj6erduvhgq"

  }
}
