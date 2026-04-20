
import ROOT
ROOT.EnableImplicitMT(16)
import pandas as pd
import libPy

channels =  {
    "mc20_ggf_hyy"  : ["ntuples/mc20_ggf_hyy_stxs.root"],
    "mc20_vbf_hyy"  : ["ntuples/mc20_vbf_hyy_stxs.root"],
    'mc20_wh_hyy'   : ["ntuples/mc20_wph_hyy_stxs.root", "ntuples/mc20_wmh_hyy_stxs.root"],
    'mc20_qqzh_hyy' : ["ntuples/mc20_qqzh_hyy_stxs.root"],
    'mc20_ggzh_hyy' : ["ntuples/mc20_ggzh_hyy_stxs.root"],
    'mc20_tth_hyy'  : ["ntuples/mc20_tth_hyy_stxs.root"],
    "mc23_ggf_hyy"  : ["ntuples/mc23_ggf_hyy_stxs.root"],
    "mc23_vbf_hyy"  : ["ntuples/mc23_vbf_hyy_stxs.root"],
    'mc23_wh_hyy'   : ["ntuples/mc23_wph_hyy_stxs.root", "ntuples/mc23_wmh_hyy_stxs.root"],
    'mc23_qqzh_hyy' : ["ntuples/mc23_qqzh_hyy_stxs.root"],
    'mc23_ggzh_hyy' : ["ntuples/mc23_ggzh_hyy_stxs.root"],
    'mc23_tth_hyy'  : ["ntuples/mc23_tth_hyy_stxs.root"],
}

stxs_broad_categories = {
    "mc20_ggf_hyy"  : ['ggf'],
    "mc20_vbf_hyy"  : ['vbf'],
    'mc20_wh_hyy'   : ['wh', 'vbf'],
    'mc20_qqzh_hyy' : ['qqzh', 'vbf'],
    'mc20_ggzh_hyy' : ['ggzh', 'ggf'],
    'mc20_tth_hyy'  : ['tth'],
    "mc23_ggf_hyy"  : ['ggf'],
    "mc23_vbf_hyy"  : ['vbf'],
    'mc23_wh_hyy'   : ['wh', 'vbf'],
    'mc23_qqzh_hyy' : ['qqzh', 'vbf'],
    'mc23_ggzh_hyy' : ['ggzh', 'ggf'],
    'mc23_tth_hyy'  : ['tth'],
}

weights = [
    "hw_nominal",     # nominal MC weight.                  scalar
    "hw_alphaS_up",   # up alpha_s variaton for PHD4LHC;    scalar
    "hw_alphaS_dn",   # down alpha_s variaton for PHD4LHC;  scalar
    "hw_pdf4lhc_unc", # 30 Eigen variation for PHD4LHC      vector
    "hw_qcd",         # muR/muF variation for the given MC; vector
]
for channel, files in channels.items():
    dfs = {}
    dfs['ALL']      = ROOT.RDataFrame("tree", files)
    dfs['UNKNOWN']  = dfs['ALL'].Filter("HTXS_Stage1_2_Fine_Category_pTjet30 == 0")
    for broad_category in stxs_broad_categories[channel]:
        for val, category in libPy.stage_1_2_fine[broad_category].items():
            dfs[category] = dfs['ALL'].Filter(f"HTXS_Stage1_2_Fine_Category_pTjet30 == {val}")
    if channel.startswith("mc20"):
        len_hw_pdf4lhc_unc, len_hw_qcd = 30, 8
    else:
        len_hw_pdf4lhc_unc, len_hw_qcd = 41, 8

    weight_dict = {}
    futures = []
    for slice, df in dfs.items():
        weight_dict[slice] = {}
        for weight in weights:
            if weight == "hw_pdf4lhc_unc":
                for i in range(len_hw_pdf4lhc_unc):
                    weight_name = f"{weight}_{i}"
                    tmp_df = df.Define(weight_name, f"{weight}.at({i})").Filter(f"{weight_name} == {weight_name}")
                    weight_dict[slice][weight_name] = tmp_df.Sum(weight_name)
                    weight_dict[slice][f"{weight_name}_error"] = tmp_df.Define(f"{weight_name}_squared", f"{weight_name}*{weight_name}").Sum(f"{weight_name}_squared")
                    futures.append(weight_dict[slice][weight_name])
                    futures.append(weight_dict[slice][f"{weight_name}_error"])
            elif weight == "hw_qcd":
                for i in range(len_hw_qcd):
                    weight_name = f"{weight}_{i}"
                    tmp_df = df.Define(weight_name, f"{weight}.at({i})").Filter(f"{weight_name} == {weight_name}")
                    weight_dict[slice][weight_name] = tmp_df.Sum(weight_name)
                    weight_dict[slice][f"{weight_name}_error"] = tmp_df.Define(f"{weight_name}_squared", f"{weight_name}*{weight_name}").Sum(f"{weight_name}_squared")
                    futures.append(weight_dict[slice][weight_name])
                    futures.append(weight_dict[slice][f"{weight_name}_error"])
            else:
                tmp_df = df.Filter(f"{weight} == {weight}")
                weight_dict[slice][weight] = tmp_df.Sum(weight)
                weight_dict[slice][f"{weight}_error"] = tmp_df.Define(f"{weight}_squared", f"{weight}*{weight}").Sum(f"{weight}_squared")
                futures.append(weight_dict[slice][weight])
                futures.append(weight_dict[slice][f"{weight}_error"])
    ROOT.RDF.RunGraphs(futures)

    calc_dict = {}
    for slice, weight_sum_dict in weight_dict.items():
        calc_dict[slice] = {}
        for key, future in weight_sum_dict.items():
            if key.endswith("_error"):
                calc_dict[slice][key] = future.GetValue()**0.5
            else:
                calc_dict[slice][key] = future.GetValue()


    pdf = pd.DataFrame(calc_dict)
    pdf_values = pdf.loc[~pdf.index.str.endswith("_error")]
    pdf_error = pdf.loc[pdf.index.str.endswith("_error")]
    pdf_error.index = pdf_error.index.str.replace("_error", "")
    pdf_error = pdf_error.apply(lambda row : (row / pdf_values.loc[row.name]), axis=1)
    pdf_values = pdf_values.apply(lambda row : (row / row['ALL']), axis=1)
    pdf_error = pdf_error.apply(lambda row : row * pdf_values.loc[row.name], axis=1)
    pdf_values.to_csv(f"res_stxs/{channel}.csv", index=True)
    pdf_error.to_csv(f"res_stxs/{channel}_error.csv", index=True)