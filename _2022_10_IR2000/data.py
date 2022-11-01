"""Регионы, загружаемые в БД"""
region = {
    '01': 'Adygeja_Resp',
    '04': 'Altaj_Resp',
    '22': 'Altajskij_kraj',
    '28': 'Amurskaja_obl',
    '29': 'Arkhangelskaja_obl',
    '30': 'Astrakhanskaja_obl',
    '94': 'Bajkonur_g',
    '02': 'Bashkortostan_Resp',
    '31': 'Belgorodskaja_obl',
    '32': 'Brjanskaja_obl',
    '03': 'Burjatija_Resp',
    '20': 'Chechenskaja_Resp',
    '74': 'Cheljabinskaja_obl',
    '87': 'Chukotskij_AO',
    '21': 'Chuvashskaja_Resp',
    '05': 'Dagestan_Resp',
    '79': 'Evrejskaja_Aobl',
    '06': 'Ingushetija_Resp',
    '38': 'Irkutskaja_obl',
    '37': 'Ivanovskaja_obl',
    '89': 'Jamalo-Neneckij_AO',
    '76': 'Jaroslavskaja_obl',
    '07': 'Kabardino-Balkarskaja_Resp',
    '39': 'Kaliningradskaja_obl',
    '08': 'Kalmykija_Resp',
    '40': 'Kaluzhskaja_obl',
    '41': 'Kamchatskij_kraj',
    '82': 'Kamchatskij_kraj',
    '09': 'Karachaevo-Cherkesskaja_Resp',
    '10': 'Karelija_Resp',
    '42': 'Kemerovskaja_obl',
    '27': 'Khabarovskij_kraj',
    '19': 'Khakasija_Resp',
    '86': 'Khanty-Mansijskij_AO-Jugra_AO',
    '43': 'Kirovskaja_obl',
    '11': 'Komi_Resp',
    '44': 'Kostromskaja_obl',
    '23': 'Krasnodarskij_kraj',
    '24': 'Krasnojarskij_kraj',
    '91': 'Krim_Resp',
    '45': 'Kurganskaja_obl',
    '46': 'Kurskaja_obl',
    '47': 'Leningradskaja_obl',
    '48': 'Lipeckaja_obl',
    '49': 'Magadanskaja_obl',
    '12': 'Marij_El_Resp',
    '13': 'Mordovija_Resp',
    '50': 'Moskovskaja_obl',
    '77': 'Moskva',
    '51': 'Murmanskaja_obl',
    '83': 'Neneckij_AO',
    '52': 'Nizhegorodskaja_obl',
    '53': 'Novgorodskaja_obl',
    '54': 'Novosibirskaja_obl',
    '55': 'Omskaja_obl',
    '56': 'Orenburgskaja_obl',
    '57': 'Orlovskaja_obl',
    '58': 'Penzenskaja_obl',
    '59': 'Permskij_kraj',
    '25': 'Primorskij_kraj',
    '60': 'Pskovskaja_obl',
    '62': 'Rjazanskaja_obl',
    '61': 'Rostovskaja_obl',
    '14': 'Sakha_Jakutija_Resp',
    '65': 'Sakhalinskaja_obl',
    '63': 'Samarskaja_obl',
    '78': 'Sankt-Peterburg',
    '64': 'Saratovskaja_obl',
    '92': 'Sevastopol_g',
    '15': 'Severnaja_Osetija-Alanija_Resp',
    '67': 'Smolenskaja_obl',
    '26': 'Stavropolskij_kraj',
    '66': 'Sverdlovskaja_obl',
    '68': 'Tambovskaja_obl',
    '16': 'Tatarstan_Resp',
    '72': 'Tjumenskaja_obl',
    '70': 'Tomskaja_obl',
    '71': 'Tulskaja_obl',
    '69': 'Tverskaja_obl',
    '17': 'Tyva_Resp',
    '18': 'Udmurtskaja_Resp',
    '73': 'Uljanovskaja_obl',
    '33': 'Vladimirskaja_obl',
    '34': 'Volgogradskaja_obl',
    '35': 'Vologodskaja_obl',
    '36': 'Voronezhskaja_obl',
    '75': 'Zabajkalskij_kraj'
}
sz_fo = {'78', '47', '53', '60', '10', '29', '11', '35', '51', '83', '39'}                      # Северо-западный ФО
c_fo = {'77', '32', '33', '37', '40', '44', '50', '57', '62', '67', '69', '71', '76', '31', '36', '46', '48',
              '68'}                                                                             # Центральный ФО
p_fo = {'52', '43', '12', '13', '21', '58', '73', '64', '63', '56', '02', '16', '18', '59'}     # Приволжский ФО
u_fo = {'08', '34', '30', '01', '61', '23'}                                                     # Южный ФО
sk_fo = {'26', '15', '09', '07', '20', '06', '05'}                                              # Северо-Кавказский ФО
y_fo = {'66', '74', '45', '72', '89', '86'}                                                     # Уральский ФО
s_fo = {'04', '22', '54', '70', '42', '55', '19', '17', '24', '38', '03', '75'}                 # Сибирский ФО
d_fo = {'14', '79', '87', '25', '27', '28', '41', '49', '65'}                                   # Дальневосточный ФО
k_fo = {'94', '91', '92'}                                                                       # Крымский ФО
all_regions = sz_fo | c_fo | p_fo | u_fo | sk_fo | y_fo | s_fo | d_fo | k_fo


def regions(code):
    """Имена регионов, соответственно его коду
    :param code: Код региона
    :return: Возвращает имя региона или 0, если регион не найден"""
    return region.get(code, 0)
