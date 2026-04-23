# Single Higgs STXS acceptance determination 

This repository provides a lightweight analysis workflow for deriving Higgs production cross-section in STXS bins from ATLAS Monte Carlo samples in the diphoton final state. The reason for using the di-photon samples is that it's un-filtered. In its present form, the code focuses on extracting STXS truth information and theory weights from DAOD-derived samples, producing ntuples, and evaluating acceptance and cross-section summaries for STXS stage 1.2 fine categories.


## How to Use This Repository (require ATLAS environment)

To set up the environment, build the `TruthWeightTools` [1] package, and produce the reduced ntuples, execute the following commands from the repository root:

```bash
setupATLAS
asetup --stable AnalysisBase,25.2,latest 
rm -rf build
mkdir build
cd build
cmake ../source_hwt
make
cd ..
source build/*/setup.sh
bash ntupleProd.sh
```

## Sample retrieval

The file `data/samples` contains example `rucio get` commands for several of the production modes relevant to this repository. The full list of samples can be found in the same file. 

```
ggF:
mc23_13p6TeV.602421.PhPy8EG_PDF4LHC21_ggH_NNLOPS_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017
mc20_13TeV.343981.PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_gamgam.deriv.DAOD_PHYS.e5607_s3681_r13145_p7018 

VBFH:
mc23_13p6TeV.601482.PhPy8EG_PDF4LHC21_VBFH125_gammagamma.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017
mc20_13TeV.346214.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_gamgam.deriv.DAOD_PHYS.e6970_s3681_r13145_p7018

VH:
mc23_13p6TeV.601523.PhPy8EG_PDF4LHC21_ZH125J_Zincl_MINLO_gammagamma.deriv.DAOD_PHYS.e8559_s4162_r14622_p7017
mc23_13p6TeV.601483.PhPy8EG_PDF4LHC21_WmH125J_Wincl_MINLO_gammagamma.deriv.DAOD_PHYS.e8559_a934_r16083_p7017
mc23_13p6TeV.601484.PhPy8EG_PDF4LHC21_WpH125J_Wincl_MINLO_gammagamma.deriv.DAOD_PHYS.e8559_a934_r16083_p7017

mc20_13TeV.345317.PowhegPythia8EvtGen_NNPDF30_AZNLO_WmH125J_Hyy_Wincl_MINLO.deriv.DAOD_PHYS.e5734_s3681_r13145_p7018
mc20_13TeV.345318.PowhegPythia8EvtGen_NNPDF30_AZNLO_WpH125J_Hyy_Wincl_MINLO.deriv.DAOD_PHYS.e5734_s3681_r13145_p7018
mc20_13TeV.345319.PowhegPythia8EvtGen_NNPDF30_AZNLO_ZH125J_Hyy_Zincl_MINLO.deriv.DAOD_PHYS.e5743_s3681_r13145_p7018

ttH:
mc23_13p6TeV:mc23_13p6TeV.602422.PhPy8EG_PDF4LHC21_ttH125_tincl_gammagamma_1file.deriv.DAOD_PHYS.e8559_s4369_r16083_p7017
mc20_13TeV:mc20_13TeV.346525.PowhegPythia8EvtGen_A14NNPDF23_NNPDF30ME_ttH125_gamgam.deriv.DAOD_PHYS.e7488_s3681_r13145_p7018
```

## Details
1. The DAOD_PHYS samples used in this repository is un-skimmed, meaning that all generated events are retained, no cuts are applied at reconstruction level, and all truth information is preserved. 
2. STXS information is stored in the `EventInfo` container, calculated from the central rivet routine [2-3], retrievable in DAOD_PHYS via:
```python
htxs_categories_to_save = {
    "HTXS_Njets_pTjet30"                  : "int"  ,        
    "HTXS_Stage1_Category_pTjet30"        : "int"  ,                
    "HTXS_Higgs_pt"                       : "float",      
    "HTXS_Stage1_2_Category_pTjet30"      : "int"  ,                    
    "HTXS_Stage1_2_Fine_Category_pTjet30" : "int"  ,                        
}
for cata, dtype in htxs_categories_to_save.items():
    df = df.Define(cata, f'EventInfo.auxdataConst<{dtype}>  ("{cata}")')
```
3. The `TruthWeightTools` [1] package provides a convenient way to retrieve theory weights for each event, which can be used to evaluate the theory uncertainties on the acceptance and cross-section measurements. The uncertainties considered are the 30 (Run 2) or 41 (Run 3) PDF4LHC eigen variations, the up and down alpha_s variations, and the muR/muF QCD scale variations.

This tool provide a nice interface for that, accessible via:
```python
weights_to_save = [
    "hw_nominal",     # nominal MC weight
    "hw_pdf4lhc_unc", # 30 Eigen variation for PHD4LHC
    "hw_alphaS_up",   # up alpha_s variaton for PHD4LHC
    "hw_alphaS_dn",   # down alpha_s variaton for PHD4LHC
    "hw_qcd",         # muR/muF variation for the given MC
]
for weight_name in weights_to_save:
    df = df.Define(weight_name, weight_name.replace("hw_", "hw."))
```

## References

- [1] HiggsWeightTools: https://gitlab.cern.ch/atlas_higgs_combination/software/TruthWeightTools
- [2] Rivet call in athena: https://gitlab.cern.ch/atlas/athena/-/blob/main/Generators/TruthRivetTools/Root/HiggsTruthCategoryTool.cxx
- [3] Rivet routine: https://gitlab.cern.ch/atlas/athena/-/blob/main/Generators/TruthRivetTools/TruthRivetTools/HiggsTemplateCrossSections.h
- [?] ATLAS-CMS Run 2 comparison: https://indico.cern.ch/event/1619272/\#3-information-on-stxs-acceptan
- [?] Twiki:  https://twiki.cern.ch/twiki/bin/view/AtlasProtected/StxsAcceptanceStudy
- [?] Run 2 ATLAS numbers: https://gitlab.cern.ch/lhc-hcg/Run-2/couplings/atlas/-/blob/master/Acceptances/stage1_2_acc.yaml
