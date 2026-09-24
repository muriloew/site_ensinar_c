"""Páginas do site, uma área por arquivo (cada uma usa a pasta de mesmo nome em templates/)."""

from backend.rotas import compilador, conta, desafio_diario, estudo, painel, professor, publico, revisao


def registrar_rotas(app):
    for area in (publico, conta, painel, estudo, desafio_diario, revisao, compilador, professor):
        app.register_blueprint(area.bp)
