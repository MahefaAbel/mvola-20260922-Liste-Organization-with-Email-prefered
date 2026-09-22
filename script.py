import csv

INPUT_FILE = "list-organization-prefered-notif-email-20260922-12h06-saidou.csv"
OUTPUT_FILE = "update_preferred_channel_sms.sql"

def sql_escape(value):
    if value is None:
        return ""
    return str(value).strip().replace("'", "''")

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as csvfile:

    # Ton CSV utilise ; comme séparateur
    reader = csv.DictReader(csvfile, delimiter=";")

    print("Colonnes détectées :", reader.fieldnames)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as sqlfile:

        count = 0
        skipped = 0

        for row in reader:

            shortcode = sql_escape(row["SHORTCODE"])
            phone = sql_escape(row["PHONE"])

            # Sécurité : ne pas générer d'UPDATE
            # si shortcode ou téléphone est vide
            if not shortcode or not phone:
                print(
                    f"SKIPPED: SHORTCODE={shortcode}, PHONE={phone}"
                )
                skipped += 1
                continue

            sql = f"""UPDATE CPSMGT.CPS_ORG_KYC
SET
    FIELD_9 = 1001,
    FIELD_10 = '{phone}'
WHERE FIELD_9 = 1011
    AND IDENTITYID IN (
        SELECT bo.BIZ_ORG_ID
        FROM CPSMGT.CPS_BIZ_ORG bo
        WHERE bo.SHORT_CODE = '{shortcode}'
            AND bo.STATUS = 03
    );

"""

            sqlfile.write(sql)
            count += 1

print()
print("======================================")
print(f"UPDATE générés : {count}")
print(f"Lignes ignorées : {skipped}")
print(f"Total traité : {count + skipped}")
print(f"Fichier généré : {OUTPUT_FILE}")
print("======================================")