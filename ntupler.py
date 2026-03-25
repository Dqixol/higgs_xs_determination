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

# # mc23e_ggf_hyy
# f = glob.glob("mc23_13p6TeV.602421.PhPy8EG_PDF4LHC21_ggH_NNLOPS_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017/*.root.1")
# df = Helpers.MakexAODDataFrame(f)
# df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
# df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("photon1_p4", "Photons_p4[0]")
# df = df.Define("photon2_p4", "Photons_p4[1]")
# df = df.Define("weight_mc", "EventInfo.mcEventWeight()")
# df.Snapshot("mc23e_ggf_hyy", "mc23e_ggf_hyy.root", ["Higgs_p4", "weight_mc", "photon1_p4", "photon2_p4"])
# df.Report().Print()


# mc20e_ggf_hyy
f = glob.glob("mc20_13TeV.343981.PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_gamgam.deriv.DAOD_PHYS.e5607_s3681_r13145_p7018/*.root.1")
df = Helpers.MakexAODDataFrame(f)
df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
df = df.Define("photon1_p4", "Photons_p4[0]")
df = df.Define("photon2_p4", "Photons_p4[1]")
df = df.Define("weight_mc", "EventInfo.mcEventWeight()")
df.Snapshot("mc20e_ggf_hyy", "mc20e_ggf_hyy.root", ["Higgs_p4", "weight_mc", "photon1_p4", "photon2_p4"])
df.Report().Print()

# # mc23e_vbf_hyy
# f = glob.glob("mc23_13p6TeV.601482.PhPy8EG_PDF4LHC21_VBFH125_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017/*.root.1")
# df = Helpers.MakexAODDataFrame(f)
# df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
# df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("photon1_p4", "Photons_p4[0]")
# df = df.Define("photon2_p4", "Photons_p4[1]")
# df = df.Define("weight_mc", "EventInfo.mcEventWeight()")
# df.Snapshot("mc23e_vbf_hyy", "mc23e_vbf_hyy.root", ["Higgs_p4", "weight_mc", "photon1_p4", "photon2_p4"])
# df.Report().Print()

# # mc20e_vbf_hyy
# f = glob.glob("mc20_13TeV.346214.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_gamgam.deriv.DAOD_PHYS.e6970_s3681_r13145_p7018/*.root.1")
# df = Helpers.MakexAODDataFrame(f)
# df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
# df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
# df = df.Define("photon1_p4", "Photons_p4[0]")
# df = df.Define("photon2_p4", "Photons_p4[1]")
# df = df.Define("weight_mc", "EventInfo.mcEventWeight()")
# df.Snapshot("mc20e_vbf_hyy", "mc20e_vbf_hyy.root", ["Higgs_p4", "weight_mc", "photon1_p4", "photon2_p4"])
# df.Report().Print()