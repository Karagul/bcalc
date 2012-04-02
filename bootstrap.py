import argparse
import math
from errors import Error
from ConfigParser import SafeConfigParser

def getprices(confparser):
    maturity = 1  
    prices = {}
    while True:
        try:
            price = confparser.get(str(maturity), 'price')
        except:
            raise Error("Error in config file, bond price sequence not correct")
        
        prices[maturity] = price
        maturity +=1
        
        try:
            confparser.get(str(maturity), 'price')
        except:
            break
    return prices

def zerocurve(prices, face, coupon):
        finalcf = face + (coupon * face)
        interncf = (coupon * face)

        curve = {}
        curve[1] = (finalcf / float(prices[1])) - 1
        year = 2

        while year <= len(prices):
            tempprice = float(prices[year])
            count = year
            while count > 1:
                count -= 1
                tempprice = tempprice - (interncf / (1+float(curve[count]))**count)
            curve[year] = (finalcf / tempprice) ** (float(1)/year) - 1

            year += 1
        return curve

if __name__ == '__main__':
    
    argparser = argparse.ArgumentParser(description='Zero / Forward Curve Bootstrapper')
    argparser.add_argument('--configfile', dest='conf', type=str, default='bond.ini', help='Configuration File')
    args = argparser.parse_args()
    confparser = SafeConfigParser()
    confparser.read(args.conf)
    
    try:
        face = confparser.get('main', 'face')
        coupon = confparser.get('main', 'coupon')
    except: 
        raise Error("Error in config file, coupon or face not found in main section")
    
    # Get Rates
    prices = getprices(confparser)
    zero = zerocurve(prices, float(face), float(coupon))
    for z in zero:
        print 'Year: %s, Zero Rate: %s' % (z, zero[z])
    

    
