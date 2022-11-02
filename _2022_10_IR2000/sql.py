import mysql.connector as mysql
from mysql.connector import Error
import re

fieldsLinks = {
    'id'													: 'id','publishDate'												: 'publishDate','customerregNum'											: 'customerregNum','customerconsRegistryNum'									: 'customerconsRegistryNum',
    'customerfullName'											: 'customerfullName','customershortName'											: 'customershortName',
    'customerregistrationDate'									: 'customerDate',
    'customerinn'												:'customerinn',
    'customerkpp'												:'customerkpp',
    'customerlegalFormcode'										: 'cusalFormcode',
    'customerlegalFormsingularName'								:'customerlegalFormsingularName',
    'cu'												: 'customerOKPO',
    'curCode'										: 'custode',
    'regNum'													: 'regNum',
    'number'													: 'number','contractSubject'											:'contractSubject',
    'href'														: 'href',
    'printFormurl'												: 'printFormurl',
    'printFormdocRegNumber'										: 'printFoumber',
    'productsproductsid'										: 'productsid','productsproductOKPD2code'									: 'produce',
    'productsproductOKPD2name'									: 'pPD2name',
    'productsproductname'										: 'productsname',
    'productsproductOKEIcode'									: 'productsOKEIcode',
    'productOKEInationalCode'							: 'productsOKEInationalCode',
    'productsproductOKEIfullName'								: 'produclName',
    'productsproductprice'										: 'productsprice',
    'productsproductpriceRUR'									: 'productspriceRUR','productsproductwhitoutVATPrice'							: 'produVATPrice',
    'productsproductquantity'									:'productsquantity',
    'productsproductsum'										:'productssum',
    'productsproductsumRUR'										:'productssumRUR',
    'productsproductwithoutVATSum'								: 'productswithoutVATSum',
    'productsproductVATRate'									: 'productsVATRate',
    'productsproductVATSum'										: 'productsVATSum',
    'prosproductoriginCountrycountryCode'					: 'productsoriginCountrycountryCode','productsproductoriginCountrycountryFullName'				:'productsoriginCountrycountryFullName',
    'productsTRUcode'									: 'productsKTRUcode',
    'productsproductKTRUname'									: 'productsKTRUname',
    'productsproductKTRUOKPD2code'								: 'productsKTRUOKPD2code',
    'productsproductKTRUOKPD2name'								: 'productsKTRUOKPD2name',
    'productsproductMNInfoMNNName'								: 'productsMNNInfoMNNName',
    'productsproduurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfoMNNName'	: 'productsMNNInfoMNNName',
    'productsproductdosageUserOKEIcode'							: 'roductsdosageUserOKEIcode',
    'productsproductdrugPurchaseObjectInfodUsingReferenceInfoMNNsInfoMNNInfodosageUserdosageUserOKEIcode'	: 'productsdosageUserOKEIcode',
    'productsproductdosageUserOKEIname'							: 'roductsdosageUserOKEIname',
    'productsproductdrugPurchaseObjectInfodrugInfgReferenceInfoMNNsInfoMNNInfodosageUserdosageUserOKEIname'	: 'productsdosageUserOKEIname',
    'productsproductdosageUserdosageUserName'					: 'prductsdosageUserdosageUserName',
    'productsproductdrugPurchaseObjectInfodruingReferenceInfoMNNsInfoMNNInfodosageUserdosageUserName'	: 'productsdosageUserdosageUserName',
    'productsproducttradeInfotradeName'							: 'productstradeInfotradeNam',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfoptionsTradeNamepositionTradeNametradeInfotradeName'	: 'productstradeInfotradeName',
    'productsproductpositionTradeNamecertificateNumber'			: 'productspositionTradeNamecertificateNumbr',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNameposiionTradeNamecertificateNumber'	: 'productspositionTradeNamecertificateNumber',
    'productsproductmedicamentalFormInfomedicamentalFormName'	: 'productsmedicamentalFormInfomedicamentalFormName',
    'productsprodutdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNamepositionTradeNamemedtalFormInfomedicamentalFormName'	: 'productsproductmedicamentalFormInfomedicamentalFormName',
    'productsproductdosageInfodosageName'						: 'productsdosageInfodosageName',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNInfopositionsTradeNamepositionTradeNamedosageInfodosageName'	: 'productsdosageInfodosageName',
    'productsproductdosageOKEIcode'								: 'productsdosageOKEIcode',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInnfopositionsTradeNamepositionTradeNamedosageInfodosageOKEIcode'	: 'productsdosageOKEIcode',
    'productsproductdosageOKEInationalCode'						: 'productsdosageOKEInationalCode',
    'produtsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfnsTradeNamepositionTradeNamedosageInfodosageOKEInationalCode'	: 'produageOKEInationalCode',
    'productsproductdosageOKEIname'								: 'productsdosageOKEIname',
    'productsproductdosageInfodosageValue'						: 'productsdosageInfodosageValue',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNIsitionsTradeNamepositionTradeNamedosageInfodosageValue'	: 'productsdosageInfodosageValue',
    'productsproductdosageInfodosageUserName'					: 'productsdosageInfodosageUserName',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNamositionTradeNamedosageInfodosageUserName'	: 'productsdosageInfodosageUserName',
    'productsproductpositionTradeNamecertificateKeeperName'		: 'productspositionTradeNamecertificateKeeperName',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNamitionTradeNamecertificateKeeperName'	: 'productspositionTradeNamecertificateKeeperName',
    'productsproductmanufacturerOKSMcountryCode'				: 'productsmanufacturerOKSMcountryCode',
    'productsproductdugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNamepositionTradeNmanufacturerInfomanufacturerOKSMcountryCode'	: 'productsmanufacturerOKSMcountryCode',
    'productsproductmanufacturerOKSMcountryFullName'			: 'productsmanufacturerOKSMcountryFullName',
    'productsproductdrugPrchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNamepositionTradeNamemanufarerInfomanufacturerOKSMcountryFullName'	: 'productsmanufacturerOKSMcountryFullName',
    'productsproductmanufacturerInfomanufacturerName'			: 'productsmanufacturerInfomanufacturerName',
    'produtsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoMNNsInfoMNNInfopositionsTradeNamepositradeNamemanufacturerInfomanufacturerName'	: 'productsmanufacturerInfomanufacturerName',
    'puctsproductpositionTradeNameMNNNormName'				: 'productspositionTradeNameMNNNormName',
    'prosproductpositionTradeNamedosageNormName'			: 'productspositionTradeNamedosageNormName',
    'productsproductexpirationDateMonthYearmonth'				: 'productsexpirationDateMonhYearmonth',
    'productsproductdrugPurchaseObjectInfodrugInfoUsingReferenceInfoexpiratioeCustomFormatInfoexpirationDateMonthYearmonth'	: 'productsexpirationDateMonthYearmonth',
    'productsproductexpirationDateMonthYearyear'				: 'productsexpirationDateMnthYearyear',
    'productsproductdrugPurchaseObjectInfodrugIerenceInfoexpirationDateCustomFormatInfoexpiMonthYearyear'	: 'productsexpirationDateMonthYearyear','priceInfoprice'											: 'priceInfoprice','priceInfopriceType'										: 'priceInfopriceType',
    'prirencycode'										: 'priceInfocurrencycode',
    'priceInfocurr'										: 'priceInfocurrencyname',
    'priceInfocurre'									: 'priceInfocurrencyRaterate',
    'rrencyRateraiting'								: 'priceInfocurrencyRateraiting',
    'priceInfopriceRUR'											: 'priceInfopriceRUR','priceInfopriceVAT'											: 'priceInfopriceVAT',
    'popriceVATRUR'										: 'priceInfopriceVATRUR',
    'priceInfopriceFormula'										:'priceInfopriceFormula',
    'priceInfoamountsReducedByTaxes'							: 'priceoamountsReducedByTaxes',
    'supplierssupplierindividualPersonRFme'				: 'supplierslastName',
    'supplierssupplierlegalEntityRFcontactInfolastName'			: 'suppierslastName',
    'supplierssuppliercontactInfolastName'						: 'supplierslastName',
    'supplersInfosupplierInfolegalEntityRFotherInfocontactInfolastName'	: 'supplierslastNa',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrEGRIPInfolastName'	: 'sulierslastName',
    'suppliersInfosupplierInfoindividualPersonRFlastName'		: 'supierslastName',
    'supplierssupplierindividualPersonForeignStatelastName'		: 'supplierslastName',
    'supplierssupplierindividualPersonRFisCulturelastName'		: 'supplslastName',
    'suppliersInfosupplierInfocontactInfolastName'				: 'supplierslastName',
    'suppliersInosupplierInfoindividualPersonForeignStatelastName'			: 'supplierslastName',
    'supplierfosupplierInfoindividualPersonRFIndEntrisCultureEGRIPInfolastName'	: 'sierslastName',
    'suppliersInfosupplierInfoindividualPersonRFisCulturelastName'			: 'supplierslasame',
    'suppliersInfosupplierInfoEGRIPInfolastName'				: 'supplierslase',
    'suppliersInfosupplierInfoindividualPersonForeignStateisCulturelastName'	: 'supplierslastName',
    'supplierssupplierindividualPersonRFfir'				: 'suppliersfirstName',
    'supplierssupplierlegalEntityRFcontactInfofirstName'		: 'suppliesfirstName',
    'supplierssuppliercontactInfofirstName'						: 'suppliersfirstName',
    'suppliesInfosupplierInfolegalEntityRFotherInfocontactInfofirstName'	: 'suppliersfirstName',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrEGRIPInfofirstName'	: 'supplrsfirstName',
    'supplierssupplierindividualPersonForeignStatefirstName'	: 'suppersfirstName',
    'supplierssupplierindividualPersonRFisCulturefirstName'		:'suppliersfirstName',
    'suppliersInfosupplierInfoindividualPersonRFfirstName'		: 'supplrsfirstName',
    'suppliersInfosupplierInfocontactInfofirstName'				: 'suppliersfirstName',
    'suppliersnfosupplierInfoindividualPersonForeignStatefirstName'		: 'suppliersfirstName',
    'supplienfosupplierInfoindividualPersonRFIndEntrisCultureEGRIPInfofirstName'	: 'siersfirstName',
    'suppliersInfosupplierInfoindividualPersonRFisCulturefirstName'			: 'suppliersfirName',
    'suppliersInfosupplierInfoEGRIPInfofirstName'				: 'suppliersfirme',
    'suppliersInfosupplierInfoindividualPersonForeignStateisCulturefirstName'	: 'suppliersfirstName',
    'supplierssupplierindividualPersonRFmidde'				: 'suppliersmiddleName',
    'supplierssupplierlegalEntityRFcontactInfomiddleName'		: 'supplirsmiddleName',
    'supplierssuppliercontactInfomiddleName'					: 'suppliersmiddleName',
    'supplirsInfosupplierInfolegalEntityRFotherInfocontactInfomiddleName'	: 'suppliersmiddleName',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrEGRIPInfomiddleName'	: 'supplersmiddleName',
    'supplierssupplierindividualPersonForeignStatemiddleName'	: 'supiersmiddleName',
    'supplierssupplierindividualPersonRFisCulturemiddleName'	:'suppliersmiddleName',
    'suppliersInfosupplierInfoindividualPersonRFmiddleName'		: 'supplrsmiddleName',
    'suppliersInfosupplierInfocontactInfomiddleName'			: 'suppliersmiddleName',
    'suppliersnfosupplierInfoindividualPersonForeignStatemiddleName'		: 'suppliersmiddleName',
    'supplieInfosupplierInfoindividualPersonRFIndEntrisCultureEGRIPInfomiddleName'	: 'siersmiddleName',
    'suppliersInfosupplierInfoindividualPersonRFisCulturemiddleName'		: 'suppliersmiddame',
    'suppliersInfosupplierInfoEGRIPInfomiddleName'				: 'suppliddleName',
    'suppliersInfosupplierInfoindividualPersonStateisCulturemiddleName'			: 'suppliersmiddleName',
    'supplierssuppliendividualPersonRFINN'					: 'suppliersINN',
    'supplierssupplierlegalEntityRFINN'							: 'suppliersINN',
    'suppliersInfosupplierInfolegalEntityRFEGRULInfN'		: 'suppliersINN',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrEGRIPInfoINN'		: 'suppliersINN',
    'supplierssupplierindividualPersonRFireINN'			: 'suppliersINN',
    'supplierssupplierlegalEntityForeignStaegisterInRFTaxBodiesINN'		: 'suppliersINN',
    'suppliersInfosupplierInfoEGRULInfoINN'						: 'supplersINN',
    'suppliersInfosupplierInfoindividualPersonRFINN'			: 'suppliersINN',
    'suppliernfosupplierInfoindividualPersonForeignStateregisterInRFTaxBodiesINN'	: 'suppliesINN',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrisCultureEGRIPInfoINN'		: 'suppiersINN',
    'suppliersInfosupplierInfoindividualPersonRFisCINN'	: 'suppliersINN',
    'supplierssupplierindividualPersonForeignStateisterInRFTaxBodiesINN'	: 'suppliersINN',
    'suppliersInfosupplierInfoEGRIPInfoINN'						: 'supiersINN',
    'suppliersInfosupplierInforegisterInRFTaxBodiesINN'			:'suppliersINN',
    'suppliersInfosupplierInfolegalEneignStateregisterInRFTaxBodiesINN'		: 'suppliersINN',
    'supplierssuppliregisterInRFTaxBodiesINN'					: 'suppliersINN',
    'supplierssupplierlegalEntityRFKPP'							: 'suppliersKPP',
    'suppliersInfosupplierInfolegalEntitULInfoKPP'		: 'suppliersKPP',
    'supplierssupplierlegalEntityForeignStateregisterInRFTaxBodiesKP'			: 'suppliersKPP',
    'suppliersInfosupplierInfoEGRULInfoKPP'						:'suppliersKPP',
    'suppliersInfosupplierInfolegalEntityRFlegalEntityRFSubdivisionEGRULIKPP'	: 'suppliersKPP',
    'supplierssupplierlegalEntityRFlargestTaxpayerKPP'			: 'suppliersKPP',
    'suppliersInfosupplierInfolegalEntityRFotherInfolestTaxpayerKPP'			: 'suppliersKPP',
    'suppliersInfosupplierInfootherInfolargestTaxpayerKPP'		: 'suppliersKPP',
    'suppliersInfosupplierInforegisterInRFTaxBoPP'			: 'suppliersKPP',
    'suppliersInfosupplierInfolegalEntityForeignStateregisterInRTaxBodiesKPP'	: 'suppliersKPP',

    'supplierssupplierindividualPersonRFisIP'					: 'suppliersisIP',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrotheroisIP' : 'suppliersisIP',

    'supplierssupplierindividualPersonRFregistrationDate'		: 'suppliersreistrationDate',
    'supplierssupplierlegalEntityRFregistrationDate'			: 'suppliersregistrationDate',
    'supplersInfosupplierInfolegalEntityRFEGRULInforegistrationDate'	: 'suegistrationDate',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrEInforegistrationDate'	: 'suppliersregistrationDate',

    'suppliersserOKTMOcode'								: 'suppliersOKTMOcode',
    'supplierssupplierindividualPersonRFOKMOcode'				: 'suppliersOKTMOcode',
    'supplierssupplierlegalEntityRFOKTMOcode'					: 'suppliersOTMOcode',
    'suppliersInfosupplierInfolegalEntityRFotheMOcode'	: 'suppliersOKTMOcode',
    'suppliersInfosupplierInfoindividualPeRFIndEntrotherInfoOKTMOcode'	: 'suppliersOKTMOcode',

    'suppliersserOKTMOname'								: 'suppliersOKTMOname',
    'supplierssupplierindividualPersonRFOKMOname'				: 'suppliersOKTMOname',
    'supplierssupplierlegalEntityRFOKTMOname'					: 'suppliersOTMOname',
    'suppliersInfosupplierInfolegalEntityRFotherInfoOKTMOname'	:'suppliersOKTMOname',
    'suppliersInfosupplierInfoindividualPeIndEntrotherInfoOKTMOname'	: 'suppliersOKTMOname',

    'supplierssupplierindividulPersonRFaddress'				: 'suppliersaddress',
    'supplierssupplierlegalEntityRFaddress'						:'suppliersaddress',
    'suppliersInfosupplierInfolegalEntityRFEGRULInfoaddress'	: 'suppliersaddress',
    'suppliersInfosupplierInfoindividualPersonRFIndEGRIPInfoaddress'	: 'suppliersaddress',

    'supplierssupplierindividualPersonRFcontactEMail'			: 'supplierscontactEMail',
    'supplierssupplierlegalEntityRFcontactEMail'				: 'supplierscontactEMal',
    'suppliersInfosupplierInfolegalEntityRFotherInfocontactEMail'	: 'supplierntactEMail',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrotherInntactEMail'	: 'supplierscontactEMail',

    'supplierssupplierindividualPersonRFcontactPhone'			: 'supplierscontactPhone',
    'supplierssupplierlegalEntityRFcontactPhone'				: 'supplierscontactPhoe',
    'suppliersInfosupplierInfolegalEntityRFotherInfocontactPhone'	: 'supplcontactPhone',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrotherInfocontactPhone'	:'supplierscontactPhone',

    'supplierssupplierindividualPersonRFisCulture'				: 'supplierCulture',

    'supplierssupplierindividualPersonRFpostAddressInfomailingAdress'	: 'suppliersmailingAdress',
    'supplierssupplierlegalEntityRFpostAdressInfomaiAdress'			: 'suppliersmailingAdress',
    'supplierssupplierpostAdressInfomailingAdress'				: 'suppliersmailngAdress',
    'supplierssupplierpostAddressInfomailingAdress'				: 'supplielingAdress',
    'suppliersInfosupplierInfolegalEntityRFotherInAdressInfomailingAdress'	: 'suppliersmailingAdress',

    'supplierssupplierindidualPersonRFstatus'					: 'suppliersstatus',
    'supplierssupplierlegalEntityRFstatus'					: 'suppliersstatus',
    'suppliersInfosupplierInfolegalEntityRFotherInfostatus'		: 'suppliersstatus',
    'suppliersInfosupplierInfoindividualPersonRFIndEntrotherInfostatus'	: 'suppliersstat',

    'supplierssupplierindividualPersonRFpostAddressInfomailFacilityName': 'supplsmailFacilityName',
    'supplierssupplierlegalEntityRFpostAdressInfomailFacilityName'	: 'suppliersmailFacilityName',
    'supplierssupplierpostAdressInfomailFacilityName'			: 'suppliersmailFacilityNme',
    'supplierssupplierpostAddressInfomailFacilityName'			: 'suppliersmailFacilityName',
    'supliersInfosupplierInfolegalEntityRFotherInfopostAdressInfomailFacilityName'	: 'suppliersmaililityName',

    'supplierssupplierindividualPersonRFpostAddressInfopostBoxNumber'	: 'supplierspostBoxNumber',
    'supplierssupplierlegalEntityRFpostAdressInfopoxNumber'			: 'supplierspostBoxNumber',
    'supplierssupplierpostAdressInfopostBoxNumber'				: 'supplierspotBoxNumber',
    'supplierssupplierpostAddressInfopostBoxNumber'				: 'supplostBoxNumber',
    'suppliersInfosupplierInfolegalEntityRFotherInfopostAdressIpostBoxNumber'	: 'supplierspostBoxNumber',

    'supplierssupplierlegalEntitostAddress'					: 'supplierspostAddress',
    'supplierssupplierualPersonRFpostAddress'			: 'supplierspostAddress',

    'supplierssupplierlegalEntityRFlegalFrmcode'				: 'supplierslegalFormcode',
    'supplierssupplierlegalFormcode'							: 'splierslegalFormcode',
    'suppliersInfosupplierInfolegalEntityRFEGRULInfolegalFde'	: 'supplierslegalFormcode',

    'supplierssupplierlegalEntityRFlegalFormsingularName'		: 'supplierslegalFrmsingularName',
    'supplierssupplierlegalFormsingularName'					: 'supplierslegmsingularName',
    'suppliersInfosupplierInfolegalEntityRFEGRULInfolegalFormsingulaName'	: 'supplierslegalFormsingularName',

    'supplierssupplierlegatyRFfullName'					: 'suppliersfullName',
    'suppliersInfosupplierInfolegalEntityRFEGULInfofullName'	: 'suppliersfullName',

    'supplierssupplierlegtyRFshortName'					: 'suppliersshortName',
    'suppliersInfosupInfolegalEntityRFEGRULInfoshortName'	: 'suppliersshortName',

    'supplierssupplieregalEntityRFOKPO'						: 'suppliersOKPO',

    'supplierssupplierlegalEntFfirmName'					: 'suppliersfirmName',
    'suppliersInfosupplierInfolegalEntityRFEGRULInfofirmName'	: 'suppliersfirmName',

    'supplierssupplierlegalEntityRFcontractPrice'				: 'supplierscontractPrice'
}


