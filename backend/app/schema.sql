DROP TABLE IF EXISTS ppc;
DROP TABLE IF EXISTS sub;
CREATE TABLE ppc (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Year INTEGER NOT NULL,
  Month INTEGER NOT NULL,
  Power_Supplier INTEGER NOT NULL,
  HM_EKD TEXT NOT NULL,
  Contract_Account_ID INTEGER NOT NULL,
  Login_Date TEXT NOT NULL,
  AR_PAROXIS_11 INTEGER NOT NULL,
  Meter_Number INTEGER NOT NULL,
  Start_Period TEXT NOT NULL,
  End_Period TEXT NOT NULL,
  Total_ConsumptionDayPeak INTEGER NOT NULL,
  Total_ConsumptionNightOffpeak INTEGER NOT NULL,
  Total_Consumption INTEGER NOT NULL,
  Metering_Period TEXT NOT NULL,
  PoD_Postal_Code INTEGER NOT NULL,
  Square_Meters INTEGER NOT  NULL
);

CREATE TABLE sub (
id INTEGER PRIMARY KEY AUTOINCREMENT,
Contract_Account_ID INTEGER NOT NULL,
Keycloak_Account_ID TEXT NOT NULL
);