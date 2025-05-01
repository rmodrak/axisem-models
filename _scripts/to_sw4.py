#!/usr/bin/env python

import re
import sys

from _shared import _split, _parse, convert_units, convert_dep_to_rad, lists_to_dicts
from _convert_Q import Q_alpha



if __name__=='__main__':


    for filename in sys.argv[1:]:
        input = filename
        output = filename+'.sw4'

        # read text file
        with open(filename, 'r') as file:
            lines = file.readlines()

        header, body = _split(lines)


        # extract column labels
        header_dict = _parse(header)
        column_labels = header_dict['COLUMNS'].split()

        if column_labels[0] != 'depth':
            raise Exception('Unexpected format')

        # parse body
        nrows = len(body)
        ncols = len(column_labels)

        rows = []
        for line in body:
            row = [float(string) for string in line.split()]
            rows += [row]

        diff = list()
        for _ir in range(nrows-1):
            diff.append([])
            for _ic in range(ncols):
                diff[-1].append(rows[_ir+1][_ic] - rows[_ir][_ic])

        #
        # convert to sw4 input file format
        #
        dicts = lists_to_dicts(column_labels, rows)

        lines = []
        for _ir in range(nrows-1):

            depth1 = dicts[_ir]['depth']
            depth2 = dicts[_ir+1]['depth']

            if depth1==depth2:
                continue

            try:
                vp1 = dicts[_ir]['vp']
                vp2 = dicts[_ir+1]['vp']
            except:
                vp1 = dicts[_ir]['vpv']
                vp2 = dicts[_ir+1]['vpv']

            try:
                vs1 = dicts[_ir]['vs']
                vs2 = dicts[_ir+1]['vs']
            except:
                vs1 = dicts[_ir]['vsv']
                vs2 = dicts[_ir+1]['vsv']

            try:
                qkappa1 = dicts[_ir]['qkappa']
                qkappa2 = dicts[_ir+1]['qkappa']
            except:
                pass

            try:
                qmu1 = dicts[_ir]['qmu']
                qmu2 = dicts[_ir+1]['qmu']
            except:
                pass

            rho1 = dicts[_ir]['rho']
            rho2 = dicts[_ir+1]['rho']

            line = 'block '
            line += f'z1={depth1} '
            line += f'z2={depth2} '

            line += f'vp={vp1} '
            if vp1!=vp2:
               line += f'vpgrad={(vp2-vp1)/(depth2-depth1)} '

            line += f'vs={vs1} '
            if vs1!=vs2:
               line += f'vsgrad={(vs2-vs1)/(depth2-depth1)} '

            line += f'rho={rho1} '
            if rho1!=rho2:
               line += f'rhograd={(rho2-rho1)/(depth2-depth1)} '

            try:
                qp1 = Q_alpha(qkappa1,qmu1,vp1,vs1)
                qp2 = Q_alpha(qkappa2,qmu2,vp2,vs2)
                qp = (qp1+qp2)/2.

                qs1 = qmu1
                qs2 = qmu2
                qs = (qs1+qs2)/2.

                line += f'qp={qp} '
                line += f'qs={qs} '
            except:
                pass

            line += '\n'
            lines += [line]
            print(line)

        print()


        # write results
        with open(output, 'w') as file:
            file.writelines(lines)


