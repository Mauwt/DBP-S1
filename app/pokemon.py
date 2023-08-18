from flask import Blueprint, request, render_template, g
from . import poke_data 
from markupsafe import escape
import random as rd
import requests 


bp = Blueprint('pokemones', __name__, url_prefix='/pokemones', template_folder='templates/pokemones')

@bp.route('/catch', methods=['GET'])
def get_pokemon():
    
    id = rd.randint(0, len(poke_data.pokemones)-1)
    info = {"pokemon": poke_data.pokemones[id]}
    sprites =  requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_data.pokemones[id]['Nombre']}")
    info["sprites"] = sprites.json()["sprites"]["other"]["home"]["front_default"]

    return render_template('get_pokemon.html', info = info)
    

@bp.route('/add_pk', methods=['GET', 'POST'])
def add_pokemon():
    if request.method == 'GET':
        return render_template('add_pokemon.html' , add=False)
    
    if request.method == 'POST':
        poke_data.pokemones.append({
            "Nombre": request.form['nombre'],
            "Tipo": request.form['tipo'],
            "poder": request.form['poder'],
        })

        return render_template('add_pokemon.html', add=True)
    
@bp.route('/update_pk:<int:id>', methods=['GET', 'POST'])
def update_pokemon(id:int):
    poke_info = {
        "pokemon": poke_data.pokemones[id],
        "id": id,
        "update": False
    }

    if request.method == 'GET':
        return render_template('update_pokemon.html', info = poke_info)

    poke_data.pokemones[id]["Nombre"] = request.form["nombre"]
    poke_data.pokemones[id]["Tipo"] = request.form["tipo"]
    poke_data.pokemones[id]["poder"] = request.form["poder"]

    poke_info["update"] = True

    return render_template('update_pokemon.html', info = poke_info)


@bp.route('delete_pk:<int:id>', methods=['GET','DELETE'])   
def delete_pokemon(id:int):
    poke =  poke_data.pokemones[id]
    try:
        poke_data.pokemones.pop(id)
        return render_template('delete_pokemon.html', info = poke)
    except IndexError:
        return "<h1>Index out of range</h1>"


