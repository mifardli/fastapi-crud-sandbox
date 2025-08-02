from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello_bocil():
    return {"pesan":"Halo dunia! Ini backend bocil aktif cuy 🚀"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tugas_list = [
    {"id": 1, "judul":"Belajar backend", "status":"belum"},
    {"id":2, "judul":"Sholat maghrib", "status":"sudah"}

]

next_id = 3

@app.get("/tugas")
def get_semua_tugas():
    return {"data": tugas_list}

@app.get("/tugas/{tugas_id}")
def get_tugas_by_id(tugas_id: int):
    for tugas in tugas_list:
        if tugas["id"] == tugas_id:
            return {"data": tugas}
    raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")

class TugasBaru(BaseModel):
    judul: str
    status: str

@app.post("/tugas")
def tambah_tugas(tugas: TugasBaru):
    global next_id
    new_tugas = {
        "id": next_id,
        "judul": tugas.judul,
        "status": tugas.status

    }
    tugas_list.append(new_tugas)
    next_id += 1
    return {"pesan": "Tugas berhasil ditambahkan", "data":new_tugas}

class EditTugas(BaseModel):
    judul: str
    status: str

@app.put("/tugas/{tugas_id}")
def edit_tugas(tugas_id: int, tugas: EditTugas):
    for t in tugas_list:
        if t["id"] == tugas_id:
            t["judul"] = tugas.judul
            t["status"] = tugas.status
            return {"pesan": "Tugas berhasil diubah", "data": t}
    raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")
@app.delete("/tugas/{tugas_id}")
def hapus_tugas(tugas_id: int):
    for i, t in enumerate(tugas_list):
        if t["id"] == tugas_id:
            del tugas_list[i]
            return {"pesan": "Tugas berhasil dihapus"}
        raise HTTPException(status_code=404, detaail="tugas tidak ditemukan")
    