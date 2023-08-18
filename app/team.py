from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests


bp = Blueprint('team', __name__, url_prefix='/team', template_folder='templates/team')


@bp.route('/add/<string:nombre>/<string:tipo>/<int:poder>', methods=['GET'])
def add_pokemon(nombre:str, tipo:str, poder:int):
    
    if 'team' not in session:
        session['team'] = []
        session['team'].append({
        "Nombre": nombre,
        "Tipo": tipo,
        "poder": poder,
        "imagen": requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre}").json()["sprites"]["front_default"]
    })
    else:
        for i in session['team']:
            if i['Nombre'] == nombre:
                flash('El pokemon ya se encuentra en el equipo')
                return redirect(url_for('team.get_team'))
    
        session['team'].append({
        "Nombre": nombre,
        "Tipo": tipo,
        "poder": poder,
        "imagen": requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre}").json()["sprites"]["front_default"]
    })

    flash(f'{nombre} agregado al equipo')
    return redirect(url_for('team.get_team'))
    

@bp.route('/get_team', methods=['GET'])
def get_team():
    if 'team' not in session:
        session['team'] = []
    return render_template('get_team.html', team=session['team'])   
    
@bp.route('/delete/', methods=['GET', 'POST'])
def delete_pokemon():

    if request.method == 'GET':
        if 'team' not in session:
            session['team'] = []
        return render_template('delete_pokemon.html', team=session['team'])
    
    if request.method == 'POST':
        print("entrp")
        idx = 0
        session.modified = True
        for pk in session['team']:
            if pk['Nombre'] == request.form['nombre'].lower():
                session['team'].pop(idx)
                break
            idx += 1
        return render_template('delete_pokemon.html', team=session['team']) 
    

