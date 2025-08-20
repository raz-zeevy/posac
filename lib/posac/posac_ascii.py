import os
from lib.posac.posac_output_parser import OutputParser

class PosacAscii:
    def __init__(self, file_path):
        self.file_path = file_path
        self.output_dir = os.path.dirname(file_path)

    def run(self):
        output = OutputParser.parse_output(self.file_path)
        # wrtie SOLUTION.PSC
        with open(os.path.join(self.output_dir, "SOLUTION.PSC"), "w") as file:
            file.write(output["psc_solution"])
        # Write MUMATRIX.PSC
        with open(os.path.join(self.output_dir, "MUMATRIX.ASC"), "w") as file:
            file.write(output["psc_mumatrix"])
        # Write ITEMFACT.PSC
        with open(os.path.join(self.output_dir, "ITEMFACT.PSC"), "w") as file:
            file.write(output["psc_item_fact"])



if __name__ == '__main__':
    posac_ascii = PosacAscii(r"C:\Users\Raz_Z\Projects\Shmuel\posac\lib\scripts\IdoPosac\POSAC.OUT")
    posac_ascii.run()