#!/usr/bin/env python

import re
import sys

def _split(lines, length=4):
    header = []
    body = []

    for _i, line in enumerate(lines):
        print(_i, line)
        if _i < length:
            header += [line]
        else:
            body += [line]

    return header, body


def _parse(header):
    header_dict = {}
    for line in header:
        parts = line.split(sep=None)
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
        parts = line.split(sep=None)
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
        parts = line.split(sep=None)
        if units=='m':
            parts[0] = str(6371000. - float(parts[0]))
        elif units=='km':
            parts[0] = str(6371. - float(parts[0]))
        else:
            raise ValueError

        new += [' '.join(parts)]
    return new



if __name__=='__main__':


    for filename in sys.argv[1:]:
        input = 'mdj2.dep'
        output = 'mdj2.rad'

        # read text file
        with open(filename, 'r') as file:
            lines = file.readlines()


        # parse header
        header, body = _split(lines)

        header_dict = _parse(header)
        print(header_dict)
        columns = header_dict['COLUMNS']

        parts = columns.split(' ')
        if parts[0]!='depth':
            print(columns)
            raise Exception('Unexpected format')


        # convert units
        old=header_dict['UNITS']
        new='m'
        header_dict, body = convert_units(header_dict, body, old, new)


        # convert depth to radius
        body = convert_dep_to_rad(body, units=new)
        columns = re.sub('depth', 'radius', columns)
        header_dict['COLUMNS'] = columns


       # write output
        header = ['%s     %s\n' % (item[0], item[1]) for item in header_dict.items()]
        body = ['%s\n' % line for line in body]

        lines = []
        lines.extend(header)
        lines.extend(body)

        output = re.sub('.dep', '.rad', filename)
        assert filename!=output

        with open(output, 'w') as file:
            file.writelines(lines)


