#!/usr/bin/env python3
# Author: @m8r0wn
# Description: Test ipparser cidr functionality

from ipparser import ipparser

print("CIDR /32, IP COUNT: {}".format(len(ipparser("10.0.0.0/32"))))
print("CIDR /31, IP COUNT: {}".format(len(ipparser("10.0.0.0/31"))))
print("CIDR /30, IP COUNT: {}".format(len(ipparser("10.0.0.0/30"))))
print("CIDR /29, IP COUNT: {}".format(len(ipparser("10.0.0.0/29"))))
print("CIDR /28, IP COUNT: {}".format(len(ipparser("10.0.0.0/28"))))
print("CIDR /27, IP COUNT: {}".format(len(ipparser("10.0.0.0/27"))))
print("CIDR /26, IP COUNT: {}".format(len(ipparser("10.0.0.0/26"))))
print("CIDR /25, IP COUNT: {}".format(len(ipparser("10.0.0.0/25"))))
print("CIDR /24, IP COUNT: {}".format(len(ipparser("10.0.0.0/24"))))
print("CIDR /23, IP COUNT: {}".format(len(ipparser("10.0.0.0/23"))))
print("CIDR /22, IP COUNT: {}".format(len(ipparser("10.0.0.0/22"))))
print("CIDR /21, IP COUNT: {}".format(len(ipparser("10.0.0.0/21"))))
print("CIDR /20, IP COUNT: {}".format(len(ipparser("10.0.0.0/20"))))
print("CIDR /19, IP COUNT: {}".format(len(ipparser("10.0.0.0/19"))))
print("CIDR /18, IP COUNT: {}".format(len(ipparser("10.0.0.0/18"))))
print("CIDR /17, IP COUNT: {}".format(len(ipparser("10.0.0.0/17"))))
print("CIDR /16, IP COUNT: {}".format(len(ipparser("10.0.0.0/16"))))
print("CIDR /15, IP COUNT: {}".format(len(ipparser("10.0.0.0/15"))))
print("CIDR /14, IP COUNT: {}".format(len(ipparser("10.0.0.0/14"))))
print("CIDR /13, IP COUNT: {}".format(len(ipparser("10.0.0.0/13"))))
print("CIDR /12, IP COUNT: {}".format(len(ipparser("10.0.0.0/12"))))
print("CIDR /11, IP COUNT: {}".format(len(ipparser("10.0.0.0/11"))))
print("CIDR /10, IP COUNT: {}".format(len(ipparser("10.0.0.0/10"))))
print("CIDR /9, IP COUNT: {}".format(len(ipparser("10.0.0.0/9"))))
print("CIDR /8, IP COUNT: {}".format(len(ipparser("10.0.0.0/8"))))
print("CIDR /7, IP COUNT: {}".format(len(ipparser("10.0.0.0/7", exit_on_error=False))))
print("CIDR /33, IP COUNT: {}".format(len(ipparser("10.0.0.0/33", exit_on_error=False))))