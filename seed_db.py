"""
Script para poblar la base de datos con datos de prueba.
Uso: python seed_db.py
"""

from src.core.exceptions import AppException
from src.crud import Candidate_crud, Voter_crud, Vote_crud
from src.database.config import SessionLocal, create_tables
from src.schemas.Candidate_schema import CandidateCreate
from src.schemas.Voter_schema import VoterCreate
from src.schemas.Vote_schema import VoteCreate

CANDIDATES = [
    {"name": "Ana Torres", "party": "Partido 1"},
    {"name": "Guillermo Diaz", "party": "Partido 2"},
    {"name": "Yoel Ramirez", "party": "Partido 3"},
]

VOTERS = [
    {"name": "Juan Osorio", "email": "juanosorio14@gmail.com"},
    {"name": "Laura Diaz", "email": "laudiaz@gmail.com"},
    {"name": "Carlos Fajardo", "email": "carlosfajardo1@gmail.com"},
    {"name": "Sofia Lopez", "email": "sofia.lopez@gmail.com"},
    {"name": "Miguel Castro", "email": "miguelcast@gmail.com"},
]

# indice del votante -> indice del candidato por el que vota
VOTES = [(0, 0), (1, 0), (2, 1), (3, 2), (4, 0)]


def seed() -> None:
    create_tables()
    db = SessionLocal()
    try:
        created_candidates = []
        for c in CANDIDATES:
            try:
                created_candidates.append(
                    Candidate_crud.create_candidate(db, CandidateCreate(**c))
                )
                print(f"Candidato creado: {c['name']}")
            except AppException as e:
                print(f"Saltando candidato '{c['name']}': {e.message}")

        created_voters = []
        for v in VOTERS:
            try:
                created_voters.append(Voter_crud.create_voter(db, VoterCreate(**v)))
                print(f"Votante creado: {v['name']}")
            except AppException as e:
                print(f"Saltando votante '{v['name']}': {e.message}")

        for voter_idx, candidate_idx in VOTES:
            if voter_idx >= len(created_voters) or candidate_idx >= len(
                created_candidates
            ):
                continue
            try:
                Vote_crud.cast_vote(
                    db,
                    VoteCreate(
                        voter_id=created_voters[voter_idx].id,
                        candidate_id=created_candidates[candidate_idx].id,
                    ),
                )
                print(
                    f"Voto registrado: {VOTERS[voter_idx]['name']} -> {CANDIDATES[candidate_idx]['name']}"
                )
            except AppException as e:
                print(f"Saltando voto: {e.message}")

        print("\nSeed completado.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