def db_connect():
    """Соединение с базой данных"""
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '3306',
        'raise_on_warnings': True
    }
    return mysql.connect(**config)


def get_columns(table):
    """Функция получения списка столбцов таблицы
    :param table: Имя таблицы
    :return: Список столбцов"""
    try:
        connection = db_connect()
        with connection.cursor as cursor:
            query = f"SHOW COLUMNS FROM {table}"
            cursor.execute(query)
            columns = cursor.fetchall()
        connection.close()
        result = [column[0] for column in columns]
        return result
    except Error as e:
        print(f'The error {e} was occurred')


def get_contracts_numbers(table):
    """Функция получения списка контрактов
    :param table: Имя таблицы
    :return: Список контрактов"""
    try:
        connection = db_connect()
        with connection.cursor as cursor:
            query = f"SELECT `nn`.`regNum`, `nn`.`publishDate` FROM `{table}` AS `nn`"
            cursor.execute(query)
            ids = cursor.fetchall()
        connection.close()
        result = {}
        for i in ids:
            result[i[0]] = {'regNum': i[0], 'publishDate': i[1]}
        return result
    except Error as e:
        print(f'The error {e} was occurred')


def get_suppliers_info(table, region):
    """Функция получения информации о подрядчиках
    :param table: Имя таблицы
    :param region: Регион
    :return: Информация о подрядчиках"""
    try:
        connection = db_connect()
        query = f"""
SELECT 
  `t`.`suppliersINN`, 
  `t`.`suppliersKPP`, 
  `t`.`suppliersfullName`, 
  `t`.`suppliersaddress`, 
  `t`.`supplierscontactEMail`, 
  `t`.`supplierscontactPhone`, 
  `t`.`supplierslastName`, 
  `t`.`suppliersfirstName`, 
  `t`.`suppliersmiddleName` 
FROM 
  `{table}` AS `t` 
WHERE 
  `t`.`region` = '{region}' 
  AND `t`.`suppliersINN` IS NOT NULL"""
        with connection.cursor as cursor:
            cursor.execute(query)
            contracts = cursor.fetchall()
        connection.close()
        result = []
        for contract in contracts:
            inn = contract[0].split(';:;')
            kpp = None if contract[1] is None else contract[1].split(';:;')
            name = None if contract[2] is None else contract[2].split(';:;')
            address = None if contract[3] is None else contract[3].split(';:;')
            email = None if contract[4] is None else contract[4].split(';:;')
            phone = None if contract[5] is None else contract[5].split(';:;')
            last_name = None if contract[6] is None else contract[6].split(';:;')
            first_name = None if contract[7] is None else contract[7].split(';:;')
            middle_name = None if contract[8] is None else contract[8].split(';:;')
            k = 0

            for _ in inn:
                pres = {
                    'inn': inn[k],
                    'kpp': '' if kpp is None else (kpp[0] if k >= len(kpp) else kpp[k]),
                    'name': '' if name is None else (name[0] if k >= len(name) else name[k]),
                    'address': '' if address is None else (address[0] if k >= len(address) else address[k]),
                    'email': '' if email is None else (email[0] if k >= len(email) else email[k]),
                    'phone': '' if phone is None else (phone[0] if k >= len(phone) else phone[k]),
                    'fio': '' if last_name is None else (last_name[0] if k >= len(last_name) else last_name[k])}
                pres['fio'] += '' if first_name is None else ' ' + (
                    first_name[0] if k >= len(first_name) else first_name[k])
                pres['fio'] += '' if middle_name is None else ' ' + (
                    middle_name[0] if k >= len(middle_name) else middle_name[k])

                result.append(pres)
                k += 1
        return result
    except Error as e:
        print(f'The error {e} was occurred')


