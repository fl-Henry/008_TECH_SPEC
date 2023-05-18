import sys
import random
import requests

from time import sleep, time
from datetime import datetime

# Custom imports
import general_methods as gm

from print_tags import Tags
from app import url_generator, parse_field_c, parse_field_e, parse_field_d, parse_field_b
from general_methods import random_dd_mm_yyy, replace_chars

tests_list = ["08"]


# 01
def tests_url_generator():
    # Tests url_generator
    if "01" in tests_list:
        values_for_url = {
            "capital": [
                "aux1.",
                "aux2.",
                "civ2.",
                "civ3.",
                "civ4.",
                "fam1.",
                "fam2.",
                "fam3.",
                "fam4.",
                "fam5.",
                "mer1.",
                "mer2.",
                "mer3.",
                "mer4.",
                "merOral.",
                "seccc.",
                "seccu.",
                "cjmf1.",
                "cjmf2.",
                "tribl."
            ],
            "lerdo": [
                "Civ1GP.",
                "Civ2GP.",
                "Fam1GP.",
                "Fam2GP.",
                "AuxMixtoGP.",
                "Fam3GP.",
                "secccGP.",
                "seccuGP.",
                "triblG.",
                "Mixto1Lerdo.",
                "Mixto2Lerdo."
            ],
            "foraneos": [
                "canatlan.",
                "nombrededios.",
                "nazas.",
                "cuencame.",
                "sanjuandelrio.",
                "elsalto.",
                "santamariadeloro.",
                "victoria.",
                "santiago."
            ]
        }
        start_time = datetime.utcnow()
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}\n")
        counter = 0
        test_amount = 20
        for _ in range(test_amount):
            dd, mm, yyyy = random_dd_mm_yyy((1, 1, 2017))
            # key_index = random.randint(0, 2)
            key_index = 0
            key = [*values_for_url.keys()][key_index]
            value_index = random.randint(0, len([*values_for_url.keys()][0]) - 1)
            value = values_for_url[key][value_index]
            value = "seccu."
            print("day:", dd, ", mm: ", mm, ", yyyy: ", yyyy, ", key: ", key, ", value: ", value)
            url = url_generator((dd, mm, yyyy), value)
            print(url)
            response_ = requests.get(url)
            if response_.text == "Not Found [CFN #0005]":
                print(response_.text)
            else:
                print("File Exists")
                counter += 1
            sleep(0.2)
            print()
        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("Working time of the test:", work_time)
        print(f"Test completed: {counter}/{test_amount} files exist")
        if "EAT" in tests_list:
            sys.exit(0)


