import os
import subprocess


class callR:
    def __init__(self, col, fname, wfname1, wframe2, script_path=None):
        self.col = col
        self.fname = fname
        self.wfname1 = wfname1
        self.wframe2 = wframe2
        self.script_path = script_path
        self.if_SA_4 = False
        self.if_SA_5 = False
        self.if_SA_6 = False
        self.if_SA_7 = False
        self.if_SA_8 = False
        self.if_SA_regional = False
        if self.if_SA_4:
            self.script_path = "R_SA/SA_4"
        elif self.if_SA_5:
            self.script_path = "R_SA/SA_5"
        elif self.if_SA_6:
            self.script_path = "R_SA/SA_6"
        elif self.if_SA_7:
            self.script_path = "R_SA/SA_2"
        elif self.if_SA_8:
            self.script_path = "R_SA/SA_1"
        elif self.if_SA_regional:
            self.script_path = "R_SA/SA_2"

    def execute(self):
        if self.script_path:
            rscript = "Rscript {}/final_meta_model_{}.R {} {} {}".format(self.script_path, self.col, self.fname, self.wfname1, self.wframe2)
        else:
            rscript = "Rscript final_meta_model_{}.R {} {} {}".format(self.col, self.fname, self.wfname1, self.wframe2)
        print(rscript)
        # print(os.system(rscript))
        result = subprocess.check_output(rscript, shell=True)
        print(result)


if __name__ == "__main__":
    obj = callR('AF', 'model_AC_2013_2019_no2.csv', 'a.csv', 'b.csv').execute()

