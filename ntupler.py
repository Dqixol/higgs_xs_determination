print("Warming up...")
import ROOT
import glob
ROOT.EnableImplicitMT(16)
ROOT.gROOT.SetBatch()

ROOT.xAOD.Init()
ROOT.xAOD.JetContainer()
ROOT.xAOD.TauJetContainer()
ROOT.xAOD.MuonContainer()
ROOT.xAOD.ElectronContainer()
ROOT.xAOD.EventInfo()
ROOT.gInterpreter.Declare('#include "libPhys.h"')

from xAODDataSource import Helpers
print("Done setting up libraries")

channels = ["mc20e_ggf_hyy", "mc23e_vbf_hyy", "mc20e_vbf_hyy", "mc23e_ggf_hyy"]
channels = [channel for channel in channels if 'mc20e_vbf_hyy' in channel]

weights_to_save = [
    "hw_nominal",     # nominal MC weight
    "hw_pdf4lhc_unc", # 30 Eigen variation for PHD4LHC
    "hw_alphaS_up",   # up alpha_s variaton for PHD4LHC
    "hw_alphaS_dn",   # down alpha_s variaton for PHD4LHC
    "hw_qcd",         # muR/muF variation for the given MC
]

# for wrights used see: https://gitlab.cern.ch/atlas_higgs_combination/software/TruthWeightTools/blob/master/Root/HiggsWeightTool.cxx#L131

for channel in channels:
    print(f"Processing {channel}...")
    if channel == "mc20e_ggf_hyy":
        f = glob.glob("data/mc20_13TeV.343981.PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_gamgam.deriv.DAOD_PHYS.e5607_s3681_r13145_p7018/*.root.1")
    elif channel == "mc23e_vbf_hyy":
        f = glob.glob("data/mc23_13p6TeV.601482.PhPy8EG_PDF4LHC21_VBFH125_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017/*.root.1")
    elif channel == "mc20e_vbf_hyy":
        f = glob.glob("data/mc20_13TeV.346214.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_gamgam.deriv.DAOD_PHYS.e6970_s3681_r13145_p7018/*.root.1")
    elif channel == "mc23e_ggf_hyy":
        f = glob.glob("data/mc23_13p6TeV.602421.PhPy8EG_PDF4LHC21_ggH_NNLOPS_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017/*.root.1")
    df = Helpers.MakexAODDataFrame(f)

    hwt = ROOT.TruthWeightTools.HiggsWeightTool( f"HiggsWeightTool_{channel}" )
    if 'vbf' in channel or 'VH-Had' in channel:
        hwt.setProperty( "ProdMode", "qq2H"  )
    elif 'ggf' in channel:
        hwt.setProperty( "RequireFinite", True )
        hwt.setProperty( "WeightCutOff", 100.0 )
        hwt.setProperty( "ProdMode", "ggF" )
    elif 'WpH' in channel or 'WmH' in channel:
        hwt.setProperty( "ProdMode", "WH" )
    elif 'qqZH' in channel:
        hwt.setProperty( "ProdMode", "qqZH" )
    elif 'ggZH' in channel:
        hwt.setProperty( "ProdMode", "ggZH" )
    elif 'ttH' in channel:
        hwt.setProperty( "ProdMode", "ttH" )
    hwt.initialize()
    hwt_ptr = ROOT.addressof(hwt)
    df = df.Define('hwt', f'''
        auto ret = reinterpret_cast<TruthWeightTools::HiggsWeightTool*>({hwt_ptr});
        return ret;
    ''')

    df = df.Define("hw", "getHiggsWeights(EventInfo, hwt)")
    df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
    df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
    df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
    df = df.Define("photon1_p4", "Photons_p4[0]")
    df = df.Define("photon2_p4", "Photons_p4[1]")
    for weight_name in weights_to_save:
        df = df.Define(weight_name, weight_name.replace("hw_", "hw."))
    df.Snapshot(channel, f"ntuples/{channel}.root", ["Higgs_p4", "photon1_p4", "photon2_p4"] + weights_to_save)
    df.Report().Print()