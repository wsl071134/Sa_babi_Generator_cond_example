def gcd(Am, Bm):
    if Am % Bm == 0:
        return Bm
    else:
        return gcd(Bm, Am % Bm)
