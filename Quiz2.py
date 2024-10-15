#2
import requests
import json

def make_pokeapi_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def extract_pokemon_data(data):
    if not data:
        return None

    extracted = {
        "stats": [],
        "name": data.get("name"),
        "sprites": {
            "back_default": data.get("sprites", {}).get("back_default"),
            "back_female": data.get("sprites", {}).get("back_female"),
            "back_shiny": data.get("sprites", {}).get("back_shiny"),
            "back_shiny_female": data.get("sprites", {}).get("back_shiny_female"),
            "front_default": data.get("sprites", {}).get("front_default"),
            "front_female": data.get("sprites", {}).get("front_female"),
            "front_shiny": data.get("sprites", {}).get("front_shiny"),
            "front_shiny_female": data.get("sprites", {}).get("front_shiny_female")
        }
    }

    for stat in data.get("stats", []):
        stat_name = stat.get("stat", {}).get("name")
        if stat_name in ["hp", "attack"]:
            stat_data = {
                "base_stat": stat.get("base_stat"),
                "effort": stat.get("effort"),
                "stat": {
                    "name": stat_name,
                    "url": stat.get("stat", {}).get("url")
                }
            }
            extracted["stats"].append(stat_data)

    return extracted

def main():
    request_id = input("Enter pokemon ID : ")
    pokemon_url = "https://pokeapi.co/api/v2/pokemon/"+  request_id
    pokemon_data = make_pokeapi_request(pokemon_url)
    
    extracted_data = extract_pokemon_data(pokemon_data)
    
    if extracted_data:
        print(json.dumps(extracted_data, indent=2))
    else:
        print("Failed to extract Pokemon data.")

if __name__ == "__main__":
    main()