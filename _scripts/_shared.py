#!/usr/bin/env python

import re
import sys

def _split(lines, length=4, sep=None):
    header = []
    body = []

    for _i, line in enumerate(lines):
        print(_i, line)
        if _i < length:
            header += [line]
        else:
            body += [line]

    return header, body


def _parse(header, sep=None):
    header_dict = {}
    for line in header:
        parts = line.split()
        key, val = parts[0], ' '.join(parts[1:])
        header_dict[key] = val

    return header_dict


def convert_units(header_dict, body, old='m', new='m'):
    if old==new:
        return header_dict, body
    elif old=='m' and new=='km':
        factor=1.e-3
    elif old=='km' and new=='m':
        factor=1.e3
    else:
        raise ValueError

    header_dict['UNITS'] = new

    lines_old = body
    lines_new = []
    for line in lines_old:
        if line.startswith('#'):
            continue
        parts = line.split()
        parts[0] = str(factor*float(parts[0])) # depth
        parts[1] = str(factor*float(parts[1])) # density
        parts[2] = str(factor*float(parts[2])) # vp
        parts[3] = str(factor*float(parts[3])) # vs

        lines_new += [' '.join(parts)]

    return header_dict, lines_new


def convert_dep_to_rad(lines, units='m'):
    old = lines
    new = []
    for line in old:
        if line.startswith('#'):
            continue
        parts = line.split()
        if units=='m':
            parts[0] = str(6371000. - float(parts[0]))
        elif units=='km':
            parts[0] = str(6371. - float(parts[0]))
        else:
            raise ValueError

        new += [' '.join(parts)]
    return new


def convert_rad_to_dep(lines, units='m'):
    old = lines
    new = []
    for line in old:
        if line.startswith('#'):
            continue
        parts = line.split()
        if units=='m':
            parts[0] = str(6371000. - float(parts[0]))
        elif units=='km':
            parts[0] = str(6371. - float(parts[0]))
        else:
            raise ValueError

        new += [' '.join(parts)]
    return new



