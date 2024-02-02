donc comment pydantic marche? il faut d'abord definir une classe pour representer(dans notre cas ici) ce a quoi un post doit ressembler. En quelque sorte le schema/squelette d'un post
sans le decorateur @app.get/.post/.delete/.head etc la fonction n'est qu'une fonction normal. Pour avoir une api il faut le decorateur
methode http: .get .post .head .delete .put = les plus connues
le path = "/" c'est le root
si on ajoute un login au path ie. "/login" alors l'operation path sera mise en marche ssi l'utilisateur va dans notre url et entre /login
pour preciser au frontend quels types de donnees peuvent etre entrer par un utilisateur(schema de base) on utilise la librairire de pydantic. Pydantic nous permet de preciser les elements pouvant etre saisi ainsi que leur type taille avec la fonction basemodel etc... Il faut importer pydantic et la fonction basemodel "from pydantic import basemodel"
dans notre cas on veut: title: str, content: str
partie 2
toute application doit etre capable de faire ces 4 choses: create(creer), read(lire), update(mise a jour), supprimer(delete): d'ou l'accronyme CRUD
toujours utiliser le pluriel pour les urls
CREATE: POST method url: /posts
READ: GET method url: /posts/{id}
READ: GET method url: /posts
UPDATE: PUT/PATCH method url: /posts/{id}
DELETE: DELETE method url: /posts/{id}
pour creer un dictionnaire a partir des elements entrer dans le schema Post il faut utiliser la methode .model_dump
pour manipuler les reponse http ie. lorsque par exemple un utilisateur essaie d'acceder a une url qui n'existe pas on doit import "Response" de fastapi
Pour se connecter a une base donnee postgres il faut d'abord

-- installer le package psycopg2 et l'importer ensuite. -- il faut aussi importer RealDictCursor de psycopg2.extras.
pour etablir la connexion a notre base il faut

creer une instance de connexion avec la methode connect du package psycopg2 syntaxe: psycopg2.connect(host, database, user, password, cursor_factory) host = l'adresse ip de votre base dans notre cas c'est le localhost database = nom de la base de donnees dans notre cas c'est fastapiDb user = postgres password = mot de passe saisie lors de l'installation de postgresSQL cursor_factory = RealDictCursor
definir une variable qui va nous permetre d'executer les differentes commande sql

cursor = conn.cursor()
utiliser une boucle while pour forcer la connexion avant toute manipulation

pour communiquer avec une base de donnees on va utiliser un ORM (Object-Relational Mapper) c'est une librairie qui permet de communiquer avec une BD sans utiliser les requetes sql, souvent compliquer pour certaines personnes. Avec un ORM comme SQLAlchemy on peut envoyer des requetes sql a une base de donnees en utilisant des objects et des classes.
Note.

Dans un projet avec fastapi il faut avoir un dossier appeler app dans lequel il y aura certain fichier comme init.py, crud.py, database.py, main.py, models.py, schemas.py

le fichier init.py est un fichier vide qui indique a python que app et tous ses module(fichier python) est un package

Tant bien meme qu'ils disposent des methodes et fonctions pour interagir avec les BD, les ORM ne sont pas capable de communiquer directement avec les BD donc ils ont besoin d'un driver pour transmettre les requetes sql a la BD
models

Avec les ORM on n'a plus besoin de creer les tables. Il suffit de definir ces tables comme des models chaque model cree en python correspond a une table dans une base de donnees

lorsque le model(table) n'existe pas dans la BD sqlalchemy va la creer au cas contraire il ne fera rien