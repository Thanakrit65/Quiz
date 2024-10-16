#2
import requests
import json

def make_pokeapi_request(url): #check response error
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def extract_pokemon_data(stat_info,name_info): #returnแบบJsonตามตัวอย่าง

    extracted = {
        "stats": [],
        "name": name_info.get("name"),
        "sprites": {
            "back_default": name_info.get("sprites", {}).get("back_default"),
            "back_female": name_info.get("sprites", {}).get("back_female"),
            "back_shiny": name_info.get("sprites", {}).get("back_shiny"),
            "back_shiny_female": name_info.get("sprites", {}).get("back_shiny_female"),
            "front_default": name_info.get("sprites", {}).get("front_default"),
            "front_female": name_info.get("sprites", {}).get("front_female"),
            "front_shiny": name_info.get("sprites", {}).get("front_shiny"),
            "front_shiny_female": name_info.get("sprites", {}).get("front_shiny_female")
        }
    }
    for stat in stat_info.get("stats", []):
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
    request_id = input("Enter pokemon ID : ") #รับค่าid
    url_stats = "https://pokeapi.co/api/v2/pokemon/"+  request_id # stats มาจากลิงค์นี้
    pokemon_stats = make_pokeapi_request(url_stats) 
    url_name = "https://pokeapi.co/api/v2/pokemon-form/"+  request_id #name and sprites มาจากลิงค์นี้
    pokemon_name = make_pokeapi_request(url_name) 
    
    extracted_data = extract_pokemon_data(pokemon_stats,pokemon_name)
    
    if extracted_data:
        print(json.dumps(extracted_data, indent=2))
    else:
        print("Failed to extract Pokemon data.")

if __name__ == "__main__":
    main()