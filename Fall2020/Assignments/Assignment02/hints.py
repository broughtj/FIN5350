import numpy as np

def bond_factory(face: float, coupon: float, frequency: int, maturity: int) -> np.ndarray:
    the_bond = np.full(maturity * frequency, (coupon  * face) / frequency)
    the_bond[-1] += face
    return the_bond

def bond_price(rate: float, the_bond: np.ndarray) -> float:
    disc = np.array([1.0 / ((1.0 + rate) ** i) for i in range(1, the_bond.shape[0] + 1)])
    return np.dot(disc, the_bond)

def bond_yield(price: float, the_bond: np.ndarray) -> float:
    tolerance = 10.0 ** -8
    lower = 0.0
    upper = 2.0 ## something extreme, but this isn't perfect yet!
    guess = 0.5 * (lower + upper)
    diff = price - bond_price(guess, the_bond)
    tries = 0
    
    while abs(diff) >= tolerance:
        tries += 1
        if diff <= 0.0:
            lower = guess
        else:
            upper = guess
        guess = 0.5 * (lower + upper)
        diff = price - bond_price(guess, the_bond)
        
    return (tries, guess)
            

## main
face_value = 1000.0
coupon_rate = .08
frequency = 2
maturity = 12
ytm = .08 / frequency


## Solve for a bond price
the_bond = bond_factory(face_value, coupon_rate, frequency, maturity)
the_price = bond_price(ytm, the_bond)
print(f"The bond price is: ${the_price:,.2f}")


## Now solve for a bond price given the yield
## Test: this should match up with the above
tries, the_yield = bond_yield(the_price, the_bond)
print(f"Found the YTM of {the_yield : 0.4f} in {tries} tries")