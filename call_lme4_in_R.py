import os
import subprocess


class callR:
    def __init__(self, col, fname, wfname1, wframe2, script_path=None, if_SA = None):
        self.col = col
        self.fname = fname
        self.wfname1 = wfname1
        self.wframe2 = wframe2
        self.script_path = script_path
        self.if_SA = if_SA
        # self.if_SA_4 = False
        # self.if_SA_5 = False
        # self.if_SA_6 = False
        # self.if_SA_7 = False
        # self.if_SA_8 = False
        self.if_SA_regional = False
        if self.if_SA == "SA4":
            self.script_path = "R_SA/SA_4"
        elif self.if_SA == "SA5":
            self.script_path = "R_SA/SA_5"
        elif self.if_SA == "SA6":
            self.script_path = "R_SA/SA_6"
        elif self.if_SA == "SA7":
            self.script_path ="R_SA/SA_2"
        elif self.if_SA == "SA8":
            self.script_path = "R_SA/SA_1"
        elif self.if_SA == "SARegional":
            self.script_path = "R_SA/SA_2"

    def execute(self):
        rscript, rscript2, rscript3, rscript4 = None, None, None, None
        if self.script_path:
            rscript = "Rscript {}/final_meta_model_{}.R {} {} {}".format(self.script_path, self.col, self.fname, self.wfname1, self.wframe2)
        else:
            rscript = "Rscript final_meta_model_{}.R {} {} {}".format(self.col, self.fname, self.wfname1, self.wframe2)
            wfname2 = "EV_vs_all_{}".format(self.wfname1)
            rscript2 = "Rscript final_ev_vs_all_vec_model.R {} {} {}".format(self.fname, wfname2, self.col)
            wfname3 = "EVFleet_vs_light{}".format(self.wfname1)
            rscript3 = "Rscript ev_fleet_vs_nonev_fleet_model.R {} {} {}".format(self.fname, wfname3, self.col)
            wfname4 = "EVFleet_vs_all{}".format(self.wfname1)
            rscript4 = "Rscript ev_fleet_vs_all_fleet_model.R {} {} {}".format(self.fname, wfname4, self.col)

        print("Rscript1: ", rscript)
        print("Rscript2", rscript2)
        print("Rscript3", rscript3)
        print("Rscript4", rscript4)

        # print(os.system(rscript))

        try:
            # Try to capture both stdout and stderr
            result = subprocess.check_output(rscript, stderr=subprocess.STDOUT, shell=True)
            print(result.decode('utf-8'))  # decode byte string into a regular string
        except subprocess.CalledProcessError as e:
            # If an error occurs, print the output which includes the error message
            print("Command failed with return code", e.returncode)
            print(e.output.decode('utf-8'))  # decode byte string into a regular string
        # if rscript2:
        #     try:
        #         result = subprocess.check_output(rscript2, stderr=subprocess.STDOUT, shell=True)
        #         print(result.decode('utf-8'))  # decode byte string into a regular string
        #     except subprocess.CalledProcessError as e:
        #         # If an error occurs, print the output which includes the error message
        #         print("Command failed with return code", e.returncode)
        #         print(e.output.decode('utf-8'))  # decode byte string into a regular string
        # if rscript3:
        #     try:
        #         result = subprocess.check_output(rscript3, stderr=subprocess.STDOUT, shell=True)
        #         print(result.decode('utf-8'))  # decode byte string into a regular string
        #     except subprocess.CalledProcessError as e:
        #         # If an error occurs, print the output which includes the error message
        #         print("Command failed with return code", e.returncode)
        #         print(e.output.decode('utf-8'))  # decode byte string into a regular string
        # if rscript4:
        #     try:
        #         result = subprocess.check_output(rscript4, stderr=subprocess.STDOUT, shell=True)
        #         print(result.decode('utf-8'))  # decode byte string into a regular string
        #     except subprocess.CalledProcessError as e:
        #         # If an error occurs, print the output which includes the error message
        #         print("Command failed with return code", e.returncode)
        #         print(e.output.decode('utf-8'))  # decode byte string into a regular string


if __name__ == "__main__":
    obj = callR('AF', 'model_AC_2013_2019_no2.csv', 'a.csv', 'b.csv').execute()

