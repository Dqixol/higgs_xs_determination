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
channels = [channel for channel in channels if 'vbf_hyy' in channel]

# for wrights used see: https://gitlab.cern.ch/atlas_higgs_combination/software/TruthWeightTools/blob/master/Root/HiggsWeightTool.cxx#L131
weight_signatures = {
    "mc20e_ggf_hyy": "nnlo",
    "mc23e_ggf_hyy": "nnlo",
    "mc23e_vbf_hyy": "nominal",
    "mc20e_vbf_hyy": "90400",
}

for channel in channels:
    print(f"Processing {channel}...")
    if channel == "mc20e_ggf_hyy":
        f = glob.glob("mc20_13TeV.343981.PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_gamgam.deriv.DAOD_PHYS.e5607_s3681_r13145_p7018/*.root.1")
    elif channel == "mc23e_vbf_hyy":
        f = glob.glob("mc23_13p6TeV.601482.PhPy8EG_PDF4LHC21_VBFH125_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017/*.root.1")
    elif channel == "mc20e_vbf_hyy":
        f = glob.glob("mc20_13TeV.346214.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_gamgam.deriv.DAOD_PHYS.e6970_s3681_r13145_p7018/*.root.1")
    elif channel == "mc23e_ggf_hyy":
        f = glob.glob("mc23_13p6TeV.602421.PhPy8EG_PDF4LHC21_ggH_NNLOPS_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017/*.root.1")
    df = Helpers.MakexAODDataFrame(f)

    twt = ROOT.PMGTools.PMGTruthWeightTool(f'truth_weight_tool_{channel}')
    twt.initialize()
    weight_names = [str(weight_name) for weight_name in twt.getWeightNames() if weight_signatures[channel] in weight_name]
    column_names = [weight_name.strip().replace('-', '_').replace(' ', '_').replace('.', 'p').replace(':', '_').replace('=', '_').replace(',', '_') for weight_name in weight_names]
    print("Saving weights:")
    print(weight_names)

    twt_ptr = ROOT.addressof(twt)

    df = df.Define('twt', f'''
        auto ret = reinterpret_cast<PMGTools::PMGTruthWeightTool*>({twt_ptr});
        return ret;
    ''')

    df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
    for weight_name, column_name in zip(weight_names, column_names):
        df = df.Define(column_name, f'twt->getWeight(&EventInfo, "{weight_name}")')

    df = df.Filter("TruthBosonsWithDecayParticles.size() >= 3", "TruthBosonsWithDecayParticles.size() >= 3")
    df = df.Define("Higgs_p4", "getTruthHiggsP4(TruthBosonsWithDecayParticles)")
    df = df.Define("Photons_p4", "getTruthPhotonsP4(TruthBosonsWithDecayParticles)")
    df = df.Define("photon1_p4", "Photons_p4[0]")
    df = df.Define("photon2_p4", "Photons_p4[1]")
    df.Snapshot(channel, f"{channel}.root", ["Higgs_p4", "photon1_p4", "photon2_p4"] + column_names)
    df.Report().Print()