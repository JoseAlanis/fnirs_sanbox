import pathlib
import os.path as op

# names of sources and detectors in the montage
sources_and_detector_names = dict(S1='AF7', S2='Fpz', S3='AF8', S4='AF3', S5='AF4',
                                  S6='F3', S7='Fz', S8='F4', S9='FC1', S10='FC5',
                                  S11='FT9', S12='C3', S13='T7', S14='CP5', S15='TP9',
                                  S16='P7', S17='FC2', S18='FC6', S19='FT10', S20='C4',
                                  S21='T8', S22='CP6', S23='TP10', S24='P8', S25='CP1',
                                  S26='CP2', S27='Pz', S28='P3', S29='P4', S30='POz',
                                  S31='O1', S32='O2',

                                  D1='Fp1', D2='Fp2', D3='AFz', D4='F1', D5='F2',
                                  D6='FCz', D7='C1', D8='C2', D9='FC3', D10='FT7',
                                  D11='F9', D12='P5', D13='TP7', D14='P5', D15='P9',
                                  D16='PO7', D17='FC4', D18='FT8', D19='F10', D20='C6',
                                  D21='TP8', D22='P6', D23='P10', D24='PO8', D25='CPz',
                                  D26='P1', D27='P2', D28='PO3', D29='PO4', D30='Oz')

DATA_PATH = op.join(pathlib.Path(__file__).parent.resolve(), "data")
