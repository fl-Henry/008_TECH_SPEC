import os
import sys
import shutil
import random
import codecs
import pymongo
import argparse
import pdfquery
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from time import sleep

import pdf_parser as pp
import general_methods as gm





def main():
    # print(len("LISTA DE ACUERDOS"))
    # tag = '<LTTextLineHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" word_margin="0.1"><LTTextBoxHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" index="2">No. </LTTextBoxHorizontal></LTTextLineHorizontal>'
    # tag = pp.get_tag_by_attr_position(20, tag)
    # print(tag[-1])
    # tag = '<LTTextBoxHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" index="2">No. </LTTextBoxHorizontal>'
    # tag = pp.get_tag_by_attr_position(20, tag)
    # print(tag[-1])

    # in_string = '<LTTextBoxHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" index="2">No. </LTTextBoxHorizontal>'
    # str_find = "Horizontal"
    # poses = gm.find_string_indexes(in_string, str_find)
    # print(poses)
    # print(in_string[poses[0]:poses[1]])

    e_fields = [
        "SOCORRO MORALES GONZALEZ Vs LILIANA VERONICA SALCIDO RAMOS",
        "RAYMUNDO SOLIS GALLEGOS Vs JOSE RODRIGUEZ MENDOZA ",
        "RAYMUNDO SOLIS GALLEGOS Vs JORGE ANTONIO PIZARRO RIVAS ",
        "RAYMUNDO SOLIS GALLEGOS Vs JUAN PABLO HERNANDEZ AGUILERA ",
        "CELIA MORALES SIDA Vs ALFREDO ANTONIO MORALES AMEZAGA ",
        "FELIPE PALACIOS SARMIENTO Vs BIANCA VIOLETA VAZQUEZ TORRES ",
        "GUADALUPE TORRES URIBE Vs JUANA GALAVIZ DOMINGUEZ,ANA MARIA GONZALEZ CARRILLO ",
        "FLORENTINA BELEN MORALES ALMARAZ Vs MARISELA NEVAREZ NEVAREZ (EJECUTORIA) ",
        "JERONIMO ELIAS GALLARZO RENTERIA Vs ELVIRA ROMAN MARTINEZ,PATRICIA MARTINEZ,SAMUEL ORTEGA RIVERA,NORMA ARACELY CALDERON ORTEGA,MARIA SELENE CALDERON ORTEGA ",
        "JERONIMO ELIAS GALLARZO RENTERIA Vs MA NATIVIDAD MORALES HERNANDEZ,MARIA DEL CARMEN BLANCO MORALES,JUANA BUSTAMANTE SALAZAR,NATALISIA PERALES MONSIVAIS ",
        "FRANCISCA MERCADO Vs EUSEBIA GONZALEZ GOMEZ (EJECUTORIA) ",
        "ROCIO SETURINO TORRES Vs LAURA ADAME FERNANDEZ (S.D.) ",
        "DIRECCION DE PENSIONES DEL ESTADO DE DURANGO Vs JORGE ARMANDO MARTINEZ LOZANO ",
        "JERONIMO ELIAS GALLARZO RENTERIA Vs FRANCISCA GARCIA ROMERO,LETICIA CISNEROS RENTERIA,MA DEL CARMEN RAMIREZ JUAREZ,MARIA DEL ROCIO HIDALGO CANALES,GRISELDA MIJARES GALLEGOS (SENTENCIA INTERLOCUTORIA)",
        "JUAN ANTONIO RIVERA MONDACA Vs MARIA ELENA HERNANDEZ TORRES (SENTENCIA DEFINITIVA)",
        "JUANA ARTEMISA HERNANDEZ VALTIERRA DE GONZALEZ,AZALEA GUADALUPE HERNANDEZ VALTIERRA,SARA MARISA HERNANDEZ VALTIERRA,MARCO POLO HERNANDEZ VALTIERRA,MARTIN ANTONIO HERNANDEZ VALTIERRA,JOSE ANGEL HERNANDEZ VALTIERRA,ARTEMISA VALTIERRA GUTIERREZ DE HERNANDEZ Vs EDIFICADORA URBANA DE DURANGO, S.A. DE C.V.,DESARROLLO URBANO E INDUSTRIAL DE DURANGO, S.A. DE C.V.",
        "INSTITUTO DEL FONDO NACIONAL DE LA VIVIENDA PARA LOS TRABAJADORES Vs NICOLAS OLIVAS ARCINIEGA,MARIA MANUELA UNZUETA SOTO (***)",
        "MARIA DE LOS ANGELES MENDIOLA CONTRERAS Vs MARIA DOLORES FLORES BERMUDEZ (A U D I E N C I A)",
        "JUANA ARTEMISA HERNANDEZ VALTIERRA DE GONZALEZ Vs EDIFICADORA URBANA DE DURANGO, S.A. DE C.V.",
        "SANDRA GUADALUPE GUEVARA RODRIGUEZ Vs DIRECTOR GENERAL DEL REGISTRO CIVIL DE ESTA CIUDAD,OFICIAL NUMERO 26 DEL REGISTRO CIVIL DE ESTA CIUDAD (SUSPENCION)",
    ]
    patterns = [
        "(*)",      # G // also (*(*))
        "<-- Vs",   # E
        "Vs -->",   # F
    ]
    # TODO: 1 - G = "(*)" or "(*(*))" and remove from string
    #       2 - locate of "Vs"
    #           2.1 if there is not "Vs" than E = remaining string
    #       3 - E = string before "Vs"
    #       4 - F = string after "Vs"


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
