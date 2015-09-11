#!/usr/bin/env python
import xml.etree.ElementTree as ET
import os

if len(os.sys.argv) != 3:
	print "Error in %s" % os.sys.argv[0]
	print "Usage: %s <parameters.xml> <parameters.c>"
	raise SystemExit

fp = open(os.sys.argv[2], "w")

tree = ET.parse(os.sys.argv[1])
root = tree.getroot()
body = """
#include <stdint.h>
#include <systemlib/param/param.h>

// DO NOT EDIT
// This file is autogenerated from paramaters.xml

"""

start_name = ""
end_name = ""

for group in root:
	if group.tag == "group":
		body += "// %s\n" % group.attrib["name"]
		for param in group:
			if not start_name:
				start_name = param.attrib["name"]
			end_name = param.attrib["name"]
			body += """ 
static const
__attribute__((used, section("__param")))
struct param_info_s __param__%s = {
	"%s",
	PARAM_TYPE_%s,
	.val.f = %s
};
""" % (param.attrib["name"], param.attrib["name"], param.attrib["type"], param.attrib["default"])
body += """
extern const
__attribute__((alias("__param__%s")))
struct param_info_s __param_start;

extern const
__attribute__((alias("__param__%s")))
struct param_info_s __param_end;
""" % (start_name, end_name)

fp.write(body)
