"""Páginas do site, uma área por arquivo (cada uma usa a pasta de mesmo nome em templates/)."""

from backend.rotas import compilador, desafio_diario, estudo, painel, publico, revisao


def registrar_rotas(app):
    for area in (publico, painel, estudo, desafio_diario, revisao, compilador):
        app.register_blueprint(area.bp)
