def convert_to_kgs(mass, units):
    """Function has two parmeters: a number that is a mass quantity 
    and a string that is a unit of measurement for mass. Returns 
    the equivaent mass as measured in kilograms."""
    to_kgs = {
        'lbs' : 0.453592,
        'oz' : 0.0283495,
        'mg' : 0.000001,
        'g' : 0.001,
        'kg' : 1,
        'ton (Metric)' : 1000,
        'ton (US)' : 907.185,
        'ton (Imperial)' : 1016.05,
        'st' : 6.35029,
    }
    return mass * to_kgs[units]

def convert_from_kgs(mass, units):
    """Function has two parmeters: a number that is a mass quantity 
    mesured in kilograms and a string that is a unit of measurement 
    for mass. Returns the equivaent mass as measured in the 
    specified units."""
    from_kgs = {
        'lbs' : 2.20462,
        'oz' : 35.274,
        'mg' : 1000000,
        'g' : 1000,
        'kg' : 1,
        'ton (Metric)' : 0.001,
        'ton (US)' : 0.00110231,
        'ton (Imperial)' : 0.000984207,
        'st' : 0.157473,
    }
    return mass * from_kgs[units]
