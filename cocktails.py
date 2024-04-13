import requests
import tkinter as tk
from io import BytesIO
from PIL import ImageTk, Image


RANDOM_URL = "https://www.thecocktaildb.com/api/json/v1/1/random.php"


def show_random_cocktail():
    cocktail = getRandomCocktail()

    # Update cocktail information labels
    name_label.config(text=f"Name: {cocktail['Name']}")
    category_label.config(text=f"Category: {cocktail['Category']}")
    glass_label.config(text=f"Glass: {cocktail['Glass']}")
    instructions_label.config(text=f"Instructions: {cocktail['Instructions']}", wraplength=300)

    # Update ingredients label
    ingredients_text = "\n".join([f"{ingredient} - {measure}" for ingredient, measure in cocktail['Ingredients']])
    ingredients_label.config(text="Ingredients:\n" + ingredients_text)

    # Display thumbnail image
    image_url = cocktail["Thumbnail"]
    response = requests.get(image_url)
    if response.status_code == 200:
        # Open image using Pillow
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)

        # Update image label
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the PhotoImage object
    else:
        print("Failed to download image")

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
        
        if ingredient is None or measure is None:
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


    # Create main window
    root = tk.Tk()
    root.title("Random Cocktail Viewer")

    # Set fixed size for the window
    root.geometry("800x700")  # Set width and height in 

    ##set background color to black
    root.configure(bg="black")

    # Button to show random cocktail
    show_cocktail_button = tk.Button(root, text="Show Random Cocktail", command=show_random_cocktail,bg="black", fg="#FF69B4")
    show_cocktail_button.pack(side="top",pady=10)

    # Cocktail information labels
    name_label = tk.Label(root, text="", wraplength=400, justify="center",bg="black", fg="#FF69B4")
    name_label.pack(anchor="center")
    category_label = tk.Label(root, text="",justify="center",bg="black", fg="#FF69B4")
    category_label.pack(anchor="center")
    glass_label = tk.Label(root, text="",justify="center",bg="black", fg="#FF69B4")
    glass_label.pack(anchor="center")
    instructions_label = tk.Label(root, text="", wraplength=400, justify="center",bg="black", fg="#FF69B4")
    instructions_label.pack(anchor="center")
    ingredients_label = tk.Label(root, text="",justify="center",bg="black", fg="#FF69B4")
    ingredients_label.pack(anchor="center")

    # Image label
    image_label = tk.Label(root)
    image_label.pack()

    

    # Initially show a random cocktail
    show_random_cocktail()

    root.mainloop()