def create_columns(columns):
    """Функция создания столбцов
    :param columns: Перечень имен столбцов в виде списка"""
    try:
        connection = db_connect()
        columns = ', '.join(columns)
        with connection.cursor as cursor:
            query = "ALTER TABLE `northwestern_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `central_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `volga_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `southern_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `north_caucasian_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `ural_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `siberian_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `far_eastern_fd` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `moscow_and_moscow_region` " + columns
            cursor.execute(query)
            query = "ALTER TABLE `crimean_fd` " + columns
            cursor.execute(query)
            connection.commit()
        connection.close()
        return True
    except Error as e:
        print(f'The error {e} was occurred')


def update_values(table, columns, values):
    """Функция обновления записей в таблице
    :param table: Имя таблицы
    :param columns: Перечень имен столбцов в виде списка
    :param values: Данные для записи в виде списка кортежей"""
    try:
        connection = db_connect()
        columns = columns[3:]
        columns = [f"`{column}` = IFNULL(%s, DEFAULT(`{column}`))" for column in columns]
        sets = ', '.join(columns)
        values = (tuple(list(value)[1:-1] + [value[0]]) for value in values)
        query = f"UPDATE `{table}` SET {sets} WHERE `regNum` = %s"
        with connection.cursor as cursor:
            cursor.executemany(query, values)
            connection.commit()
        connection.close()
        return True
    except Error as e:
        print(f'The error {e} was occurred')


