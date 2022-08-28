import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from PIL import Image
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import MolDraw2D
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import io


class App(ttk.Frame):

     def __init__(self, master, **kw):
        template = Chem.MolFromSmiles('c1nccc2n1ccc2')
        AllChem.Compute2DCoords(template)

        ms = [Chem.MolFromSmiles(smi) for smi in ('OCCc1ccn2cnccc12', 'C1CC1Oc1cc2ccncn2c1', 'CNC(=O)c1nccc2cccn12')]
        _ = [AllChem.GenerateDepictionMatching2DStructure(m, template) for m in ms]
        d = rdMolDraw2D.MolDraw2DCairo(50, 50)
        d.DrawMolecule(ms[0])
        d.FinishDrawing()
        png = d.GetDrawingText()
        mol = Chem.MolFromPNGString(png)
        Chem.MolToSmiles(mol)


        self.SortDir = True
        #f = ttk.Frame(master) #1. this widget is self, no need to assign to f. 2. You missed out .__init__().
        ttk.Frame.__init__(self, master)
        #f.pack(fill=tk.BOTH, expand=True)# redundant. done by app.grid


        #self.dataCols = ('Project Name', 'Status', 'Cores', 'Turn', 'Added date/time')
        #I have removed 'Project Name' since it is #0. self.dataCols is for #01, #02, .. onwards
        self.dataCols = ('Status', 'Cores', 'Turn', 'Added date/time')
        #self.tree = ttk.Treeview(self, columns=self.dataCols, show='headings')
        # Did not define widget's parent? I have added. Picture not shown because u used option show='headings'
        self.tree = ttk.Treeview(self, columns=self.dataCols)
        #self.tree.column("Project Name", anchor="center")
        #self.tree.grid(in_=f, row=0, column=0, sticky=tk.NSEW)
        # I have removed "in_=f" since parent has been defined.
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Setup column heading
        self.tree.heading('#0', text='Project Name', anchor='center')
        self.tree.heading('#1', text='Status', anchor='center')
        self.tree.heading('#2', text='Cores', anchor='center')
        self.tree.heading('#3', text='Turn', anchor='center')
        self.tree.heading('#4', text='Added date/time', anchor='center')


        #f.rowconfigure(0, weight=1) # Use with .grid but not for .pack positioning method
        #f.columnconfigure(0, weight=1) # same as above
        style = ttk.Style(master)
        style.configure('Treeview', rowheight=38)

        self._img = tk.PhotoImage(data = png)
        self.tree.insert('', 'end', text="#0's text", image=self._img,
                         value=("A's value", "B's value"))

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('450x180+300+300')

    app = App(root)
    app.grid(row=0, column=0, sticky='nsew')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()