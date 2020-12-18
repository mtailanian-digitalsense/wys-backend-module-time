# API Endpoints for Times

Port: 8087

## Get a estimated time for a project given m2

**URL** : `/api/times`

**Method** : `POST`

**Auth required** : YES

**Body**:
```json
{
    "adm_agility": "low", // low, normal, high
    "client_agility": "normal", // low, normal, high
    "mun_agility": "high", // low, normal, high
    "construction_mod": "const_adm", // const_adm, turnkey, general_contractor 
    "constructions_times": "daytime",// daytime, nightime, free
    "procurement_process": "direct", // direct, bidding
    "demolitions": "yes", //yes, no
    "m2": 569.0
}
```

### Success Response

**Code** : `200 OK`

**Content example:** 
````json
{
    "weeks": 5
}
````

### Error Responses

**Condition** : If body is invalid

**Code** : `400 Bad Request`

**Content** : `{error_message}`

### Or

**Condition** :  If server or database has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`

## Get a estimated time for a project given m2

**URL** : `/api/times/detailed`

**Method** : `POST`

**Auth required** : YES

**Body**:
```json
{
    "adm_agility": "low", // low, normal, high
    "client_agility": "normal", // low, normal, high
    "mun_agility": "high", // low, normal, high
    "construction_mod": "const_adm", // const_adm, turnkey, general_contractor 
    "constructions_times": "daytime",// daytime, nightime, free
    "procurement_process": "direct", // direct, bidding
    "demolitions": "yes", //yes, no
    "m2": 569.0
}
```

### Success Response

**Code** : `200 OK`

**Content example:** 
````json
[
  {
    "id": 1,
    "name": "Arriendo",
    "sub_categories": [{
      "id": 2,
      "name": "Arriendo",
      "is_milestone": false,
      "duration": 1 // weeks
    },{
      "id": 2,
      "name": "Negociación",
      "is_milestone": false,
      "duration": 3 // weeks
    }]  
  },
  {
    "id": 6,
    "name": "diseño",
    "sub_categories": [{
      "id": 2,
      "name": "Levantamiento de Requerimientos",
      "is_milestone": false,
      "duration": 5 // weeks
    },{
      "id": 3,
      "name": "aprobación del cliente",
      "is_milestone": true,
      "duration": 0 // weeks
    }]
  }  
]
````

### Error Responses

**Condition** : If body is invalid

**Code** : `400 Bad Request`

**Content** : `{error_message}`

### Or

**Condition** :  If server or database has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`

## Save a config to estimate the time for a project given m2

**URL** : `/api/times/save`

**Method** : `POST`

**Auth required** : YES

**Body**:
```json
{
    "project_id": 1,
    "adm_agility": "low", // low, normal, high
    "client_agility": "normal", // low, normal, high
    "mun_agility": "high", // low, normal, high
    "construction_mod": "const_adm", // const_adm, turnkey, general_contractor 
    "constructions_times": "daytime",// daytime, nightime, free
    "procurement_process": "direct", // direct, bidding
    "demolitions": "yes", //yes, no
    "m2": 569.0,
    "weeks": 0 //weeks to move
}
```

### Success Response

**Code** : `200 OK`

**Content example:** 
````json
{
    "id": 1,
    "adm_agility": "low", // low, normal, high
    "client_agility": "normal", // low, normal, high
    "mun_agility": "high", // low, normal, high
    "construction_mod": "const_adm", // const_adm, turnkey, general_contractor 
    "constructions_times": "daytime",// daytime, nightime, free
    "procurement_process": "direct", // direct, bidding
    "demolitions": "yes", //yes, no
    "m2": 569.0
}

````
### Error Responses

**Condition** : If body is invalid

**Code** : `400 Bad Request`

**Content** : `{error_message}`

### Error Responses

**Condition** : If body is invalid

**Code** : `404 Project Not Found`

**Content** : `{error_message}`

### Or

**Condition** :  If server or database has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`

## Get a config 
**URL** : `/api/times/saved/{id}`

**Method** : `GET`

**Auth required** : YES

### Success Response

**Code** : `200 OK`

**Content example:** 
````json
{
    "id": 1,
    "adm_agility": "low", // low, normal, high
    "client_agility": "normal", // low, normal, high
    "mun_agility": "high", // low, normal, high
    "construction_mod": "const_adm", // const_adm, turnkey, general_contractor 
    "constructions_times": "daytime",// daytime, nightime, free
    "procurement_process": "direct", // direct, bidding
    "demolitions": "yes", //yes, no
    "m2": 569.0,
    "weeks": 5
}
````
### Error Responses

**Condition** : If body is invalid

**Code** : `404 Time Generated Config Not Found`

**Content** : `{error_message}`

### Or

**Condition** :  If server or database has some error.

**Code** : `500 Internal Error Server`

**Content** : `{error_message}`
