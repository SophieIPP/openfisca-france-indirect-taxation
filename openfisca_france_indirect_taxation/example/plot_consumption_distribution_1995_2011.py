# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 15:43:49 2015

@author: germainmarchand
"""

# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, percent_formatter


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Exemple: graphe par décile de revenu par uc de la ventilation de la consommation
    # selon les postes agrégés de la CN
    # Liste des coicop agrégées en 12 postes
    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'niveau_vie_decile',
        'revtot',
        'ocde10',
        'niveau_de_vie',
        'rev_disponible',
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    for year in [2000, 2005, 2011]:
        # Constition d'une base de données agrégée par décile (= collapse en stata)
        df = simulate_df(var_to_be_simulated, year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10
        list_part_coicop12 = []
        df['depenses_tot'] = 0
        for i in range(1, 13):
            df['depenses_tot'] += df['coicop12_{}'.format(i)]

        var_to_concat = list_coicop12 + ['depenses_tot']
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = var_to_concat)

        for i in range(1, 13):
            Wconcat['part_coicop12_{}'.format(i)] = Wconcat['coicop12_{}'.format(i)] / Wconcat['depenses_tot']
            'list_part_coicop12_{}'.format(i)
            list_part_coicop12.append('part_coicop12_{}'.format(i))

        df_to_graph = Wconcat[list_part_coicop12].copy()
        df_to_graph.columns = [
            'Alimentaire', 'Alcool + Tabac', 'Habits', 'Logement', 'Meubles', u'Santé', 'Transport',
            'Communication', 'Loisir & culture', 'Education', u'Hôtel & restaurant', 'Bien & services divers'
            ]

    # TODO: vérifier si les postes COICOP12 sont bien les suivants (en particulier les 8 premiers)
    # RAPPEL : 12 postes CN et COICOP
    #    01 Produits alimentaires et boissons non alcoolisées
    #    02 Boissons alcoolisées et tabac
    #    03 Articles d'habillement et chaussures
    #    04 Logement, eau, gaz, électricité et autres combustibles
    #    05 Meubles, articles de ménage et entretien courant de l'habitation
    #    06 Santé
    #    07 Transports
    #    08 Communication
    #    09 Loisir et culture
    #    10 Education
    #    11 Hotels, cafés, restaurants
    #    12 Biens et services divers

        axes = df_to_graph.plot(
            kind = 'bar',
            stacked = True,
            color = ['#FF0000', '#006600', '#660066', '#0000FF', '#FFFF00', '#999966', '#FF6699', '#00FFFF',
                     '#CC3300', '#990033', '#3366CC', '#000000']
            )
        plt.axhline(0, color = 'k')

            # TODO utiliser format et corriger également ici
            # https://github.com/openfisca/openfisca-matplotlib/blob/master/openfisca_matplotlib/graphs.py#L123
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

        # Supprimer la légende du graphique
        axes.legend(
            bbox_to_anchor = (1.6, 1.0),
            ) # TODO: supprimer la légende pour les lignes pointillées et continues
    plt.show()
        # plt.savefig('C:\Users\hadrien\Desktop\Travail\ENSAE\Statapp\graphe_ventilation_consommation_niveau_vie_decile.eps', format='eps', dpi=1000)

        # TODO: analyser, changer les déciles de revenus en déciles de consommation
        # faire un truc plus joli, mettres labels...
