import ROOT
ROOT.EnableImplicitMT(16)
import pandas as pd



# see https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap
# see https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV

channels =  {
    "mc20_ggf_hyy"  : (4.852E+01 * 1e3, ["ntuples/mc20_ggf_hyy_stxs.root"]),
    "mc20_vbf_hyy"  : (3.779     * 1e3, ["ntuples/mc20_vbf_hyy_stxs.root"]),
    'mc20_wh_hyy'   : (1.369     * 1e3, ["ntuples/mc20_wph_hyy_stxs.root", "ntuples/mc20_wmh_hyy_stxs.root"]),
    'mc20_qqzh_hyy' : (0.8839    * 1e3, ["ntuples/mc20_qqzh_hyy_stxs.root"]),
    'mc20_tth_hyy'  : (0.5065    * 1e3, ["ntuples/mc20_tth_hyy_stxs.root"]),
    "mc23_ggf_hyy"  : (5.217E+01 * 1e3, ["ntuples/mc23_ggf_hyy_stxs.root"]),
    "mc23_vbf_hyy"  : (4.075     * 1e3, ["ntuples/mc23_vbf_hyy_stxs.root"]),
    'mc23_wh_hyy'   : (1.453     * 1e3, ["ntuples/mc23_wph_hyy_stxs.root", "ntuples/mc23_wmh_hyy_stxs.root"]),
    'mc23_qqzh_hyy' : (0.9422    * 1e3, ["ntuples/mc23_qqzh_hyy_stxs.root"]),
    'mc23_tth_hyy'  : (0.5688    * 1e3, ["ntuples/mc23_tth_hyy_stxs.root"]),
}

weights = [
    "hw_nominal",     # nominal MC weight.                  scalar
    "hw_alphaS_up",   # up alpha_s variaton for PHD4LHC;    scalar
    "hw_alphaS_dn",   # down alpha_s variaton for PHD4LHC;  scalar
    "hw_pdf4lhc_unc", # 30 Eigen variation for PHD4LHC      vector
    "hw_qcd",         # muR/muF variation for the given MC; vector
]

for channel, (xs, files) in channels.items():
    print(f"Processing channel {channel} with xs = {xs} fb and files = {files}")
    if 'wh' in channel or 'zh' in channel:
        print(f"  Applying additional filter for {channel} to select only events with hadronic/leptonic W/Z decays")
        sub_channes = {
            channel + '_lep' : 'HTXS_Stage1_Category_pTjet30 >= 300',
            channel + '_had' : 'HTXS_Stage1_Category_pTjet30 < 300',
        }
    else:
        sub_channes = {channel: '1'}
    for sub_channel, sub_channel_filter in sub_channes.items():
        dfs = {}
        dfs['all']      = ROOT.RDataFrame('tree', files)
        dfs['300pt']    = dfs['all'].Filter(sub_channel_filter).Filter("HTXS_Higgs_pt > 300e3")
        dfs['300pt450'] = dfs['all'].Filter(sub_channel_filter).Filter("HTXS_Higgs_pt > 300e3 && HTXS_Higgs_pt <= 450e3")
        dfs['450pt650'] = dfs['all'].Filter(sub_channel_filter).Filter("HTXS_Higgs_pt > 450e3 && HTXS_Higgs_pt <= 650e3")
        dfs['650pt']    = dfs['all'].Filter(sub_channel_filter).Filter("HTXS_Higgs_pt > 650e3")

        # len_hw_pdf4lhc_unc = set(dfs['all'].Range(10).Define('len_hw_pdf4lhc_unc', 'hw_pdf4lhc_unc.size()').AsNumpy(['len_hw_pdf4lhc_unc'])['len_hw_pdf4lhc_unc'])
        # len_hw_qcd         = set(dfs['all'].Range(10).Define('len_hw_qcd', 'hw_qcd.size()').AsNumpy(['len_hw_qcd'])['len_hw_qcd'])
        # assert (len(len_hw_pdf4lhc_unc) == 1 and len(len_hw_qcd) == 1)
        # len_hw_pdf4lhc_unc = list(len_hw_pdf4lhc_unc)[0]
        # len_hw_qcd         = list(len_hw_qcd)[0]
        
        if sub_channel.startswith("mc20"):
            len_hw_pdf4lhc_unc, len_hw_qcd = 30, 8
        elif sub_channel.startswith("mc23"):
            len_hw_pdf4lhc_unc, len_hw_qcd = 41, 8
        dfs['all'].Filter("hw_alphaS_up == hw_alphaS_up", 'hw_alphaS_up_not_nan').Report().Print()
        weight_dict = {}
        futures = []
        for slice, df in dfs.items():
            weight_dict[slice] = {}
            for weight in weights:
                if weight == "hw_pdf4lhc_unc":
                    for i in range(len_hw_pdf4lhc_unc):
                        weight_name = f"{weight}_{i}"
                        weight_dict[slice][weight_name] = df.Define(weight_name, f"{weight}.at({i})").Filter(f"{weight_name} == {weight_name}").Sum(weight_name)
                        futures.append(weight_dict[slice][weight_name])
                elif weight == "hw_qcd":
                    for i in range(len_hw_qcd):
                        weight_name = f"{weight}_{i}"
                        weight_dict[slice][weight_name] = df.Define(weight_name, f"{weight}.at({i})").Filter(f"{weight_name} == {weight_name}").Sum(weight_name)
                        futures.append(weight_dict[slice][weight_name])
                else:
                    weight_dict[slice][weight] = df.Filter(f"{weight} == {weight}").Sum(weight)
                    futures.append(weight_dict[slice][weight])
        ROOT.RDF.RunGraphs(futures)
        for slice, weight_sum_dict in weight_dict.items():
            for weight_name, weight_sum in weight_sum_dict.items():
                weight_dict[slice][weight_name] = weight_sum.GetValue()
        pdf = pd.DataFrame(weight_dict)
        pdf = pdf.apply(lambda row : (row / row['all']), axis=1)
        ratio_pdf = pdf.apply(lambda row : row / pdf.iloc[0], axis=1)
        pdf.columns = [col + '_acc' for col in pdf.columns]
        pdf[[col.split('_')[0] + '_xs' for col in pdf.columns]] = pdf.apply(lambda row : row * xs, axis=1)
        pdf = pd.concat([pdf, ratio_pdf.add_suffix('_ratio')], axis=1)
        pdf.to_csv(f"results/{sub_channel}.csv", index=True)