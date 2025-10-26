from fastapi import Body, FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description= "Айди"),
    title: str | None = Query(None, description= "Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed= True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "ok"}
    

@app.delete("/hotels/{hotel_id}")
def del_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "ok"}

@app.put("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    new_name: str = Body(embed= True),
    new_title: str = Body(embed= True)
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = new_name
            hotel["title"] = new_title
            return hotel
    return {"status": "object is not finded"}

@app.patch("/hotels/{id}")
def change_param(
    id: int,
    new_name: str | None = Body(embed= True),
    new_title: str | None = Body(embed= True)
):
    for hotel in hotels:
        if hotel["id"] == id:
            if new_name:
                hotel["name"] = new_name
            if new_title:
                hotel["title"] = new_title
            if not (new_name or new_title):
                return {"status": "object parameters have not modified"}
            return hotel
    return {"status": "object is not finded"}
