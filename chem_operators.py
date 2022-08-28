from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import MolDraw2D
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.Chem.AtomPairs import Pairs


class ChemOperators:
    def __str__(self):
        """
        All the chemical operations that are being made.
        this should not be a class... properly!!
        """

    @staticmethod
    def get_mol(smiles):
        """
        Gets molecule weight based on smiles code

        :param smiles: Smiles code for compound
        :type smiles: str
        :return: molecule weight in mols
        :rtype: Chem.MolFromSmiles
        """
        return Chem.MolFromSmiles(smiles)

    def png_string(self, smiles, size=(250, 100)):
        """
        Translate smiles code to a png-string that can be drawn, to get a 2d drawing of compounds from a smiles code

        :param smiles: Smiles code for a compound
        :type smiles: str
        :param size: The size of the picture
        :type size: (int, int)
        :return: A png in string formate
        :rtype: str
        """
        mol = self.get_mol(smiles)
        data = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
        data.DrawMolecule(mol)
        data.FinishDrawing()
        return data.GetDrawingText()

    def structure_search(self, methode, threshold, rows, smiles_search, morgan_values=None):
        """
        Compare molecules with a main smiles code, to see how similar they are.

        :param methode: What structure search methode to use. (general, morgan or dice)
        :type methode: str
        :param threshold: Minimum similarity score the compound needs
        :type threshold: int
        :param rows: Rows from the database with compounds.
        :type rows: dict
        :param smiles_search: Main smiles code, that compounds are compared to.
        :type smiles_search: str
        :param morgan_values: Morgan search values, for determining different variables of the search criteria.
        :type: list or None
        :return: Rows from the database, with compounds under the threshold removed.
        :rtype: dict
        """
        sub_search = self.sub_search_method(methode)
        smiles_1 = smiles_search
        compound_to_delete = []
        for compound in rows:
            smiles_2 = rows[compound]["smiles"]
            smiles_temp = (smiles_1, smiles_2)
            score = sub_search(smiles_temp)
            if score >= threshold:
                rows[compound]["match_score"] = round(score, 2)
            else:
                compound_to_delete.append(compound)

        for compound in compound_to_delete:
            rows.pop(compound)

        return rows

    def sub_search_method(self, methode):
        """
        set the methode to use

        :param methode: What methode to use
        :type methode: str
        :return: Sub_search with the right set-up
        :rtype: function
        """
        if methode == "finger":
            sub_search = self.match_sub_structure_general
        elif methode == "morgan":
            sub_search = self.match_morgan
        elif methode == "dice":
            sub_search = self.match_dice

        return sub_search

    def match_sub_structure_general(self, smiles):
        """
        Uses Fingerprint search to find out how similar two compounds are

        :param smiles: The two smiles codes that are compared
        :type smiles: tuple
        :return: Match score for how similar the two compounds are
        :rtype: int
        """
        mols = [self.get_mol(smile) for smile in smiles]
        fp1, fp2 = [FingerprintMols.FingerprintMol(mol) for mol in mols]

        match_score = DataStructs.FingerprintSimilarity(fp1, fp2) * 100
        return match_score

    def match_morgan(self, smiles, bonds, n_bits, chirality, features):
        """
        Using Morgan search to find out how similar two compounds are
        NEEDS TO READ UP ON THIS! ! !

        :param smiles: The two smiles codes that are compared
        :type smiles: tuple
        :param bonds:
        :type bonds:
        :param n_bits:
        :type n_bits: int
        :param chirality:
        :type chirality: bool
        :param features:
        :type features: bool
        :return: Match score for how similar the two compounds are
        :rtype: int
        """
        mols = [self.get_mol(smile) for smile in smiles]
        fp1, fp2 = [AllChem.GetMorganFingerprintAsBitVect(mol, radius=bonds, nBits=n_bits,
                                                          useChirality=chirality, useFeatures=features)
                    for mol in mols]

        match_score_1 = DataStructs.FingerprintSimilarity(fp1, fp2) * 100
        match_score_2 = DataStructs.TanimotoSimilarity(fp1, fp2) * 100
        return match_score_1, match_score_2

    def match_dice(self, smiles):
        """
        uses Dice search to find out how similar two compounds are

        :param smiles: The two smiles codes that are compared
        :type smiles: tuple
        :return: Match score for how similar the two compounds are
        :rtype: int
        """
        mols = [self.get_mol(smile) for smile in smiles]
        ap1, ap2 = [Pairs.GetAtomPairFingerprint(mol) for mol in mols]
        dice_match_score = DataStructs.DiceSimilarity(ap1, ap2) * 100
        return dice_match_score


if __name__ =="__main__":
    co = ChemOperators()

    #smiles1 = "c1nccc2n1ccc2"
    smiles1 = "CCO"
    smiles2 = "CCOC"
    smiles = (smiles2, smiles1)

    chirality = True
    features = False
    n_bits = 2048
    bound_range = 2

    size = (100, 100)

    #print(co.PNGString(mol1, size))
    print(co.match_sub_structure_general(smiles))
    print(co.match_morgan(smiles, bound_range, n_bits, chirality, features))
    print(co.match_dice(smiles))