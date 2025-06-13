back du projet datamining

Route /version - GET

Retourne 
{
    "version": {Version de l'API}
}

Route /upload - POST

Payload
{
    "file_name":"{file name}",
    "delimiter": "{delimiter to string}",
    "file_data": {BASE_64 encoded data}
}

Retourne 

{ } -> Si succès
Sinon 
{'error': {description de l'erreur}}
