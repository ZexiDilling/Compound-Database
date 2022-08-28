"""
All tables used in the initial database.
"""

compound_main = """ CREATE TABLE IF NOT EXISTS compound_main( 
            compound_id INTEGER PRIMARY KEY, 
            smiles TEXT,
            png TEXT, 
            volume REAL,
            concentration REAL,
            ac = TEXT
            ac_id INTEGER,
            origin_id INTEGER,
            FOREIGN KEY (ac_id) REFERENCES origin(ac_id)
            ); """

compound_mp_table = """ CREATE TABLE IF NOT EXISTS compound_mp( 
            row_counter INTEGER PRIMARY KEY,
            mp_barcode TEXT,
            compound_id INTEGER,
            mp_well TEXT,
            volume REAL,
            date REAL,
            FOREIGN KEY (mp_barcode) REFERENCES mp_plates(mp_barcode),
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id)
            ); """

compound_dp_table = """ CREATE TABLE IF NOT EXISTS compound_dp( 
            row_counter INTEGER PRIMARY KEY,
            dp_barcode TEXT,
            compound_id INTEGER,
            dp_well TEXT, 
            volume REAL, 
            date REAL,         
            mp_barcode TEXT,
            mp_well TEXT,
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

bio_experiment_table = """ CREATE TABLE IF NOT EXISTS bio_experiment(
            exp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assay_name TEXT
            raw_data TEXT,
            plate_layout TEXT
            responsible TEXT,
            date REAL
            ); """

biological_data = """ CREATE TABLE IF NOT EXISTS biological(
            bio_data_id INTEGER PRIMARY KEY,
            compound_id INTEGER,
            experiment TEXT,
            result_max REAL,
            result_total TEXT,
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id),
            FOREIGN KEY (experiment) REFERENCES exp_id(experiment)
            ); """

lc_experiment_table = """ CREATE TABLE IF NOT EXISTS lc_experiment(
            batch PRIMARY KEY AUTOINCREMENT,
            date REAL
            ); """

purity_data = """ CREATE TABLE IF NOT EXISTS purity(
            purity_id INTEGER PRIMARY KEY,
            compound_id INTEGER,
            experiment TEXT,
            result_max REAL,
            result_max_ion REAL,
            result_total TEXT,
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id)
            ); """

lcms_experiment_raw = """ CREATE TABLE IF NOT EXISTS lc_raw(
            row_id INTEGER PRIMARY KEY,
            compound_id INTEGER,
            sample TEXT,
            batch TEXT,
            method TEXT,
            file_name TEXT,
            date REAL
            FOREIGN KEY (compound_id) REFERENCES compound_main(compound_id),
            FOREIGN KEY (batch) REFERENCES lc_experiment(batch)
            ); """

compound_source = """ CREATE TABLE IF NOT EXISTS origin(
                ac_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ac TEXT,
                origin TEXT
                ); """