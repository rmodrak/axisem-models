#!/usr/bin/env python

import re



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


def convert_km_to_m(lines):
    old = lines
    new = []
    for line in old:
        parts = line.split(sep=None)
        parts[0] = str(1000.*float(parts[0]))
        new += [' '.join(parts)]
    return new


def convert_dep_to_rad(lines):
    old = lines
    new = []
    for line in old:
        parts = line.split(sep=None)
        parts[0] = str(6371000. - float(parts[0]))
        new += [' '.join(parts)]
    return new



if __name__=='__main__':


    input = 'ak135f_mdj2_celso.dep'
    output = 'ak135f_mdj2_celso.rad'

    # read text file
    with open(input, 'r') as file:
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


    # convert km to m
    if header_dict['UNITS'] == 'm':
        pass
    elif header_dict['UNITS'] == 'km':
        body = convert_km_to_m(body)
        header_dict['UNITS'] = 'm'
    else:
        raise ValueError


    # convert depth to radius
    body = convert_dep_to_rad(body)
    columns = re.sub('depth', 'radius', columns)
    header_dict['COLUMNS'] = columns


   # write output
    header = ['%s     %s\n' % (item[0], item[1]) for item in header_dict.items()]
    body = ['%s\n' % line for line in body]

    lines = []
    lines.extend(header)
    lines.extend(body)

    with open(output, 'w') as file:
        file.writelines(lines)


