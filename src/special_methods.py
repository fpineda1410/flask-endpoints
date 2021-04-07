from models import db, User,Character,Planet,FavoritePlanet,FavoriteCharacter


def get_merged_lists(current_user_id):
    try:
        favorite_character = FavoriteCharacter.query.filter_by(user_id=current_user_id)
    except:
        favorite_character=[]
    try:
        favorite_planet = FavoritePlanet.query.filter_by(user_id=current_user_id)
    except:
        favorite_character=[]
    favorite_planet_serial = list(map(lambda favorite: favorite.serialize(), favorite_planet))
    favorite_character_serial = list(map(lambda favorite: favorite.serialize(), favorite_character))
    complete_list=favorite_character_serial + favorite_planet_serial
    return complete_list

def update_filter_planet (planet_list,current_user_id):
    try:
        #delete the removed values from the database-then append the new ones
        favorite_planet = FavoritePlanet.query.filter_by(user_id=current_user_id)
        serialized_items = list(map(lambda favorite: favorite.serialize(), favorite_planet))
        for old_db_item in range (len(serialized_items)):
            if old_db_item[i]['id'] not in planet_list:
                #if old item in DB is not in the new list emitted by the user then erase it and update DB
                item_to_delete  = FavoritePlanet.query.filter_by(user_id=current_user_id,id=old_db_item["id"]).first()
                db.session.delete(item_to_delete)
        db.session.commit()

        new_favorite_planet = FavoritePlanet.query.filter_by(user_id=current_user_id)
        new_serialized_items = list(map(lambda favorite: favorite.serialize(), favorite_planet))
        new_serialized_items_dict =[]
        for updated_db_item in range (len(serialized_items)):
            new_serialized_items_dict.append(updated_db_item[i]['id'])
        for new_item in planet_list:
            if new_item not in new_serialized_items:
                item_to_add=FavoritePlanet(user_id=current_user_id, planet_id =new_item)
                db.session.add(item_to_add)
        db.session.commit()
    except:
        #the DB favorite was empty proceed to insert all values in planet_list
        for json_item in planet_list:
            newPlanetFavorite = FavoritePlanet(user_id=current_user_id, planet_id = json_item)
            db.session.add(newPlanetFavorite)
        db.session.commit()


def update_filter_character (character_list,current_user_id):
    try:
        #delete the removed values from the database-then append the new ones
        favorite_character = FavoriteCharacter.query.filter_by(user_id=current_user_id)
        serialized_items = list(map(lambda favorite: favorite.serialize(), favorite_character))
        for item in range (len(serialized_items)):
            print(serialized_items[item]['id'])
            if serialized_items[item]['id'] not in character_list:
                print(True)
                #if old item in DB is not in the new list emitted by the user then erase it and update DB
                item_to_delete  = FavoriteCharacter.query.filter_by(user_id=current_user_id, id=serialized_items[item]['id'])
                db.session.delete(item_to_delete)

        db.session.commit()

        new_favorite_character = FavoriteCharacter.query.filter_by(user_id=current_user_id)
        new_serialized_items = list(map(lambda favorite: favorite.serialize(), favorite_character))
        new_serialized_items_dict =[]
        for updated_db_item in range (len(serialized_items)):
            new_serialized_items_dict.append(updated_db_item[i]['id'])
        for new_item in character_list:
            if new_item not in new_serialized_items:
                item_to_add=FavoriteCharacter(user_id=current_user_id, character_id =new_item)
                db.session.add(item_to_add)

        db.session.commit()
    except:
        #the DB favorite was empty proceed to insert all values in planet_list
        for json_item in character_list:
            newCharacterFavorite = FavoriteCharacter(user_id=current_user_id, character_id = json_item)
            db.session.add(newCharacterFavorite)
        db.session.commit()


def update_favorites_lists (payload_from_request,current_user_id):
    planet_dict=[]
    characters_dict=[]
    #if payload comes with data
    #this data can contain planets or characters or both
    for json_item in payload_from_request:
        # print(type(json_item['category']))
        if (json_item['category'] == "PLANET"):
            planet_dict.append(json_item["planet_id"]) #[12,5,6,14] how it will look
        if (json_item['category'] == "CHARACTER"):
            characters_dict.append(json_item["character_id"]) #[12,5,6,14] how it will look
    if (len(planet_dict)>0):
        update_filter_planet(planet_dict,current_user_id)
    if (len(characters_dict)>0):
        update_filter_character(characters_dict,current_user_id)
    updated_list = get_merged_lists(current_user_id)
    return updated_list