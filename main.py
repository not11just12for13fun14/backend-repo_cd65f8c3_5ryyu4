import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from typing import List, Dict, Any

from database import create_document, db
from schemas import Lead, ContactMessage

app = FastAPI(title="Nettoyage Lausanne API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend pour Entreprise de Nettoyage à Lausanne"}


@app.get("/api/services")
def get_services() -> List[Dict[str, Any]]:
    return [
        {
            "id": "residential",
            "title": "Nettoyage résidentiel",
            "description": "Ménage complet, dépoussiérage, sols, salles de bain et cuisines.",
            "price_from": 120,
            "unit": "CHF / intervention"
        },
        {
            "id": "commercial",
            "title": "Nettoyage commercial",
            "description": "Bureaux, commerces et espaces professionnels impeccables.",
            "price_from": 180,
            "unit": "CHF / intervention"
        },
        {
            "id": "end-of-lease",
            "title": "Fin de bail",
            "description": "Nettoyage en profondeur pour état des lieux sans stress.",
            "price_from": 350,
            "unit": "CHF / forfait"
        },
        {
            "id": "windows",
            "title": "Nettoyage de vitres",
            "description": "Vitres et encadrements sans traces, intérieur / extérieur.",
            "price_from": 90,
            "unit": "CHF / intervention"
        },
        {
            "id": "regular",
            "title": "Entretien récurrent",
            "description": "Passages hebdomadaires ou mensuels selon vos besoins.",
            "price_from": 49,
            "unit": "CHF / heure"
        }
    ]


@app.post("/api/lead")
def create_lead(lead: Lead):
    try:
        doc_id = create_document("lead", lead)
        return {"success": True, "id": doc_id}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement: {str(e)}")


@app.post("/api/contact")
def create_contact(message: ContactMessage):
    try:
        doc_id = create_document("contactmessage", message)
        return {"success": True, "id": doc_id}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement: {str(e)}")


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
