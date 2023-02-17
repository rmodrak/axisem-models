#!/usr/bin/env python

import argparse
import numpy as np
import re
import sys

from collections import defaultdict
from _shared import _split, _parse, convert_units, convert_dep_to_rad

from matplotlib import pyplot

params = {'mathtext.default': 'regular' }          
pyplot.rcParams.update(params)


def _parse_columns(keys, lines):

    table = defaultdict(list)

    for line in lines:
        values = line.split()
        for _i, key in enumerate(keys):
            table[key] += [float(values[_i])]

    return table


labels = {
    'vp': '$V_P$ [km/s]',
    'vpv': '$V_P$ [km/s]',
    'vs': '$V_S$ [km/s]',
    'vsv': '$V_S$ [km/s]',
    'rho': 'Density [kg/$m^3$]',
    'qmu': '$Q_{mu}$',
    'qka': '$Q_{kappa}$',
    'qkappa': '$Q_{kappa}$',
    }


if __name__=='__main__':

    parser = argparse.ArgumentParser()

    # optional arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_depth', type=float)

    # at least one positional argument required
    parser.add_argument('args', nargs='+')

    args = parser.parse_args()


    for filename in args.args:
        print('  plotting %s' % filename)

        input = filename
        output = filename+'.rad'

        # read text file
        with open(filename, 'r') as file:
            lines = file.readlines()


        # parse header
        header, body = _split(lines)
        header_dict = _parse(header)

        if header_dict['COLUMNS'].split()[0]!='depth':
            raise Exception('Unexpected format')

        # convert units
        old=header_dict['UNITS']
        new='km'
        header_dict, body = convert_units(header_dict, body, old, new)


        keys = header_dict['COLUMNS'].split(' ')
        table = _parse_columns(keys, body)


        if len(keys)!=6:
            raise Exception('Unexpected number of columns')

        # create figure
        width = 15.
        height = 9.

        fig, axes = pyplot.subplots(1, 5,
            figsize=(width, height),
            subplot_kw=dict(clip_on=False),
            #gridspec_kw=dict(width_ratios=[station_label_width]+column_width_ratios)
            )

        z = np.array(table[keys[0]])

        for _i, key in enumerate(keys[1:]):
            x = np.array(table[key])
            axes[_i].plot(x, z)

            axes[_i].set_title(labels[key])

            if _i==0:
                axes[_i].set_ylabel('Depth [km]')
            else:
                axes[_i].set_yticklabels([])

            if args.max_depth:
                z_min = 0.
                z_max = args.max_depth

                # rescale x axis
                visible_x = x[((z_min < z) & (z < z_max))]

                xmin = np.min(visible_x)
                xmax = np.max(visible_x)
                xpad = 0.1*(xmax - xmin)

                axes[_i].set_xlim([xmin-xpad, xmax+xpad])

                # rescale y axis
                axes[_i].set_ylim([z_min, z_max])

            axes[_i].invert_yaxis()

        print('  saving %s\n' % (filename+'.png'))
        pyplot.savefig(filename+'.png')


