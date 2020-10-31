import logging

from sage.all import ZZ
from sage.all import Zmod

from small_roots.coron import integer_bivariate
from small_roots.howgrave_graham import modular_univariate


def factorize_univariate(n, bitsize, msb_known, msb, lsb_known, lsb, m_start=1):
    """
    Recovers the prime factors from a modulus using Coppersmith's method.
    :param n: the modulus
    :param bitsize: the amount of bits of the target prime factor
    :param msb_known: the amount of known most significant bits of the target prime factor
    :param msb: the known most significant bits of the target prime factor
    :param lsb_known: the amount of known least significant bits of the target prime factor
    :param lsb: the known least significant bits of the target prime factor
    :param m_start: the m value to start at for the Howgrave-Graham small roots method (default: 1)
    :return: a tuple containing the prime factors
    """
    x = Zmod(n)["x"].gen()
    f = msb * 2 ** (bitsize - msb_known) + x * 2 ** lsb_known + lsb
    bound = 2 ** (bitsize - msb_known - lsb_known)
    m = m_start
    while True:
        t = m
        logging.debug(f"Trying m = {m}, t = {t}...")
        for root in modular_univariate(f, n, m, t, bound):
            p = msb * 2 ** (bitsize - msb_known) + root * 2 ** lsb_known + lsb
            if p != 0 and n % p == 0:
                return p, n // p

        m += 1


def factorize_bivariate(n, p_bitsize, p_msb_known, p_msb, p_lsb_known, p_lsb, q_bitsize, q_msb_known, q_msb, q_lsb_known, q_lsb, k_start=1):
    """
    Recovers the prime factors from a modulus using Coppersmith's method.
    For more complex combinations of known bits, the coron module in the small_roots package should be used directly.
    :param n: the modulus
    :param p_bitsize: the amount of bits of the first prime factor
    :param p_msb_known: the amount of known most significant bits of the first prime factor
    :param p_msb: the known most significant bits of the first prime factor
    :param p_lsb_known: the amount of known least significant bits of the first prime factor
    :param p_lsb: the known least significant bits of the first prime factor
    :param q_bitsize: the amount of bits of the second prime factor
    :param q_msb_known: the amount of known most significant bits of the second prime factor
    :param q_msb: the known most significant bits of the second prime factor
    :param q_lsb_known: the amount of known least significant bits of the second prime factor
    :param q_lsb: the known least significant bits of the second prime factor
    :param k_start: the k value to start at for the Coron small roots method (default: 1)
    :return: a tuple containing the prime factors
    """
    x, y = ZZ["x, y"].gens()
    f = (p_msb * 2 ** (p_bitsize - p_msb_known) + x * 2 ** p_lsb_known + p_lsb) * (q_msb * 2 ** (q_bitsize - q_msb_known) + y * 2 ** q_lsb_known + q_lsb) - n
    xbound = 2 ** (p_bitsize - p_msb_known - p_lsb_known)
    ybound = 2 ** (q_bitsize - q_msb_known - q_lsb_known)
    k = k_start
    while True:
        logging.debug(f"Trying k = {k}...")
        for xroot, yroot in integer_bivariate(f, k, xbound, ybound):
            p = p_msb * 2 ** (p_bitsize - p_msb_known) + xroot * 2 ** p_lsb_known + p_lsb
            q = q_msb * 2 ** (q_bitsize - q_msb_known) + yroot * 2 ** q_lsb_known + q_lsb
            if p * q == n:
                return p, q

        k += 1
