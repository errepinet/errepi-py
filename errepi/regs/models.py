"""
errepi-py - Python bindings for Errepi Net microservices

Copyright © 2023-2025 Errepi Net S.R.L.
Author: Valerio Faiuolo <valerio.faiuolo@errepinet.it>

All rights reserved. This software is the property of Errepi Net S.R.L.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without express written permission.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from errepi.models import AppInfo


class RegsClientConfiguration(BaseModel):
    """
    Connection configuration for the generic registries client.

    Attributes:
        host: Host of the generic registries microservice.
        port: Port of the generic registries microservice.
    """

    host: str = "localhost"
    port: int = 50051


class State(BaseModel):
    """
    State (country) record.

    Mirrors the State message of protos/generic_regs.proto.
    """

    id: Optional[str] = None
    nome_it: str
    nome_en: str
    stato_o_territorio: str
    area_codice: int
    area_nome: str
    continente_codice: int
    continente_nome: str
    codice_istat: int
    codice_istat_genitore: Optional[int] = None
    codice_iso_3166_alpha2: Optional[str] = None
    codice_iso_3166_alpha3: Optional[str] = None
    codice_iso_3166_alpha3_genitore: Optional[str] = None
    codice_m49: Optional[str] = None
    codice_min: Optional[str] = None
    codice_at: Optional[str] = None


class City(BaseModel):
    """
    Municipality (comune) record.

    Mirrors the City message of protos/generic_regs.proto.
    """

    id: Optional[str] = None
    istat: int
    comune: str
    cap: Optional[str] = None
    regione: str
    provincia: str
    cod_fisco: str
    superficie: float
    state_istat: int
    codice_regione: int


class Cap(BaseModel):
    """
    Postal code (cap) record.

    Mirrors the Cap message of protos/generic_regs.proto.
    """

    id: Optional[str] = None
    istat: int
    cap: str
    citta: Optional[str] = None
    provincia: Optional[str] = None
    provincia_sigla: Optional[str] = None
    stato_it: Optional[str] = None
    stato_en: Optional[str] = None


class Province(BaseModel):
    """
    Province record.

    Mirrors the Province message of protos/generic_regs.proto.
    """

    id: Optional[str] = None
    sigla: str
    provincia: str
    superficie: int
    num_comuni: int
    codice_regione: int
    istat_stato: int
    codice_istat: str


class Region(BaseModel):
    """
    Region record.

    Mirrors the Region message of protos/generic_regs.proto.
    """

    id: Optional[str] = None
    codice_regione: int
    nome_it: str
    ripartizione_geografica: str
