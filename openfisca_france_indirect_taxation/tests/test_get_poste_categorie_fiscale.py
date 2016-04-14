# -*- coding: utf-8 -*-


# Import de modules généraux
from __future__ import division

from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import get_poste_categorie_fiscale


def test():
    confiserie = dict(
        value = ['01.1.8.1.3', '01.1.8.2.1'],
        categorie_fiscale = 'tva_taux_plein'
        )
    # 02 Boissons alcoolisées et tabac
    # alccols forts
    alcools = dict(
        value = '02.1.1.1.1',
        categorie_fiscale = 'alcools_forts',
        )
    # vins et boissons fermentées
    vin = dict(
        value = '02.1.2.1.1',
        categorie_fiscale = 'vin',
        )
    # bière
    biere = dict(
        value = '02.1.3.1.1',
        categorie_fiscale = 'biere',
        )

    for categorie in [confiserie, alcools, vin, biere]:
        postes_coicop = categorie['value']
        categorie_fiscale = categorie['categorie_fiscale']
        if isinstance(postes_coicop, str):
            yield assert_categorie_fiscale, postes_coicop, [categorie_fiscale]
        else:
            for poste_coicop in postes_coicop:
                yield assert_categorie_fiscale, poste_coicop, [categorie_fiscale]


def assert_categorie_fiscale(poste_coicop, categorie_fiscale):
    got = get_poste_categorie_fiscale(poste_coicop)
    assert categorie_fiscale == got, \
        "For poste coicop {} we have wrong categorie fiscale: \n got {} but should be {}".format(
            poste_coicop, got, categorie_fiscale)



if __name__ == '__main__':
    toto = test()