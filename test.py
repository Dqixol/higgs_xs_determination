print("Warming up...")
import ROOT
import glob
ROOT.gROOT.SetBatch()

ROOT.xAOD.Init()
ROOT.xAOD.JetContainer()
ROOT.xAOD.TauJetContainer()
ROOT.xAOD.MuonContainer()
ROOT.xAOD.ElectronContainer()
ROOT.xAOD.EventInfo()
ROOT.gInterpreter.Declare('#include "libPhys.h"')

from xAODDataSource import Helpers
print("Done setting up libraries, running...")

# mc20e_ggf_hyy
f = glob.glob("mc20_13TeV.343981.PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_gamgam.deriv.DAOD_PHYS.e5607_s3681_r13145_p7018/*.root.1")[:1]

df = Helpers.MakexAODDataFrame(f)
df = df.Range(0, 10)
df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
df = df.Define("tmp", "printTruthParticles(TruthBosonsWithDecayParticles)")
df.Histo1D("tmp", "tmp").GetValue()