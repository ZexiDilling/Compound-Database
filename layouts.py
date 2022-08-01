"""
All tables used in the initial database.
"""

compound_main = """ CREATE TABLE IF NOT EXISTS compound_main( 
            compound_id INTEGER PRIMARY KEY, 
            smiles TEXT,
            png TEXT, 
            volume REAL
            ); """

compound_mp_table = """ CREATE TABLE IF NOT EXISTS compound_mp( 
            compound_id INTEGER,
            mp_barcode TEXT,
            mp_well TEXT,
            volume REAL,
            FOREIGN KEY (mp_barcode) REFERENCES mp_plates(mp_barcode),
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id)
            ); """

compound_dp_table = """ CREATE TABLE IF NOT EXISTS compound_dp( 
            compound_id INTEGER,
            mp_barcode TEXT,
            mp_well TEXT,
            dp_barcode TEXT,
            dp_well, 
            volume REAL, 
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id),
            FOREIGN KEY (mp_barcode) REFERENCES mp_plates(mp_barcode),
            FOREIGN KEY (dp_barcode) REFERENCES dp_plates(dp_barcode)
            ); """

compound_data_table = """ CREATE TABLE IF NOT EXISTS compound_data( 
            compound_id INTEGER,
            exp_id INTEGER,
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id),
            FOREIGN KEY (exp_id) REFERENCES experiment(exp_id)
            ); """

mother_plate_table = """ CREATE TABLE IF NOT EXISTS mp_plates(
            mp_barcode TEXT PRIMARY KEY,
            date REAL
            ); """

daughter_plate_table = """ CREATE TABLE IF NOT EXISTS dp_plates(
            dp_barcode TEXT PRIMARY KEY,
            date REAL     
            ); """

location_table = """ CREATE TABLE IF NOT EXISTS locations(              
            loc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            location TEXT,
            spot TEXT
            ); """

experiment_table = """ CREATE TABLE IF NOT EXISTS experiment(
            exp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            responsible TEXT,
            date REAL
            ); """

purity_data = """ CREATE TABLE IF NOT EXISTS purity(
            compound_id TEXT,
            experiment TEXT,
            result_max REAL,
            result_max_ion REAL,
            result_total TEXT,
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id)
            ); """

biological_data = """ CREATE TABLE IF NOT EXISTS biological(
            compound_id TEXT,
            experiment TEXT,
            result_max REAL,
            result_total TEXT,
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id),
            FOREIGN KEY (experiment) REFERENCES exp_id(experiment)
            ); """