def insert_values(table, columns, values):
    """Функция добавления записей в таблицу
    :param table: Имя таблицы
    :param columns: Перечень имен столбцов в виде списка
    :param values: Данные для записи в виде списка кортежей"""
    try:
        connection = db_connect()
        val = re.sub(r'\$s', '%s', ', '.join(['IFNULL($s, DEFAULT(`%s`))'] * len(columns)) % tuple(columns))
        columns = '`, `'.join(columns)
        query = f"INSERT INTO `{table}` (`{columns}`) VALUES ({val})"
        with connection.cursor as cursor:
            cursor.executemane(query, values)
            connection.commit()
        connection.close()
        return True
    except Error as e:
        print(f'The error {e} was occurred')


def parse_for_update(columns, values):
    data = {}
    for idx, column in enumerate(columns):
        data[column] = {}
        for value in values:
            data[column][value[0]] = value[idx + 1]
    return data


def parse_sql(data, region):
    """Функция парсера БД"""
    global fieldsLinks
    columns_to_add = []
    preval = {}
    values = []
    updates = []

    # В зависимости от региона, получаем таблицу для записи
    if region in ['78', '47', '53', '60', '10', '29', '11', '35', '51', '83', '39']:
        table_name = 'northwestern_fd'
    elif region in ['32', '33', '37', '40', '44', '57', '62', '67', '69', '71', '76', '31', '36', '46', '48', '68']:
        table_name = 'central_fd'
    elif region in ['52', '43', '12', '13', '21', '58', '73', '64', '63', '56', '02', '16', '18', '59']:
        table_name = 'volga_fd'
    elif region in ['08', '34', '30', '01', '61', '23']:
        table_name = 'southern_fd'
    elif region in ['26', '15', '09', '07', '20', '06', '05']:
        table_name = 'north_caucasian_fd'
    elif region in ['66', '74', '45', '72', '89', '86']:
        table_name = 'ural_fd'
    elif region in ['04', '22', '54', '70', '42', '55', '19', '17', '24', '38', '03', '75']:
        table_name = 'siberian_fd'
    elif region in ['14', '79', '87', '25', '27', '28', '41', '49', '65']:
        table_name = 'far_eastern_fd'
    elif region in ['77', '50']:
        table_name = 'moscow_and_moscow_region'
    else:
        table_name = 'crimean_fd'

    contract_numbers = get_contracts_numbers(table_name)
    table_columns = get_columns(table_name)

    # Формируем столбцы для добавления в БД
    # !!!Внимание!!! Проверка столбцов чувствительна к регистру. EndDate не равно endDate.
    for notif in data:
        value = {}
        for column in data[notif]:
            if column in fieldsLinks:
                col = fieldsLinks[column]
                if col not in table_columns:
                    columns_to_add.append('ADD `' + col + '` mediumtext')
                    table_columns.append(col)
                value[col] = data[notif][column]
        preval[notif] = value

    # Если есть новые столбцы, то добавляем их в БД
    if len(columns_to_add) > 0:
        create_columns(columns_to_add)

    # Формируем данные для записи/обновления в БД
    for notif in preval:
        if notif not in contract_numbers:
            value = []
            for it in table_columns:
                if it in preval[notif]:
                    value.append(preval[notif][it])
                elif it == 'region':
                    value.append(region)
                else:
                    value.append(None)
            values.append(tuple(value))
        else:
            update = []
            if preval[notif]['publishDate'] >= contract_numbers[notif]['publishDate']:
                for it in table_columns:
                    if it in preval[notif]:
                        update.append(preval[notif][it])
                    else:
                        update.append(None)

                update = update[1:]
                update.append(update.pop(0))
                updates.append(tuple(update))

                contract_numbers[notif]['publishDate'] = preval[notif]['publishDate']

    # Обновление сущестыующих записей в БД
    # разкоментировать, чтобы записи обнавлялись, иначе будет пропускать
    if len(updates) > 0:
        res_upt = update_values(table_name, table_columns, updates)

    # Добавление новых записей в БД
    if len(values) > 0:
        res_ins = insert_values(table_name, table_columns, values)

    print(len(data), len(values), len(updates))
