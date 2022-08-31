import pandas as pd
import openpyxl
import json
import csv
import time
import os


mb = pd.read_excel('mb_table.xlsx')

mb.columns.values.tolist()

mb_headers = [
                "CustomerEmail",
                "CustomerMobilePhone",
                "CustomerFirstName",
                "CustomerMiddleName",
                "CustomerLastName",
                "CustomerIanaTimeZone",
                "CustomerTimeZoneSource",
                "CustomerIdsMindboxId",
                "CustomerBirthDate",
                "CustomerIsEmailInvalid",
                "CustomerIsMobilePhoneInvalid",
                "CustomerChangeDateTimeUtc",
                "CustomerIdsBitrixID",
                "CustomerIdsBitrixIDiport",
                "CustomerIdsContactID",
                "CustomerIdsCustomerID",
                "CustomerIdsId1C",
                "CustomerIdsIdiport1C",
                "CustomerIdsLegalUniqId",
                "CustomerIdsTest",
                "CustomerCustomFieldsActivatedBonusesIPort",
                "CustomerCustomFieldsActivatedBonusesNBcom",
                "CustomerCustomFieldsActivatedBonusesSamsung",
                "CustomerCustomFieldsActivatedBonusesSCenters",
                "CustomerCustomFieldsBonusesActivationDateIPort",
                "CustomerCustomFieldsBonusesActivationDateNBcom",
                "CustomerCustomFieldsBonusesActivationDateSamsung",
                "CustomerCustomFieldsBonusesActivationDateSCenters",
                "CustomerCustomFieldsBonusesBurningDateIPort",
                "CustomerCustomFieldsBonusesBurningDateNBcom",
                "CustomerCustomFieldsBonusesBurningDateSamsung",
                "CustomerCustomFieldsBonusesBurningDateSCenters",
                "CustomerCustomFieldsBonusesGeneral",
                "CustomerCustomFieldsBurningBonusesDate",
                "CustomerCustomFieldsBurningBonusesIport",
                "CustomerCustomFieldsBurningBonusesNBcom",
                "CustomerCustomFieldsBurningBonusesSamsung",
                "CustomerCustomFieldsBurningBonusesSCenters",
                "CustomerCustomFieldsClientType",
                "CustomerCustomFieldsCompanyNameForB2B",
                "CustomerCustomFieldsCreateSource",
                "CustomerCustomFieldsCustomerType",
                "CustomerCustomFieldsDeleted",
                "CustomerCustomFieldsDeviceMchmp",
                "CustomerCustomFieldsINN",
                "CustomerCustomFieldsKPP",
                "CustomerCustomFieldsLocationFromMC",
                "CustomerCustomFieldsMemberRating",
                "CustomerCustomFieldsMetkaFromMailChimp",
                "CustomerCustomFieldsOrgCustomerName",
                "CustomerCustomFieldsShop",
                "CustomerCustomFieldsTextLetterToTheFuture",
                "CustomerCustomFieldsTimeZonefronMailchimp",
                "CustomerCustomFieldsUpdateSource",
                "CustomerCustomerSubscriptionsNbcomIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmsIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmsnbcompanyIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmsiportIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmssamsungstoreIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmsscentresIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmsb2bIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomSmsMicroprice. ruIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailnbcompanyIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailiportIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailsamsungstoreIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailscentresIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailb2bIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomEmailMicroprice. ruIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomViberIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomVibernbcompanyIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomViberiportIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomVibersamsungstoreIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomViberscentresIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomViberb2bIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomViberMicroprice. ruIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushnbcompanyIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushiportIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushsamsungstoreIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushscentresIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushb2bIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomMobilePushMicroprice. ruIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushnbcompanyIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushiportIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushsamsungstoreIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushscentresIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushb2bIsSubscribed",
                "CustomerCustomerSubscriptionsNbcomWebPushMicroprice. ruIsSubscribed",
                "CustomerBalanceBonusnyjSchetNbcomTotal",
                "CustomerBalanceBonusnyjSchetNbcomAvailable",
                "CustomerBalanceBonusnyjSchetNbcomBlocked",
            ]

mb_headers_filter = [
                "CustomerEmail",
                "CustomerMobilePhone",
                "CustomerFirstName",
                "CustomerMiddleName",
                "CustomerLastName",
                "CustomerIanaTimeZone",
                "CustomerTimeZoneSource",
                "CustomerIdsMindboxId",
                "CustomerBirthDate",
                "CustomerIsEmailInvalid",
                "CustomerIsMobilePhoneInvalid",
                "CustomerChangeDateTimeUtc",
                "CustomerIdsBitrixID",
                "CustomerIdsBitrixIDiport",
                "CustomerIdsContactID",
                "CustomerIdsCustomerID",
                "CustomerIdsId1C",
                "CustomerIdsIdiport1C",
                "CustomerIdsLegalUniqId",
            ]

mb_copy = mb.copy()

for header in mb_headers:
    if header not in mb_headers_filter:
        mb_copy.drop(header, axis=1, inplace=True)

mb_with_phone_numbers = mb_copy.dropna(subset='CustomerMobilePhone')

mb_with_phone_numbers = mb_with_phone_numbers.astype({"CustomerMobilePhone": "str"})