class ChaiUtils:
    default_ingredients = "water, milk, ginger"

    @classmethod
    def clean_default(cls):
        return [item.strip() for item in cls.default_ingredients.split(",")]

    def __init__(self, recipe):
        self.recipe = recipe

    def clean_recipe(self):
        return [item.strip() for item in self.recipe.split(",")]
default_ingredients = "water, milk, ginger  "
ch = ChaiUtils(default_ingredients);
print(ChaiUtils.clean_default());