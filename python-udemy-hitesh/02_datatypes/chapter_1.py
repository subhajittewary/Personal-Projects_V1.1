sugar_amount = 2
print(f"Initial sugar: {sugar_amount}")
print(f"ID of 2: {id(sugar_amount)}")

sugar_amount = 12
print(f"Second Initial sugar: {sugar_amount}")
# The ID of 12 will be different from the ID of 2 because integers are immutable in Python. When we assign a new value to sugar_amount, it creates a new integer object in memory, and sugar_amount now references this new object. Therefore, the ID of 12 will be different from the ID of 2.
print(f"ID of 12: {id(sugar_amount)}")