import json

sample_products = [[12345, "Chef's Knife", 20, 35.0], [67890, 'Olive Oil', 50, 10.0],
                   [11111, 'Cast Iron Skillet', 10, 40.0], [22222, 'Large Cooking Pot', 7, 60.0],
                   [33333, 'Cutting Board', 12, 32.0], [44444, 'Oven Mitt', 50, 5.0]]

sample_attach_prod = [[67890, 'Glass', 54321, 'Olive Oil Bottle', 20, 10.0],
                      [44444, 'Plastic', 78912, 'Oven Mit Bedazzle Kit', 10, 5.0],
                      [33333, 'Steel', 13246, 'Cutting Board Rack', 7, 20.0],
                      [11111, 'Clamp', 24356, 'Secondary Skillet Handle', 14, 14.0]]

with open('products.json', 'w') as json_file:
    json.dump(sample_products, json_file)


with open('attach_products.json', 'w') as json_file:
    json.dump(sample_attach_prod, json_file)
