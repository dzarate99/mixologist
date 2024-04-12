import requests

RANDOM_URL = "https://www.thecocktaildb.com/api/json/v1/1/random.php"


def processDrink(drink):
    cocktail = {
        "Name" : drink["strDrink"],
        "Category": drink["strCategory"],
        "Glass" : drink["strGlass"],
        "Instructions": drink["strInstructions"],
        "Thumbnail": drink["strDrinkThumb"]
    }

    ##process each individual ingredients and its corresponding measurements 
    ##format is "strIngredient" + "number". number will be 1-15. if doesnt need all 15 ingredient fields, field will be null
    ##same for measurements 
    ingredients = []
    for i in range(1,16):
        ingredientFieldName = "strIngredient" + str(i)
        measureFieldName = "strMeasure" + str(i)

        ingredient = drink[ingredientFieldName]
        measure = drink[measureFieldName]
        
        if ingredient is None  or measure is None:
            break
        else:
            ingredients.append((ingredient,measure))

    cocktail["Ingredients"] = ingredients
    cocktail["RawJson"] = drink

    return cocktail

def makeApiCall(url):
    response = requests.get(url)
    if(response.status_code == 200):
        drinks = response.json()["drinks"]
        randomDrink = drinks[0]

        cocktailInfo = processDrink(randomDrink)

        return cocktailInfo

    else:
        print('Error:',response.status_code)



def getRandomCocktail():
    return makeApiCall(RANDOM_URL)


if __name__ == "__main__":
    cocktail = getRandomCocktail()
    print("Cocktail: " + cocktail["Name"])
    print("Category: " + cocktail["Category"])
    print("Glass: " + cocktail["Glass"])
    print("Instructions: " + cocktail["Instructions"])
    
    for ingredient_info in cocktail["Ingredients"]:
        print(f"Ingredient: {ingredient_info[0]}; Measure: {ingredient_info[1]}")
