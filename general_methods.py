import os
import sys
import random
import shutil
import argparse

from datetime import datetime, timedelta, date

# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


class DaNHandler:

    def __init__(self):
        base_path = str(__file__)[:len(__file__) - len(os.path.basename(str(__file__))) - 1]
        base_dir = f"{base_path}/"
        temp_dir = f"{base_dir}temp/"
        for_tests_dir = f"{base_dir}for_tests/"

        self.dirs = {
            "base_dir": base_dir,
            "temp_dir": temp_dir,
            "for_tests_dir": for_tests_dir,
            "capital": f"{temp_dir}capital/",
            "lerdo": f"{temp_dir}lerdo/",
            "foraneos": f"{temp_dir}foraneos/",
        }

        self.dirs_to_remove = {
            "temp_dir": temp_dir,
            "for_tests_dir": for_tests_dir,
        }

        self.files = {}
        self.create_dirs()

    def __str__(self):
        stdout = ""

        # Add dirs in stdout
        if len(self.dirs) > 0:
            stdout = f"\nDirs: "
            for key in self.dirs.keys():
                stdout += f"\n  {key:<16}: {self.dirs[key]}"

        # Add files in stdout
        if len(self.files) > 0:
            stdout += f"\nFiles: "
            for key in self.files.keys():
                stdout += f"\n  {key:<16}: {self.files[key]}"

        # Add dirs_to_delete in stdout
        if len(self.dirs_to_remove) > 0:
            stdout += f"\nDirs to delete: "
            for key in self.dirs_to_remove.keys():
                stdout += f"\n  {key:<16}: {self.dirs_to_remove[key]}"

        return stdout

    # Create all dirs
    def create_dirs(self):
        for key in self.dirs.keys():
            if not os.path.exists(self.dirs[key]):
                os.mkdir(self.dirs[key])

    # Delete all dirs
    def remove_dirs(self):
        for key in self.dirs_to_remove.keys():
            if os.path.exists(self.dirs_to_remove[key]):
                shutil.rmtree(self.dirs_to_remove[key], ignore_errors=True)


def arg_parser():
    # Parsing of arguments
    try:
        parser = argparse.ArgumentParser(description='TECH_SPEC')
        parser.add_argument('--tests', dest='tests_str', default=None,
                            help='Names of testes // separator "-"; Ex: "01-02-03"')
        parser.add_argument('--start-date', dest='start_date', default='1-1-2023',
                            help='Which date is scraping starts from // dd-mm-yyyy; Ex: "31-12-2022"')
        parser.add_argument('--end-date', dest='end_date', default=None,
                            help='Which date is scraping ends to // dd-mm-yyyy; Ex: "31-12-2022"')
        # parser.add_argument('--id', dest='id', default=5,
        #                     help='Id of callback Ex: 5')
        # parser.add_argument('--test', dest='test_key', nargs='?', const=True, default=False,
        #                     help='Enable test mode')
        # parser.add_argument('--force-url', dest='force_url', nargs='?', const=True, default=False,
        #                     help="Enable force url for Spot and Websocket (in the test mode has no effect")
        parsed_args = parser.parse_args()

        # Arguments
        args = {}
        args.update({"tests_list": str(parsed_args.tests_str).split("-")})
        args.update({"start_date": [int(x) for x in str(parsed_args.start_date).split("-")]})
        if parsed_args.end_date is None:
            parsed_args.end_date = datetime.today().strftime("%d-%m-%Y")
        args.update({"end_date": [int(x) for x in str(parsed_args.end_date).split("-")]})

        # Output of arguments
        stdout = "\nArguments: "
        if len(args) > 0:
            for key in args.keys():
                stdout += f"\n{key:<16}: {args[key]}"

        args.update({"stdout": stdout})

        return args

    except Exception as _ex:
        print("[ERROR] Parsing arguments >", _ex)
        sys.exit(1)


def delete_last_print_lines(n=1):
    # print("Entering to loop")
    # delete_last_print_lines()
    # print(f"{list_index}/{len(symbols_list)}")
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


