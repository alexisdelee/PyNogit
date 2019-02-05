# NoGit

NoGit est un système de gestion de bases de données clef-valeur scalable utilisant le moteur interne de git.

Ce dépôt contient donc :  
  - un client NoGit en python  
  - une application web de gestion pour les systèmes de gestion de bases de données NoGit  

## Variables d'environnement

  - PYNOGIT_DB (location for the database)  
  - PYNOGIT_HOST (host for client server)  
  - PYNOGIT_PORT (port for client server)  

## Client

Après s'être identifié, un objet NoGit contenant l'accès aux méthodes de gestion est retourné :  
```shell
<instance> = NoGit(username="master", credentials="master", database="mcdo")
```

Info : le paramètre __credentials__ (mot de passe) est facultatif, toutefois les données ne seront pas chiffrées dans le cas de son absence.  

### Insertion

NoGit supporte les nombres entiers, les nombres décimaux, les chaînes de caractères (dit types simples) et les listes (types complexes).  

#### Types simples

```python
# insert a single key
<instance>.set(<key>, <value>, <collection>, [ <expire> ])
# insert several keys
<instance>.mset(<keys>, <values>, <collection>, [ <expire> ])
# insert incrementally
<instance>.incrby(<key>, <step>, <collection>)
<instance>.decrby(<key>, <step>, <collection>)
<instance>.incr(<key>, <collection>) # by one
<instance>.decr(<key>, <collection>) # by one
```

#### Types complexes

```python
<instance>.lpush(<key>, <values>, <collection>)
<instance>.rpush(<key>, <values>, <collection>)
```

### Récupération

#### Types simples

```python
# get a single key
<instance>.get(<key>, <collection>)
# get several keys
<instance>.mget(<keys>, <collection>)
```

#### Types complexes

```python
<instance>.lrange(<key>, <start>, <end>, <collection>)
```

### Suppression

```python
<instance>.delete(<key>, <collection>)
```

### Expiration

```python
# set
<instance>.expire(<key>, <collection>, <seconds>)
# get
<instance>.ttl(<key>, <collection>)
# remove
<instance>.persistent(<key>, <collection>)
```

### Transaction

Avec NoGit, les transactions à la MySQL sont maintenant possibles pour une de base de données de type clef-valeur.  

#### Points de sauvegarde

```python
# no tag
<transaction> = <instance>.begin()
# with tag
<transaction> = <instance>.savepoint(<tag>)
# no tag from a transaction instance
<transaction>.begin()
# with tag a transaction instance
<transaction>.savepoint(<tag>)
```

#### Retour en arrière

```python
# last transaction
<instance>.rollback()
# transaction with a specific tag
<instance>.rollback(<tag>)
# last transaction from a transaction instance
<transaction>.rollback()
# transaction with a specific tag from a transaction instance
<transaction>.rollback(<tag>)
```

#### Etiquettes

```python
<instance>.release(<tag>)
# from a transaction instance
<transaction>.release(<tag>)
```

### Autres méthodes

```python
# get type
<instance>.type(<key>, <collection>)
# check if a variable exists
<instance>.exists(<key>, <collection>, [ <data> ])
```

## Application web

```shell
pip install Flask
pip install flask_cors
pip install pytest

# Windows
"bin/run.bat"

# Linux
bash bin/run.sh
```

## Tests unitaires

```shell
pytest -q tests/main.py
```