# 02
def tests_replace_chars():
    if "02" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        string_for_checking = "Dictados el día jueves 27 de abril de 2023"
        result_string = "DICTADOS EL DIA JUEVES 27 DE ABRIL DE 2023"
        string_temp = string_for_checking
        print(f"string_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking)
        print(f"string_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking).upper()
        print(f"string_temp: {string_temp}")
        if result_string == string_temp:
            print("Match")
            counter += 1
        else:
            raise AssertionError

        string_for_checking = "áéíóöúüÁÉÍÓÖÚÜ"
        result_string = "AEIOOUUAEIOOUU"
        string_temp = string_for_checking
        print(f"\nstring_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking)
        print(f"string_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking).upper()
        print(f"string_temp: {string_temp}")
        if result_string == string_temp:
            print("Match")
            counter += 1
        else:
            raise AssertionError

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


# 03
def tests_parce_field_c():
    if "03" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        c_fields = [
            "1149/2017 0333/2010 00929/2011-II",
            "007CC/2016 1149/2017 0333/2010 ",
            "1149/2017 0333/2010 007CC/2016",
            "0333/2010 1149/2017 007CC/2016",
            "00724/2016 1149/2017",
            "00939/2015-I",
            "00929/2011-II",
            "1149/2017 0333/2010 00929/2011-II",
            "1149/2017 00929/2011-II 007CC/2016",
            "00929/2011-II 0333/2010 007CC/2016",
        ]
        for c_field in c_fields:
            print(c_field)
            res = parse_field_c(c_field)
            print(res)
            print()

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


# 04
def tests_parse_field_e():
    if "04" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

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
            "SISTEMAS DE BIENESTAR HECYMAR S. DE R.L DE C.V",
            "MARTIN OMAR CASTAÑEDA BAÑUELOS",
            "GUILERMO HIGAREDA Vs MARIA VERONICA GONZALEZ ORTIZ",
            "MARIA ESTHER MARTINEZ GONZALEZ",
            "ROBERTO HERNANDEZ SALAZAR A FAVOR DE: VIRGINIA HERNANDEZ DIAZ",
            "DOLORES VARELA RAMIREZ",
            "MARIA ELIZABETH QUINTERO AGUILAR",
            "YOLANDA HERRERA VAZQUEZ",
            "MARÍA ANTONIA HEIM SORIA - CAREN JANNETE RODRÍGUEZ CHACÓN (SE DELARA INCOMPTENTE LA SALA SE REMITE ALA COLEGIADA. ( PRIMERA SALA ))",
        ]

        for e_field in e_fields:
            print(e_field)
            print(parse_field_e(e_field))
            print()
            # break

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


# 05
def teste_parse_field_d():
    if "05" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        d_fields = [
            "TERCERO DE LO FAMILIAR 1er. DISTRITO JUDICIAL CONTROVERSIA DEL ORDEN FAMILIAR",
            "TERCERO DE LO FAMILIAR 1er.DISTRITO JUDICIAL CONTROVERSIA DEL ORDEN FAMILIAR",
            "MIXTO 8 ° DISTRITO JUDICIAL F. CONTROVERSIA DEL ORDEN FAMILIAR",
            "MIXTO 8 ° DISTRITO JUDICIALF. CONTROVERSIA DEL ORDEN FAMILIAR",
            "SEGUNDO DE LO CIVIL 1er. DISTRITO JUDICIAL ORDINARIO CIVIL",
            "MIXTO 13 ° DISTRITO JUDICIAL F. JUICIOS SUCESORIOS",
            "CUARTO DE LO FAMILIAR 1er. DISTRITO JUDICIAL JUICIOS SUCESORIOS",
            "CUARTO DE LO FAMILIAR 1er. DISTRITO JUDICIALJUICIOS SUCESORIOS",
            "SEGUNDO DE LO CIVIL 1er. DISTRITO JUDICIAL ORDINARIO CIVIL",
            "MIXTO 5 ° DISTRITO JUDICIAL C. DILIGENCIAS JURISDICCION VOLUNTARIA",
            "MIXTO 11 ° DISTRITO JUDICIAL C. ORDINARIO CIVIL",
            "QUINTO DE LO FAMILIAR 1er. DISTRITO JUDICIAL CONTROVERSIA DEL ORDEN FAMILIAR",
            "QUINTO DE LO FAMILIAR 1er. DISTRITO JUDICIAL CONTROVERSIA DEL ORDEN FAMILIAR",
            "CUARTO DE LO FAMILIAR 1er. DISTRITO JUDICIAL CONTROVERSIA DEL ORDEN FAMILIAR",
            "SEGUNDO DE LO CIVIL 1er. DISTRITO JUDICIAL ORDINARIO CIVIL",
            "SEGUNDO DE LO CIVIL 1er. DISTRITO JUDICIAL ORDINARIO CIVIL",
            "SEGUNDO DE LO FAMILIAR 1er. DISTRITO JUDICIAL AMPARO",
            "TERCERO DE LO CIVIL 1er. DISTRITO JUDICIAL AMPARO",
            "CUARTO DE LO CIVIL 1er. DISTRITO JUDICIAL AMPARO",
            "EJECUTIVO MERCANTIL",
            "ORDINARIO MERCANTIL",
            "EJECUTIVO MERCANTIL",
            "INCIDENTE PLANILLA DE LIQUIDACION DE SENTENCIA",
            "INCIDENTE PLANILLA DE GASTOS Y COSTAS",
            "INCIDENTE PLANILLA DE LIQUIDACION DE SENTENCIA",
            "SECRETO",
            "INCIDENTE NO ESPECIFICADO",
            "CONTROVERSIA DEL ORDEN FAMILIAR",
            "INCIDENTE LIQUIDACION DE LA SOCIEDAD CONYUGAL",
        ]

        for d_field in d_fields:
            print(d_field)
            print(parse_field_d(d_field))
            print()

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


# 06
def tests_remove_repeated_char():
    if "06" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        strings_spaces = [
            "text 2 space >  < here",
            "text 2 spaces>  <here",
            "text 2spaces>  <here",
            "text 3 spaces >   < here",
            "text 3 spaces>   <here",
            "text 4 spaces >    < here",
            "text 4 spaces>    < here",
            "text 4 spaces>    <here",
            "text 5 spaces >     < here",
            "text 5 spaces >     <here",
            "text 5 spaces>     <here",
            "text 5 spaces >     < here and text 4 spaces >    < here",
            "text 2 spaces >  < here and text 4 spaces >    < here",
            "text 4 spaces >    < here and text 2 spaces >  < here",

        ]

        strings_chars_b = [
            "text 2 chars 'b' >bb< here",
            "text 2 chars 'b'>bb<here",
            "text chars 'b'>bb<here",
            "text 3 chars 'b' >bbb< here",
            "text 3 chars 'b'>bbb<here",
            "text 4 chars 'b' >bbbb< here",
            "text 4 chars 'b'>bbbb< here",
            "text 4 chars 'b'>bbbb<here",
            "text 5 chars 'b' >bbbbb< here",
            "text 5 chars 'b' >bbbbb<here",
            "text 5 chars 'b'>bbbbb<here",
            "text 5 chars 'b' >bbbbb< here and text 4 chars 'b' >bbbb< here",
            "text 2 chars 'b' >bb< here and text 4 chars 'b' >bbb < here",
            "text 4 chars 'b' >bbbb< here and text 2 chars 'b' >bb< here",

        ]

        print(" ===== \/\/\/\/\/\/ ===== spaces ===== \/\/\/\/\/\/ ===== ")
        for string_ in strings_spaces:
            print(string_)
            print(gm.remove_repeated_char(string_, char=" "))
            print()
            # break

        print(" ===== \/\/\/\/\/\/ ===== chars 'b' ===== \/\/\/\/\/\/ ===== ")
        for string_ in strings_chars_b:
            print(string_)
            print(gm.remove_repeated_char(string_, char="b"))
            print()
            # break

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


# 07
def tests_find_number_indexes():
    if "07" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        str_nums = [
            "21516615_dsfge",
            "  516615_dsfge",
            "wefs16615_dsfge",
            "sd fsg 516615_dsfge",
            "215 615_dsfge",
        ]

        for str_num in str_nums:
            print(str_num)
            indexes = gm.find_number_indexes(str_num)
            print(indexes)
            print(str_num[indexes[0]:indexes[1]])
            print()

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


# 08
def tests_parse_field_b():
    if "08" in tests_list:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        sp_date_list = [
            "27 de septiembre de 2017"
            "Dictados el día miércoles 10 de febrero de 2021",
            "10 de febrero de 2018",
            " 10 de febrero de 2018 ",
            "Dictados el día miércoles 20 de enero de 2021",
            "20 de enero de 2018",
            " 20 de enero de 2018 ",
            "Dictados el día martes 9 de febrero de 2021",
            "9 de febrero de 2018",
            " 9 de febrero de 2018 ",
            "Dictados el día martes 23 de marzo de 2021",
            "23 de marzo de 2018",
            " 23 de marzo de 2018 ",
            "Dictados el día jueves 22 de abril de 2021",
            "22 de abril de 2018",
            " 22 de abril de 2018 ",
            "Dictados el día miércoles 12 de mayo de 2021",
            "12 de mayo de 2018",
            " 12 de mayo de 2018 ",
            "Dictados el día viernes 4 de junio de 2021",
            "4 de junio de 2018",
            " 4 de junio de 2018 ",
            "Dictados el día miércoles 14 de julio de 2021",
            "14 de julio de 2018",
            " 14 de julio de 2018 ",
            "Dictados el día miércoles 4 de agosto de 2021",
            "4 de agosto de 2018",
            " 4 de agosto de 2018 ",
            "Dictados el día martes 28 de septiembre de 2021",
            "28 de septiembre de 2018",
            " 28 de septiembre de 2018 ",
            "Dictados el día viernes 22 de octubre de 2021",
            "22 de octubre de 2018",
            " 22 de octubre de 2018 ",
            "Dictados el día miércoles 10 de noviembre de 2021",
            "10 de noviembre de 2018",
            " 10 de noviembre de 2018 ",
            "Dictados el día martes 14 de diciembre de 2021",
            "14 de diciembre de 2018",
            " 14 de diciembre de 2018 ",
        ]

        for sp_date in sp_date_list:
            print(sp_date)
            print(parse_field_b(sp_date))
            print()

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in tests_list:
            sys.exit(0)


if __name__ == '__main__':
    tests_url_generator()                   # 01
    tests_replace_chars()                   # 02
    tests_parce_field_c()                   # 03
    tests_parse_field_e()                   # 04
    teste_parse_field_d()                   # 05
    tests_remove_repeated_char()            # 06
    tests_find_number_indexes()             # 07
    tests_parse_field_b()                   # 08