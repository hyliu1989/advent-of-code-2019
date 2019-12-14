import numpy as np

def manufacture_FUEL(amount):
    # mapping the name of the output chemical to its minimum quantity and the input chemicals
    formula_dict = {}
    what_it_produces = {}

    with open('day14-input.txt', 'r') as f:
        while True:
            formula = f.readline()
            if formula == '':
                break
            in_chemicals, out_chemical = formula.split('=>')

            quantity, out_chem_name = out_chemical[:-1].rstrip(' ').lstrip(' ').split(' ')

            formula_dict_key = out_chem_name
            formula_dict_entry = [int(quantity)]

            for in_chem in in_chemicals.split(','):
                quantity, in_chem_name = in_chem.rstrip(' ').lstrip(' ').split(' ')
                formula_dict_entry.append((in_chem_name,int(quantity)))

                if what_it_produces.get(in_chem_name) is None:
                    what_it_produces[in_chem_name] = set()
                what_it_produces[in_chem_name].add(out_chem_name)

            formula_dict[formula_dict_key] = formula_dict_entry

    what_it_produces['FUEL'] = set()
    required_dict = {'FUEL':amount}
    ORE_count = 0

    while True:
        ok = False
        for chemical in required_dict.keys():
            if len(what_it_produces[chemical]) == 0:
                amount_required = required_dict.pop(chemical)
                ok = True
                break
        assert ok

        formula = formula_dict[chemical]
        amount_produced = formula[0]

        times_apply = int(np.ceil(amount_required / amount_produced))

        for chem_req, quan_req in formula[1:]:
            if chem_req == 'ORE':
                ORE_count += quan_req*times_apply
                continue
            if required_dict.get(chem_req) is None:
                required_dict[chem_req] = 0
            required_dict[chem_req] += quan_req*times_apply
            what_it_produces[chem_req].remove(chemical)

        # print(required_dict)

        if len(required_dict) == 0:
            break

    return ORE_count

#                                    # 1000000000000
# print(manufacture_FUEL(1000000))   #  385319967221
# print(manufacture_FUEL(10000000))  # 3853199105974
# print(manufacture_FUEL(3000000))   # 1155959723925
# print(manufacture_FUEL(2500000))   #  963299823499

fuel_amount_range = [2500000, 3000000]
while fuel_amount_range[1] - fuel_amount_range[0] > 1:
    fuel_amount = (fuel_amount_range[1] + fuel_amount_range[0]) // 2
    ore_amount = manufacture_FUEL(fuel_amount)

    if ore_amount < 1000000000000:
        fuel_amount_range[0] = fuel_amount
    else:
        fuel_amount_range[1] = fuel_amount
print(fuel_amount_range)
