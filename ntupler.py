print("Warming up...")
import ROOT
ROOT.EnableImplicitMT(4)
ROOT.gROOT.SetBatch()
ROOT.xAOD.Init()
ROOT.xAOD.EventInfo()
ROOT.xAOD.TruthParticleContainer()
from xAODDataSource import Helpers

ROOT.gInterpreter.Declare('#include "libCpp.h"')
import libPy

import glob
import argparse
argparser = argparse.ArgumentParser(description='myNtupler')
argparser.add_argument('--channel', help='Channel to process')

args = argparser.parse_args()


print("Done setting up libraries")

channels = [
    "mc20_ggf_hyy", 
    "mc23_vbf_hyy", 
    "mc20_vbf_hyy", 
    "mc23_ggf_hyy", 
    'mc20_qqzh_hyy', 
    'mc23_qqzh_hyy', 
    'mc20_ggzh_hyy', 
    'mc23_ggzh_hyy', 
    'mc20_wmh_hyy', 
    'mc23_wmh_hyy', 
    'mc20_wph_hyy', 
    'mc23_wph_hyy',
    'mc20_tth_hyy',
    'mc23_tth_hyy',
]

assert args.channel in channels, f"Channel {args.channel} is not in the list of available channels."

channel = args.channel

sample_dict = {
    "mc20_ggf_hyy":    'data/mc20_13TeV.343981.*/*.root.1',
    "mc20_vbf_hyy":    'data/mc20_13TeV.346214.*/*.root.1',
    "mc20_qqzh_hyy":   'data/mc20_13TeV.345319.*/*.root.1',
    "mc20_ggzh_hyy":   'data/mc20_13TeV.345061.*/*.root.1',
    "mc20_wph_hyy":    'data/mc20_13TeV.345318.*/*.root.1',
    "mc20_wmh_hyy":    'data/mc20_13TeV.345317.*/*.root.1',
    "mc20_tth_hyy":    "data/mc20_13TeV.346525.*/*.root.1",
    "mc23_ggf_hyy":  'data/mc23_13p6TeV.602421.*/*.root.1',
    "mc23_vbf_hyy":  'data/mc23_13p6TeV.601482.*/*.root.1',
    "mc23_qqzh_hyy": 'data/mc23_13p6TeV.601523.*/*.root.1',
    "mc23_ggzh_hyy": 'data/mc23_13p6TeV.601522.*/*.root.1',
    "mc23_wph_hyy":  'data/mc23_13p6TeV.601484.*/*.root.1',
    "mc23_wmh_hyy":  'data/mc23_13p6TeV.601483.*/*.root.1',
    "mc23_tth_hyy":  "data/mc23_13p6TeV.602422.*/*.root.1",
}

weights_to_save = [
    "hw_nominal",     # nominal MC weight
    "hw_pdf4lhc_unc", # 30 Eigen variation for PHD4LHC
    "hw_alphaS_up",   # up alpha_s variaton for PHD4LHC
    "hw_alphaS_dn",   # down alpha_s variaton for PHD4LHC
    "hw_qcd",         # muR/muF variation for the given MC
]

kine_to_save = ["Higgs_p4", "photon1_p4", "photon2_p4"] 

htxs_categories_to_save = {
    "HTXS_Njets_pTjet30"                  : "int"  ,        
    "HTXS_Stage1_Category_pTjet30"        : "int"  ,                
    "HTXS_Higgs_pt"                       : "float",      
    "HTXS_Stage1_2_Category_pTjet30"      : "int"  ,                    
    "HTXS_Stage1_2_Fine_Category_pTjet30" : "int"  ,                        
}

# for wrights used see: https://gitlab.cern.ch/atlas_higgs_combination/software/TruthWeightTools/blob/master/Root/HiggsWeightTool.cxx#L131

print(f"!!!!!!!!!!!!!!!!! Processing {channel}... !!!!!!!!!!!!!!!!!!")
f = glob.glob(sample_dict[channel])
df = Helpers.MakexAODDataFrame(f)

df, hwt = libPy.getHiggsWeightTool(df, channel)

df = df.Define("hw", "getHiggsWeights(EventInfo, hwt)")

# df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("photon1_p4", "Photons_p4[0]")
# df = df.Define("photon2_p4", "Photons_p4[1]")
for cata, dtype in htxs_categories_to_save.items():
    df = df.Define(cata, f'EventInfo.auxdataConst<{dtype}>  ("{cata}")')
for weight_name in weights_to_save:
    df = df.Define(weight_name, weight_name.replace("hw_", "hw."))
df.Snapshot('tree', f"ntuples/{channel}_stxs.root", weights_to_save + list(htxs_categories_to_save.keys()))