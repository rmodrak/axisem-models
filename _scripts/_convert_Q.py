#!/usr/bin/env python

# TODO - ADD CITATIONS


def Q_alpha(Q_kappa, Q_mu, alpha, beta):
    return (
               (1. - 4./3.*beta**2/alpha**2)*Q_kappa**-1 + 
               4./3.*(beta**2/alpha**2)*Q_mu**-1
           )**-1


def Q_kappa(Q_alpha, Q_beta, alpha, beta):
    return (
               (Q_alpha**-1 - 4./3.*(beta**2/alpha**2)*Q_beta**-1) * 
               (1. - 4./3.*beta**2/alpha**2)**-1
           )**-1



