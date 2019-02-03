# *Projet Data-Engineering E4 

from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *

# Configuration du systeme
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='maclesecrete'))
client = MongoClient('localhost:27017')
db = client.TaskManager

if db.settings.find({'name': 'task_id'}).count() <= 0:
    print("Tache non trouvee...")
    db.settings.insert_one({'name':'task_id', 'value':0})

def modifID(value): # fonction permettant de donner un ID à chaque évenement de manière croissante
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name':'task_id'},
        {'$set':
            {'value':task_id}
        })

def rdvCreate(form): #fonction permettant la création d'un nouvel évenement
    date = form.date.data
    heure = form.heure.data
    description = form.description.data
    task_id = db.settings.find_one()['value']
    
    task = {'id':task_id, 'date':date, 'description':description, 'heure':heure}

    db.tasks.insert_one(task)
    modifID(1)
    return redirect('/')

def rdvSupprimer1(form): # fonction permettant de supprimer n'importe quel évenement en introduisant son ID
    id = form.id.data
    if(id):
        print(id, type(id))
        db.tasks.delete_many({'id':int(id)})

    return redirect('/')

def rdvModifier(form): # fonction permettant de modifier la description d'un évenement en introduisant son ID
    id = form.id.data
    description = form.description.data
    
    db.tasks.update_one(
        {"id": int(id)},
        {"$set":
            {"description": description}
        }
    )

    return redirect('/')

def reinit_tache(form): # reinitialisation de la liste des évenements de l'agenda
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name':'task_id', 'value':0})
    return redirect('/')

@app.route('/', methods=['GET','POST'])
def main():
    # Création de chaque bloc d'évenements'
    cform = RdvCreate(prefix='cform')
    dform = RdvSupprimer(prefix='dform')
    uform = RdvModifier(prefix='uform')
    reinit = Reinit(prefix='reinit')

    # Réponses de chaque requête
    if cform.validate_on_submit() and cform.creer.data:
        return rdvCreate(cform)
    if dform.validate_on_submit() and dform.supprimer.data:
        return rdvSupprimer1(dform)
    if uform.validate_on_submit() and uform.modifier.data:
        return rdvModifier(uform)
    if reinit.validate_on_submit() and reinit.reinit.data:
        return reinit_tache(reinit)

    # Lecture de toutes les données
    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)

    return render_template('home.html', cform = cform, dform = dform, uform = uform, \
            data = data, reinit = reinit) # on retourne les données de chaques évenements

if __name__=='__main__':
    app.run(debug=True)