# # ===== String Methods ========================================================================= String Methods =====
...
# # ===== String Methods ========================================================================= String Methods =====


def find_number_index(in_string):
    in_list = [str(x) for x in range(10)]
    for index in range(len(in_string)):
        if in_string[index] in in_list:
            return index


def find_char_index(in_string, char):
    for index in range(len(in_string)):
        if in_string[index] == char:
            return index
    return None


def find_string_indexes(in_string, string_to_find):
    for index in range(len(in_string) - len(string_to_find)):
        if in_string[index:index + len(string_to_find)] == string_to_find:
            return index, index + len(string_to_find)
    return None


def str_equals_str(str_1, str_2):
    if len(str_1) != len(str_2):
        print("len:", len(str_1), len(str_2))
        return False

    for char_1, char_2 in zip(str_1, str_2):
        if char_1 != char_2:
            print("char:", char_1, char_2)
            return False

    return True


def replace_chars(in_str):
    """"""

    # Latin Extended-A
    """
    Char 	Dec 	Hex 	Entity 	    Name
        Ā	256	    0100	&Amacr;	    LATIN CAPITAL LETTER A WITH MACRON
        ā	257	    0101	&amacr;	    LATIN SMALL LETTER A WITH MACRON
        Ă	258	    0102	&Abreve;    LATIN CAPITAL LETTER A WITH BREVE
        ă	259	    0103	&abreve;    LATIN SMALL LETTER A WITH BREVE
        Ą	260	    0104	&Aogon;	    LATIN CAPITAL LETTER A WITH OGONEK
        ą	261	    0105	&aogon;	    LATIN SMALL LETTER A WITH OGONEK
        Ć	262	    0106	&Cacute;    LATIN CAPITAL LETTER C WITH ACUTE
        ć	263	    0107	&cacute;    LATIN SMALL LETTER C WITH ACUTE
        Ĉ	264	    0108	&Ccirc;	    LATIN CAPITAL LETTER C WITH CIRCUMFLEX
        ĉ	265	    0109	&ccirc;	    LATIN SMALL LETTER C WITH CIRCUMFLEX
        Ċ	266	    010A	&Cdot;	    LATIN CAPITAL LETTER C WITH DOT ABOVE
        ċ	267	    010B	&cdot;	    LATIN SMALL LETTER C WITH DOT ABOVE
        Č	268	    010C	&Ccaron;    LATIN CAPITAL LETTER C WITH CARON
        č	269	    010D	&ccaron;    LATIN SMALL LETTER C WITH CARON
        Ď	270	    010E	&Dcaron;    LATIN CAPITAL LETTER D WITH CARON
        ď	271	    010F	&dcaron;    LATIN SMALL LETTER D WITH CARON
        Đ	272	    0110	&Dstrok;    LATIN CAPITAL LETTER D WITH STROKE
        đ	273	    0111	&dstrok;    LATIN SMALL LETTER D WITH STROKE
        Ē	274	    0112	&Emacr;	    LATIN CAPITAL LETTER E WITH MACRON
        ē	275	    0113	&emacr;	    LATIN SMALL LETTER E WITH MACRON
        Ĕ	276	    0114	 	        LATIN CAPITAL LETTER E WITH BREVE
        ĕ	277	    0115	 	        LATIN SMALL LETTER E WITH BREVE
        Ė	278	    0116	&Edot;	    LATIN CAPITAL LETTER E WITH DOT ABOVE
        ė	279	    0117	&edot;	    LATIN SMALL LETTER E WITH DOT ABOVE
        Ę	280	    0118	&Eogon;	    LATIN CAPITAL LETTER E WITH OGONEK
        ę	281	    0119	&eogon;	    LATIN SMALL LETTER E WITH OGONEK
        Ě	282	    011A	&Ecaron;	LATIN CAPITAL LETTER E WITH CARON
        ě	283	    011B	&ecaron;	LATIN SMALL LETTER E WITH CARON
        Ĝ	284	    011C	&Gcirc;	    LATIN CAPITAL LETTER G WITH CIRCUMFLEX
        ĝ	285	    011D	&gcirc;	    LATIN SMALL LETTER G WITH CIRCUMFLEX
        Ğ	286	    011E	&Gbreve;	LATIN CAPITAL LETTER G WITH BREVE
        ğ	287	    011F	&gbreve;	LATIN SMALL LETTER G WITH BREVE
        Ġ	288	    0120	&Gdot;	    LATIN CAPITAL LETTER G WITH DOT ABOVE
        ġ	289	    0121	&gdot;	    LATIN SMALL LETTER G WITH DOT ABOVE
        Ģ	290	    0122	&Gcedil;	LATIN CAPITAL LETTER G WITH CEDILLA
        ģ	291	    0123	&gcedil;	LATIN SMALL LETTER G WITH CEDILLA
        Ĥ	292	    0124	&Hcirc;	    LATIN CAPITAL LETTER H WITH CIRCUMFLEX
        ĥ	293	    0125	&hcirc;	    LATIN SMALL LETTER H WITH CIRCUMFLEX
        Ħ	294	    0126	&Hstrok;	LATIN CAPITAL LETTER H WITH STROKE
        ħ	295	    0127	&hstrok;	LATIN SMALL LETTER H WITH STROKE
        Ĩ	296	    0128	&Itilde;	LATIN CAPITAL LETTER I WITH TILDE
        ĩ	297	    0129	&itilde;	LATIN SMALL LETTER I WITH TILDE
        Ī	298	    012A	&Imacr;	    LATIN CAPITAL LETTER I WITH MACRON
        ī	299	    012B	&imacr;	    LATIN SMALL LETTER I WITH MACRON
        Ĭ	300	    012C	 	        LATIN CAPITAL LETTER I WITH BREVE
        ĭ	301	    012D	 	        LATIN SMALL LETTER I WITH BREVE
        Į	302	    012E	&Iogon;	    LATIN CAPITAL LETTER I WITH OGONEK
        į	303	    012F	&iogon;	    LATIN SMALL LETTER I WITH OGONEK
        İ	304	    0130	&Idot;	    LATIN CAPITAL LETTER I WITH DOT ABOVE
        ı	305	    0131	&inodot;	LATIN SMALL LETTER DOTLESS I
        Ĳ	306	    0132	&IJlog;	    LATIN CAPITAL LIGATURE IJ
        ĳ	307	    0133	&ijlig;	    LATIN SMALL LIGATURE IJ
        Ĵ	308	    0134	&Jcirc;	    LATIN CAPITAL LETTER J WITH CIRCUMFLEX
        ĵ	309	    0135	&jcirc;	    LATIN SMALL LETTER J WITH CIRCUMFLEX
        Ķ	310	    0136	&Kcedil;	LATIN CAPITAL LETTER K WITH CEDILLA
        ķ	311	    0137	&kcedli;	LATIN SMALL LETTER K WITH CEDILLA
        ĸ	312	    0138	&kgreen;	LATIN SMALL LETTER KRA
        Ĺ	313	    0139	&Lacute;	LATIN CAPITAL LETTER L WITH ACUTE
        ĺ	314	    013A	&lacute;	LATIN SMALL LETTER L WITH ACUTE
        Ļ	315	    013B	&Lcedil;	LATIN CAPITAL LETTER L WITH CEDILLA
        ļ	316	    013C	&lcedil;	LATIN SMALL LETTER L WITH CEDILLA
        Ľ	317	    013D	&Lcaron;	LATIN CAPITAL LETTER L WITH CARON
        ľ	318	    013E	&lcaron;	LATIN SMALL LETTER L WITH CARON
        Ŀ	319	    013F	&Lmodot;	LATIN CAPITAL LETTER L WITH MIDDLE DOT
        ŀ	320	    0140	&lmidot;	LATIN SMALL LETTER L WITH MIDDLE DOT
        Ł	321	    0141	&Lstrok;	LATIN CAPITAL LETTER L WITH STROKE
        ł	322	    0142	&lstrok;	LATIN SMALL LETTER L WITH STROKE
        Ń	323	    0143	&Nacute;	LATIN CAPITAL LETTER N WITH ACUTE
        ń	324	    0144	&nacute;	LATIN SMALL LETTER N WITH ACUTE
        Ņ	325	    0145	&Ncedil;	LATIN CAPITAL LETTER N WITH CEDILLA
        ņ	326	    0146	&ncedil;	LATIN SMALL LETTER N WITH CEDILLA
        Ň	327	    0147	&Ncaron;	LATIN CAPITAL LETTER N WITH CARON
        ň	328	    0148	&ncaron;	LATIN SMALL LETTER N WITH CARON
        ŉ	329	    0149	&napos;	    LATIN SMALL LETTER N PRECEDED BY APOSTROPHE
        Ŋ	330	    014A	&ENG;	    LATIN CAPITAL LETTER ENG
        ŋ	331	    014B	&eng;	    LATIN SMALL LETTER ENG
        Ō	332	    014C	&Omacr;	    LATIN CAPITAL LETTER O WITH MACRON
        ō	333	    014D	&omacr;	    LATIN SMALL LETTER O WITH MACRON
        Ŏ	334	    014E	 	        LATIN CAPITAL LETTER O WITH BREVE
        ŏ	335	    014F	 	        LATIN SMALL LETTER O WITH BREVE
        Ő	336	    0150	&Odblac;	LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
        ő	337	    0151	&odblac;	LATIN SMALL LETTER O WITH DOUBLE ACUTE
        Œ	338	    0152	&OElig;	    LATIN CAPITAL LIGATURE OE
        œ	339	    0153	&oelig;	    LATIN SMALL LIGATURE OE
        Ŕ	340	    0154	&Racute;	LATIN CAPITAL LETTER R WITH ACUTE
        ŕ	341	    0155	&racute;	LATIN SMALL LETTER R WITH ACUTE
        Ŗ	342	    0156	&Rcedil;	LATIN CAPITAL LETTER R WITH CEDILLA
        ŗ	343	    0157	&rcedil;	LATIN SMALL LETTER R WITH CEDILLA
        Ř	344	    0158	&Rcaron;	LATIN CAPITAL LETTER R WITH CARON
        ř	345	    0159	&rcaron;	LATIN SMALL LETTER R WITH CARON
        Ś	346	    015A	&Sacute;	LATIN CAPITAL LETTER S WITH ACUTE
        ś	347	    015B	&sacute;	LATIN SMALL LETTER S WITH ACUTE
        Ŝ	348	    015C	&Scirc;	    LATIN CAPITAL LETTER S WITH CIRCUMFLEX
        ŝ	349	    015D	&scirc;	    LATIN SMALL LETTER S WITH CIRCUMFLEX
        Ş	350	    015E	&Scedil;	LATIN CAPITAL LETTER S WITH CEDILLA
        ş	351	    015F	&scedil;	LATIN SMALL LETTER S WITH CEDILLA
        Š	352	    0160	&Scaron;	LATIN CAPITAL LETTER S WITH CARON
        š	353	    0161	&scaron;	LATIN SMALL LETTER S WITH CARON
        Ţ	354	    0162	&Tcedil;	LATIN CAPITAL LETTER T WITH CEDILLA
        ţ	355	    0163	&tcedil;	LATIN SMALL LETTER T WITH CEDILLA
        Ť	356	    0164	&Tcaron;	LATIN CAPITAL LETTER T WITH CARON
        ť	357	    0165	&tcaron;	LATIN SMALL LETTER T WITH CARON
        Ŧ	358	    0166	&Tstrok;	LATIN CAPITAL LETTER T WITH STROKE
        ŧ	359	    0167	&tstrok;	LATIN SMALL LETTER T WITH STROKE
        Ũ	360	    0168	&Utilde;	LATIN CAPITAL LETTER U WITH TILDE
        ũ	361	    0169	&utilde;	LATIN SMALL LETTER U WITH TILDE
        Ū	362	    016A	&Umacr;	    LATIN CAPITAL LETTER U WITH MACRON
        ū	363	    016B	&umacr;	    LATIN SMALL LETTER U WITH MACRON
        Ŭ	364	    016C	&Ubreve;	LATIN CAPITAL LETTER U WITH BREVE
        ŭ	365	    016D	&ubreve;	LATIN SMALL LETTER U WITH BREVE
        Ů	366	    016E	&Uring;	    LATIN CAPITAL LETTER U WITH RING ABOVE
        ů	367	    016F	&uring;	    LATIN SMALL LETTER U WITH RING ABOVE
        Ű	368	    0170	&Udblac;	LATIN CAPITAL LETTER U WITH DOUBLE ACUTE
        ű	369	    0171	&udblac;	LATIN SMALL LETTER U WITH DOUBLE ACUTE
        Ų	370	    0172	&Uogon;	    LATIN CAPITAL LETTER U WITH OGONEK
        ų	371	    0173	&uogon;	    LATIN SMALL LETTER U WITH OGONEK
        Ŵ	372	    0174	&Wcirc;	    LATIN CAPITAL LETTER W WITH CIRCUMFLEX
        ŵ	373	    0175	&wcirc;	    LATIN SMALL LETTER W WITH CIRCUMFLEX
        Ŷ	374	    0176	&Ycirc;	    LATIN CAPITAL LETTER Y WITH CIRCUMFLEX
        ŷ	375	    0177	&ycirc;	    LATIN SMALL LETTER Y WITH CIRCUMFLEX
        Ÿ	376	    0178	&Yuml;	    LATIN CAPITAL LETTER Y WITH DIAERESIS
        Ź	377	    0179	&Zacute;	LATIN CAPITAL LETTER Z WITH ACUTE
        ź	378	    017A	&zacute;	LATIN SMALL LETTER Z WITH ACUTE
        Ż	379	    017B	&Zdot;	    LATIN CAPITAL LETTER Z WITH DOT ABOVE
        ż	380	    017C	&zdot;	    LATIN SMALL LETTER Z WITH DOT ABOVE
        Ž	381	    017D	&Zcaron;	LATIN CAPITAL LETTER Z WITH CARON
        ž	382	    017E	&zcaron;	LATIN SMALL LETTER Z WITH CARON
        ſ	383	    017F	 	        LATIN SMALL LETTER LONG S  
    """

    # C1 Controls and Latin-1 Supplement
    """
    Char 	Dec 	Hex 	Entity 	    Name
         	160	    00A0	&nbsp;	    NO-BREAK SPACE
        ¡	161	    00A1	&iexcl;	    INVERTED EXCLAMATION MARK
        ¢	162	    00A2	&cent;	    CENT SIGN
        £	163	    00A3	&pound;	    POUND SIGN
        ¤	164	    00A4	&curren;    CURRENCY SIGN
        ¥	165	    00A5	&yen;	    YEN SIGN
        ¦	166	    00A6	&brvbar;    BROKEN BAR
        §	167	    00A7	&sect;	    SECTION SIGN
        ¨	168	    00A8	&uml;	    DIAERESIS
        ©	169	    00A9	&copy;	    COPYRIGHT SIGN
        ª	170	    00AA	&ordf;	    FEMININE ORDINAL INDICATOR
        «	171	    00AB	&laquo;	    LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        ¬	172	    00AC	&not;	    NOT SIGN
        ­	173	    00AD	&shy;	    SOFT HYPHEN
        ®	174	    00AE	&reg;	    REGISTERED SIGN
        ¯	175	    00AF	&macr;	    MACRON
        °	176	    00B0	&deg;	    DEGREE SIGN
        ±	177	    00B1	&plusmn;    PLUS-MINUS SIGN
        ²	178	    00B2	&sup2;	    SUPERSCRIPT TWO
        ³	179	    00B3	&sup3;	    SUPERSCRIPT THREE
        ´	180	    00B4	&acute;	    ACUTE ACCENT
        µ	181	    00B5	&micro;	    MICRO SIGN
        ¶	182	    00B6	&para;	    PILCROW SIGN
        ·	183	    00B7	&middot;    MIDDLE DOT
        ¸	184	    00B8	&cedil;	    CEDILLA
        ¹	185	    00B9	&sup1;	    SUPERSCRIPT ONE
        º	186	    00BA	&ordm;	    MASCULINE ORDINAL INDICATOR
        »	187	    00BB	&raquo;	    RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        ¼	188	    00BC	&frac14;    VULGAR FRACTION ONE QUARTER
        ½	189	    00BD	&frac12;    VULGAR FRACTION ONE HALF
        ¾	190	    00BE	&frac34;    VULGAR FRACTION THREE QUARTERS
        ¿	191	    00BF	&iquest;    INVERTED QUESTION MARK
        À	192	    00C0	&Agrave;    LATIN CAPITAL LETTER A WITH GRAVE
        Á	193	    00C1	&Aacute;    LATIN CAPITAL LETTER A WITH ACUTE
        Â	194	    00C2	&Acirc;	    LATIN CAPITAL LETTER A WITH CIRCUMFLEX
        Ã	195	    00C3	&Atilde;    LATIN CAPITAL LETTER A WITH TILDE
        Ä	196	    00C4	&Auml;	    LATIN CAPITAL LETTER A WITH DIAERESIS
        Å	197	    00C5	&Aring;	    LATIN CAPITAL LETTER A WITH RING ABOVE
        Æ	198	    00C6	&AElig;	    LATIN CAPITAL LETTER AE
        Ç	199	    00C7	&Ccedil;    LATIN CAPITAL LETTER C WITH CEDILLA
        È	200	    00C8	&Egrave;    LATIN CAPITAL LETTER E WITH GRAVE
        É	201	    00C9	&Eacute;    LATIN CAPITAL LETTER E WITH ACUTE
        Ê	202	    00CA	&Ecirc;	    LATIN CAPITAL LETTER E WITH CIRCUMFLEX
        Ë	203	    00CB	&Euml;	    LATIN CAPITAL LETTER E WITH DIAERESIS
        Ì	204	    00CC	&Igrave;    LATIN CAPITAL LETTER I WITH GRAVE
        Í	205	    00CD	&Iacute;    LATIN CAPITAL LETTER I WITH ACUTE
        Î	206	    00CE	&Icirc;	    LATIN CAPITAL LETTER I WITH CIRCUMFLEX
        Ï	207	    00CF	&Iuml;	    LATIN CAPITAL LETTER I WITH DIAERESIS
        Ð	208	    00D0	&ETH;	    LATIN CAPITAL LETTER ETH
        Ñ	209	    00D1	&Ntilde;    LATIN CAPITAL LETTER N WITH TILDE
        Ò	210	    00D2	&Ograve;    LATIN CAPITAL LETTER O WITH GRAVE
        Ó	211	    00D3	&Oacute;    LATIN CAPITAL LETTER O WITH ACUTE
        Ô	212	    00D4	&Ocirc;	    LATIN CAPITAL LETTER O WITH CIRCUMFLEX
        Õ	213	    00D5	&Otilde;    LATIN CAPITAL LETTER O WITH TILDE
        Ö	214	    00D6	&Ouml;	    LATIN CAPITAL LETTER O WITH DIAERESIS
        ×	215	    00D7	&times;	    MULTIPLICATION SIGN
        Ø	216	    00D8	&Oslash;    LATIN CAPITAL LETTER O WITH STROKE
        Ù	217	    00D9	&Ugrave;    LATIN CAPITAL LETTER U WITH GRAVE
        Ú	218	    00DA	&Uacute;    LATIN CAPITAL LETTER U WITH ACUTE
        Û	219	    00DB	&Ucirc;	    LATIN CAPITAL LETTER U WITH CIRCUMFLEX
        Ü	220	    00DC	&Uuml;	    LATIN CAPITAL LETTER U WITH DIAERESIS
        Ý	221	    00DD	&Yacute;    LATIN CAPITAL LETTER Y WITH ACUTE
        Þ	222	    00DE	&THORN;	    LATIN CAPITAL LETTER THORN
        ß	223	    00DF	&szlig;	    LATIN SMALL LETTER SHARP S
        à	224	    00E0	&agrave;    LATIN SMALL LETTER A WITH GRAVE
        á	225	    00E1	&aacute;    LATIN SMALL LETTER A WITH ACUTE
        â	226	    00E2	&acirc;	    LATIN SMALL LETTER A WITH CIRCUMFLEX
        ã	227	    00E3	&atilde;    LATIN SMALL LETTER A WITH TILDE
        ä	228	    00E4	&auml;	    LATIN SMALL LETTER A WITH DIAERESIS
        å	229	    00E5	&aring;	    LATIN SMALL LETTER A WITH RING ABOVE
        æ	230	    00E6	&aelig;	    LATIN SMALL LETTER AE
        ç	231	    00E7	&ccedil;    LATIN SMALL LETTER C WITH CEDILLA
        è	232	    00E8	&egrave;    LATIN SMALL LETTER E WITH GRAVE
        é	233	    00E9	&eacute;    LATIN SMALL LETTER E WITH ACUTE
        ê	234	    00EA	&ecirc;	    LATIN SMALL LETTER E WITH CIRCUMFLEX
        ë	235	    00EB	&euml;	    LATIN SMALL LETTER E WITH DIAERESIS
        ì	236	    00EC	&igrave;    LATIN SMALL LETTER I WITH GRAVE
        í	237	    00ED	&iacute;    LATIN SMALL LETTER I WITH ACUTE
        î	238	    00EE	&icirc;	    LATIN SMALL LETTER I WITH CIRCUMFLEX
        ï	239	    00EF	&iuml;	    LATIN SMALL LETTER I WITH DIAERESIS
        ð	240	    00F0	&eth;	    LATIN SMALL LETTER ETH
        ñ	241	    00F1	&ntilde;    LATIN SMALL LETTER N WITH TILDE
        ò	242	    00F2	&ograve;    LATIN SMALL LETTER O WITH GRAVE
        ó	243	    00F3	&oacute;    LATIN SMALL LETTER O WITH ACUTE
        ô	244	    00F4	&ocirc;	    LATIN SMALL LETTER O WITH CIRCUMFLEX
        õ	245	    00F5	&otilde;    LATIN SMALL LETTER O WITH TILDE
        ö	246	    00F6	&ouml;	    LATIN SMALL LETTER O WITH DIAERESIS
        ÷	247	    00F7	&divide;    DIVISION SIGN
        ø	248	    00F8	&oslash;    LATIN SMALL LETTER O WITH STROKE
        ù	249	    00F9	&ugrave;    LATIN SMALL LETTER U WITH GRAVE
        ú	250	    00FA	&uacute;    LATIN SMALL LETTER U WITH ACUTE
        û	251	    00FB	&ucirc;	    LATIN SMALL LETTER U WITH CIRCUMFLEX
        ü	252	    00FC	&uuml;	    LATIN SMALL LETTER U WITH DIAERESIS
        ý	253	    00FD	&yacute;    LATIN SMALL LETTER Y WITH ACUTE
        þ	254	    00FE	&thorn;	    LATIN SMALL LETTER THORN
        ÿ	255	    00FF	&yuml;	    LATIN SMALL LETTER Y WITH DIAERESIS
    """

    # Char set for replace
    char_set = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ö": "o",
        "ú": "u",
        "ü": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ö": "O",
        "Ú": "U",
        "Ü": "U",
    }

    out_str = ''
    for char in in_str:
        if char in [*char_set.keys()]:
            char = char_set[char]
        out_str += char

    char_set = {
        "&#192;": "A",
        "&#193;": "A",
        "&#194;": "A",
        "&#195;": "A",
        "&#196;": "A",
        "&#197;": "A",
        "&#198;": "AE",
        "&#199;": "C",
        "&#200;": "E",
        "&#201;": "E",
        "&#202;": "E",
        "&#203;": "E",
        "&#204;": "I",
        "&#205;": "I",
        "&#206;": "I",
        "&#207;": "I",
        "&#208;": "D",
        "&#209;": "N",
        "&#210;": "O",
        "&#211;": "O",
        "&#212;": "O",
        "&#213;": "O",
        "&#214;": "O",
        "&#216;": "O",
        "&#217;": "U",
        "&#218;": "U",
        "&#219;": "U",
        "&#220;": "U",
        "&#221;": "Y",
        "&#222;": "B",
        "&#223;": "b",
        "&#224;": "a",
        "&#225;": "a",
        "&#226;": "a",
        "&#227;": "a",
        "&#228;": "a",
        "&#229;": "a",
        "&#230;": "ae",
        "&#231;": "c",
        "&#232;": "e",
        "&#233;": "e",
        "&#234;": "e",
        "&#235;": "e",
        "&#236;": "i",
        "&#237;": "i",
        "&#238;": "i",
        "&#239;": "i",
        "&#240;": "o",
        "&#241;": "n",
        "&#242;": "o",
        "&#243;": "o",
        "&#244;": "o",
        "&#245;": "o",
        "&#246;": "o",
        "&#248;": "o",
        "&#249;": "u",
        "&#250;": "u",
        "&#251;": "u",
        "&#252;": "u",
        "&#253;": "y",
        "&#254;": "b",
        "&#255;": "y",
    }
    result_str = ""
    last_char = 0
    for char_counter in range(len(out_str) - 6):
        if out_str[char_counter:char_counter + 6] in [*char_set.keys()]:
            result_str += out_str[last_char:char_counter] + char_set[out_str[char_counter:char_counter + 6]]
            last_char = char_counter + 6
    result_str += out_str[last_char:]

    return result_str


