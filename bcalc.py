import argparse
import sys
from errors import Error


def calculate(face, coupon, maturity, discount):
    discounted_final_cf = (face + (coupon*face))/(1+discount)**maturity
    dmac = discounted_final_cf * maturity    
    maturity -= 1  
    discounted_cf = 0
    
    while maturity > 0:
        discounted_cf = (coupon*face) + (discounted_cf/(1+discount)**maturity)
        dmac = dmac + discounted_cf
        maturity -= 1 
        
    price = discounted_cf + discounted_final_cf
    dmac = dmac / price
    dmod = dmac / (1+discount)
    
    return price, dmac, dmod

if __name__ == '__main__':
    
    argparser = argparse.ArgumentParser(description='Simple Bond Calculator')
    argparser.add_argument('--face', dest='face', type=float, default='100.00', help='Face value of bond (default $100.00)')
    argparser.add_argument('--coupon', dest='coupon', type=float, help='Coupon rate (Annual)')
    argparser.add_argument('--maturity', dest='maturity', type=int, help='Years to maturity')
    argparser.add_argument('--discount', dest='discount', type=float, help='Discount Rate (Annual)')
    argparser.add_argument('--position', dest='position', type=float, help='Number of bonds in position')
    args = argparser.parse_args()
    
    #TODO: Convert to semi annual payments 
    
    # Validate Input 
    if args.coupon > 1 or args.coupon < 0:
        raise Error ('Coupon must be between 0 and 1')
    
    if args.discount > 1 or args.coupon < 0:
        raise Error ('Coupon must be between 0 and 1')
        
    # Figure out what needs to be calculated 
    try:
        price, dmac, dmod = calculate(args.face, args.coupon, float(args.maturity), args.discount) 
        mv = (args.position * price/100 * args.face)
    except TypeError:
        raise Error ('Error in input, please check')
    
    # Output 
    print('Simple Bond Calculator') 
    print('Face: $%s' % args.face) 
    print('Coupon (Annual): $%s' % (args.coupon*args.face)) 
    print('Price: $%s' % price) 
    print('Maturity: %s years' % args.maturity) 
    print('Discount: %s' % args.discount) 
    print('DMac: %s' %dmac) 
    print('DMod: %s' %dmod) 
    print('Market Value: %s' % mv)   
    print('Dollar Duration: %s' % (mv*dmod))     
    print('DV01: %s' % ((mv*dmod) * 0.01)) 
    
    