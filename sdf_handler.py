import configparser

from rdkit.Chem import AllChem
from rdkit import Chem
from rdkit.Chem.rdmolfiles import MolFromMolBlock
from chem_operators import ChemOperators


class SDFReader:

    def __init__(self, config, fd, dbf):
        self.size = (100, 100)
        self.co = ChemOperators()
        self.fd = fd
        self.dbf = dbf
        self.fact_cache = {}

    def __str__(self):
        """
        Reads SDF files

        :return: A dict of data with compound information
        """

    def _fact(self, search_limiter, table):
        ''' Memoized factorial function '''

        try:
            row = self.fact_cache[search_limiter["origin"]["value"]]
            return row["ac_id"]
        except KeyError:
            rows = self.fd.data_search(table, search_limiter)

        for row_id in rows:
            row = rows[row_id]

        try:
            self.fact_cache[search_limiter["origin"]["value"]] = row
            return self.fact_cache[search_limiter["origin"]["value"]]["ac_id"]
        except UnboundLocalError:
            temp_data_dict = {}
            ac_id = self.dbf.number_of_rows(table) + 1
            temp_data_dict["ac_id"] = ac_id
            for headlines in search_limiter:
                temp_data_dict[headlines] = search_limiter[headlines]["value"]

            self.dbf.add_records_controller(table, temp_data_dict)

        rows = self.fd.data_search(table, search_limiter)
        for row_id in rows:
            row = rows[row_id]

        self.fact_cache[search_limiter["origin"]["value"]] = row
        return self.fact_cache[search_limiter["origin"]["value"]]["ac_id"]


    @staticmethod
    def _sdf_to_mol(sdf_data):
        """
        Gets mols out of the SDF file

        :param sdf_data: Data from an SDF file
        :type sdf_data: str
        :return: Mols
        :rtype: Chem-mol-data
        """
        return Chem.SDMolSupplier(sdf_data)

    def _to_dict(self, mols):
        """
        Translate the SDF into dict for ease of use

        :param mols: Mols
        :type mols: Chem-mol-data
        :return: A dict of data
        :rtype: dict
        """
        data = {}
        search_limiter = {
            "ac": {"value": "",
                   "operator": "=",
                   "target_column": "ac"},
            "origin": {"value": "",
                       "operator": "=",
                       "target_column": "origin"}
        }
        # c = 0
        for idx, mol in enumerate(mols):

            if mol:
                # c += 1
                mol_id = mol.GetProp("Barcode")
                search_limiter["ac"]["value"] = mol.GetProp("A/C")
                search_limiter["origin"]["value"] = mol.GetProp("Origin")
                table = "origin"
                ac_id = self._fact(search_limiter, table)

                data[mol_id] = {}
                data[mol_id]["barcode"] = mol.GetProp("Barcode")
                data[mol_id]["smiles"] = Chem.MolToSmiles(mol)
                data[mol_id]["amount"] = mol.GetProp("Volume uL")
                data[mol_id]["concentration"] = mol.GetProp("Concentration mM")
                data[mol_id]["ac_id"] = ac_id
                data[mol_id]["origin_id"] = mol.GetProp("Origin ID")
                data[mol_id]["mol_data"] = self.co.png_string(Chem.MolToSmiles(mol), self.size)
                # if c == 2982:
                #     print("DATA IS OVER 2982 COMPOUNDS... IMPORT HAVE STOPPED... THIS IS FROM SDF_HANDLER")
                #     return data
        return data

    def run(self, sdf_data):
        """
        Runs the converter

        :param sdf_data: SDF file with compound data from a vendor
        :type sdf_data: str
        :return: A dict of data.
        :rtype: dict
        """
        mols = self._sdf_to_mol(sdf_data)
        data = self._to_dict(mols)

        return data


if __name__ == "__main__":
    sdf_file = "Enamine_New_030220.sdf"
    config = configparser.ConfigParser()
    config.read("config.ini")

    from database_handler import DataBaseFunctions
    from database_controller import FetchData
    fd = FetchData(config)
    dbf = DataBaseFunctions(config)

    sr = SDFReader(config, fd, dbf)
    sr.run(sdf_file)