def url_to_name(file_url, iter_count=1):
    input_file_url = file_url
    file_name = file_url
    process_url = file_url
    error_counter = 0
    while iter_count > 0:

        # Checking infinite loop
        error_counter += 1
        if error_counter > 8000:
            print("[ERROR] url_to_name > infinite loop")
            print(input_file_url)
            raise LookupError

        # Method logic
        if process_url[-1] == '/':
            process_url = process_url[:-1]
        for _ in range(1, len(process_url)):
            char = process_url[-1]
            if char == '/':
                file_name = file_url[len(process_url):]
                file_url = process_url[:-1]
                iter_count -= 1
                break
            else:
                process_url = process_url[:-1]
    return file_name


def url_parent(file_url, iter_count=1):
    input_file_url = file_url
    parent_url = file_url
    process_url = file_url
    error_counter = 0
    while iter_count > 0:

        # Checking infinite loop
        error_counter += 1
        if error_counter > 8000:
            print("[ERROR] url_parent > infinite loop")
            print(input_file_url)
            raise LookupError

        # Method logic
        if process_url[-1] == '/':
            process_url = process_url[:-1]
        for _ in range(1, len(process_url)):
            char = process_url[-1]
            if char == '/':
                parent_url = process_url
                iter_count -= 1
                break
            else:
                process_url = process_url[:-1]

    return parent_url


# # ===== Date Methods ============================================================================= Date Methods =====
...
# # ===== Date Methods ============================================================================= Date Methods =====


def dates_between(start_date, end_date):
    """
    :param start_date: tuple[int, int, int]     | (31, 12, 2023)
    :param end_date: tuple[int, int, int]       | (31, 12, 2023)
    :return: list[tuple[int, int, int]]
    """
    start_date = date(start_date[2], start_date[1], start_date[0])
    end_date = date(end_date[2], end_date[1], end_date[0])

    delta = end_date - start_date

    dates_between_list = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates_between_list.append([int(x) for x in str(day.strftime("%d-%m-%Y")).split("-")])

    return dates_between_list


def random_dd_mm_yyy(start_date, end_date: tuple[int, int, int] = None):
    if end_date is None:
        end_date = datetime.today()
    else:
        if len(end_date) == 3:
            end_date = datetime(year=end_date[2], month=end_date[1], day=end_date[0])
        else:
            raise ValueError
    start_date = datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    dd = int(str(random_date.strftime("%d")))
    mm = int(str(random_date.strftime("%m")))
    yyyy = int(str(random_date.strftime("%Y")))
    return dd, mm, yyyy
