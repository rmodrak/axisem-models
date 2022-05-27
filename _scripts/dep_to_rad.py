#!/usr/bin/env python

import re
import sys

from _shared import _split, _parse, convert_units, convert_dep_to_rad



if __name__=='__main__':


    for filename in sys.argv[1:]:
        input = filename
        output = filename+'.rad'

        # read text file
        with open(filename, 'r') as file:
            lines = file.readlines()


        # parse header
        header, body = _split(lines)

        header_dict = _parse(header)
        columns = header_dict['COLUMNS']

        parts = columns.split(' ')
        if parts[0]!='depth':
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


        print('\nWRITING TO\n%s\n' % output)

        with open(output, 'w') as file:
            file.writelines(lines)


