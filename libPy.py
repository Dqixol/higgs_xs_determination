import ROOT

def getHiggsWeightTool(df, channel):
    hwt = ROOT.TruthWeightTools.HiggsWeightTool( f"HiggsWeightTool_{channel}" )
    if 'vbf' in channel:
        hwt.setProperty( "ProdMode", "VBF"  )
    elif 'ggf' in channel:
        hwt.setProperty( "RequireFinite", True )
        hwt.setProperty( "WeightCutOff", 100.0 )
        hwt.setProperty( "ProdMode", "ggF" )
    elif 'wph' in channel or 'wmh' in channel:
        hwt.setProperty( "ProdMode", "WH" )
    elif 'qqzh' in channel:
        hwt.setProperty( "ProdMode", "qqZH" )
    elif 'ggzh' in channel:
        hwt.setProperty( "ProdMode", "ggZH" )
    elif 'tth' in channel:
        hwt.setProperty( "ProdMode", "ttH" )
    hwt.initialize()
    hwt_ptr = ROOT.addressof(hwt)
    df = df.Define('hwt', f'''
        auto ret = reinterpret_cast<TruthWeightTools::HiggsWeightTool*>({hwt_ptr});
        return ret;
    ''')
    return df, hwt

official_1_2_fine = {
    'ggf' : {
        'gg2H_0J_ptH_0_10' : 13.6786,
        'gg2H_0J_ptH_gt10' : 42.5421,
        'gg2H_1J_ptH_0_60' : 13.3944,
        'gg2H_1J_ptH_60_120' : 9.26889,
        'gg2H_1J_ptH_120_200' : 1.53245,
        'gg2H_ge2J_mJJ_0_350_ptH_0_60_ptHJJ_0_25' : 1.33049,
        'gg2H_ge2J_mJJ_0_350_ptH_60_120_ptHJJ_0_25' : 1.96731,
        'gg2H_ge2J_mJJ_0_350_ptH_120_200_ptHJJ_0_25' : 0.718604,
        'gg2H_ge2J_mJJ_0_350_ptH_0_60_ptHJJ_gt25' : 1.06841,
        'gg2H_ge2J_mJJ_0_350_ptH_60_120_ptHJJ_gt25' : 1.69202,
        'gg2H_ge2J_mJJ_0_350_ptH_120_200_ptHJJ_gt25' : 1.1717,
        'gg2H_ge2J_mJJ_350_700_ptH_0_200_ptHJJ_0_25' : 0.514373,
        'gg2H_ge2J_mJJ_350_700_ptH_0_200_ptHJJ_gt25' : 0.732746,
        'gg2H_ge2J_mJJ_700_1000_ptH_0_200_ptHJJ_0_25' : 0.116985,
        'gg2H_ge2J_mJJ_700_1000_ptH_0_200_ptHJJ_gt25' : 0.177777,
        'gg2H_ge2J_mJJ_1000_1500_ptH_0_200_ptHJJ_0_25' : 0.06526,
        'gg2H_ge2J_mJJ_1000_1500_ptH_0_200_ptHJJ_gt25' : 0.0997468,
        'gg2H_ge2J_mJJ_gt1500_ptH_0_200_ptHJJ_0_25' : 0.0338097,
        'gg2H_ge2J_mJJ_gt1500_ptH_0_200_ptHJJ_gt25' : 0.0499217,
        'gg2H_ptH_200_300_ptHJoverptH_0_15' : 0.214378,
        'gg2H_ptH_300_450_ptHJoverptH_0_15' : 0.0604692,
        'gg2H_ptH_450_650_ptHJoverptH_0_15' : 0.0102872,
        'gg2H_ptH_gt650_ptHJoverptH_0_15' : 0.00148133,
        'gg2H_ptH_200_300_ptHJoverptH_gt15' : 0.709168,
        'gg2H_ptH_300_450_ptHJoverptH_gt15' : 0.154693,
        'gg2H_ptH_450_650_ptHJoverptH_gt15' : 0.0218401,
        'gg2H_ptH_gt650_ptHJoverptH_gt15' : 0.00301522,
        'gg2H_fwdH' : 8.66908,
    },
}

stage_1_2_fine = {
    'ggf' : {
        100 : 'GG2H_FWDH',
        101 : 'GG2H_PTH_200_300_PTHJoverPTH_0_15',
        102 : 'GG2H_PTH_300_450_PTHJoverPTH_0_15',
        103 : 'GG2H_PTH_450_650_PTHJoverPTH_0_15',
        104 : 'GG2H_PTH_GT650_PTHJoverPTH_0_15',
        105 : 'GG2H_PTH_200_300_PTHJoverPTH_GT15',
        106 : 'GG2H_PTH_300_450_PTHJoverPTH_GT15',
        107 : 'GG2H_PTH_450_650_PTHJoverPTH_GT15',
        108 : 'GG2H_PTH_GT650_PTHJoverPTH_GT15',
        109 : 'GG2H_0J_PTH_0_10',
        110 : 'GG2H_0J_PTH_GT10',
        111 : 'GG2H_1J_PTH_0_60',
        112 : 'GG2H_1J_PTH_60_120',
        113 : 'GG2H_1J_PTH_120_200',
        114 : 'GG2H_GE2J_MJJ_0_350_PTH_0_60_PTHJJ_0_25',
        115 : 'GG2H_GE2J_MJJ_0_350_PTH_60_120_PTHJJ_0_25',
        116 : 'GG2H_GE2J_MJJ_0_350_PTH_120_200_PTHJJ_0_25',
        117 : 'GG2H_GE2J_MJJ_0_350_PTH_0_60_PTHJJ_GT25',
        118 : 'GG2H_GE2J_MJJ_0_350_PTH_60_120_PTHJJ_GT25',
        119 : 'GG2H_GE2J_MJJ_0_350_PTH_120_200_PTHJJ_GT25',
        120 : 'GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25',
        121 : 'GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25',
        122 : 'GG2H_GE2J_MJJ_700_1000_PTH_0_200_PTHJJ_0_25',
        123 : 'GG2H_GE2J_MJJ_700_1000_PTH_0_200_PTHJJ_GT25',
        124 : 'GG2H_GE2J_MJJ_1000_1500_PTH_0_200_PTHJJ_0_25',
        125 : 'GG2H_GE2J_MJJ_1000_1500_PTH_0_200_PTHJJ_GT25',
        126 : 'GG2H_GE2J_MJJ_GT1500_PTH_0_200_PTHJJ_0_25',
        127 : 'GG2H_GE2J_MJJ_GT1500_PTH_0_200_PTHJJ_GT25',
    },
    'vbf'  : {
        200 : 'QQ2HQQ_FWDH',
        201 : 'QQ2HQQ_0J',
        202 : 'QQ2HQQ_1J',
        203 : 'QQ2HQQ_GE2J_MJJ_0_60_PTHJJ_0_25',
        204 : 'QQ2HQQ_GE2J_MJJ_60_120_PTHJJ_0_25',
        205 : 'QQ2HQQ_GE2J_MJJ_120_350_PTHJJ_0_25',
        206 : 'QQ2HQQ_GE2J_MJJ_0_60_PTHJJ_GT25',
        207 : 'QQ2HQQ_GE2J_MJJ_60_120_PTHJJ_GT25',
        208 : 'QQ2HQQ_GE2J_MJJ_120_350_PTHJJ_GT25',
        209 : 'QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25',
        210 : 'QQ2HQQ_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25',
        211 : 'QQ2HQQ_GE2J_MJJ_700_1000_PTH_0_200_PTHJJ_0_25',
        212 : 'QQ2HQQ_GE2J_MJJ_700_1000_PTH_0_200_PTHJJ_GT25',
        213 : 'QQ2HQQ_GE2J_MJJ_1000_1500_PTH_0_200_PTHJJ_0_25',
        214 : 'QQ2HQQ_GE2J_MJJ_1000_1500_PTH_0_200_PTHJJ_GT25',
        215 : 'QQ2HQQ_GE2J_MJJ_GT1500_PTH_0_200_PTHJJ_0_25',
        216 : 'QQ2HQQ_GE2J_MJJ_GT1500_PTH_0_200_PTHJJ_GT25',
        217 : 'QQ2HQQ_GE2J_MJJ_350_700_PTH_GT200_PTHJJ_0_25',
        218 : 'QQ2HQQ_GE2J_MJJ_350_700_PTH_GT200_PTHJJ_GT25',
        219 : 'QQ2HQQ_GE2J_MJJ_700_1000_PTH_GT200_PTHJJ_0_25',
        220 : 'QQ2HQQ_GE2J_MJJ_700_1000_PTH_GT200_PTHJJ_GT25',
        221 : 'QQ2HQQ_GE2J_MJJ_1000_1500_PTH_GT200_PTHJJ_0_25',
        222 : 'QQ2HQQ_GE2J_MJJ_1000_1500_PTH_GT200_PTHJJ_GT25',
        223 : 'QQ2HQQ_GE2J_MJJ_GT1500_PTH_GT200_PTHJJ_0_25',
        224 : 'QQ2HQQ_GE2J_MJJ_GT1500_PTH_GT200_PTHJJ_GT25',
    },
    'wh'   : {
        300 : 'QQ2HLNU_FWDH',
        301 : 'QQ2HLNU_PTV_0_75_0J',
        302 : 'QQ2HLNU_PTV_75_150_0J',
        303 : 'QQ2HLNU_PTV_150_250_0J',
        304 : 'QQ2HLNU_PTV_250_400_0J',
        305 : 'QQ2HLNU_PTV_GT400_0J',
        306 : 'QQ2HLNU_PTV_0_75_1J',
        307 : 'QQ2HLNU_PTV_75_150_1J',
        308 : 'QQ2HLNU_PTV_150_250_1J',
        309 : 'QQ2HLNU_PTV_250_400_1J',
        310 : 'QQ2HLNU_PTV_GT400_1J',
        311 : 'QQ2HLNU_PTV_0_75_GE2J',
        312 : 'QQ2HLNU_PTV_75_150_GE2J',
        313 : 'QQ2HLNU_PTV_150_250_GE2J',
        314 : 'QQ2HLNU_PTV_250_400_GE2J',
        315 : 'QQ2HLNU_PTV_GT400_GE2J',
    },
    'qqzh' : {
        400 : 'QQ2HLL_FWDH',
        401 : 'QQ2HLL_PTV_0_75_0J',
        402 : 'QQ2HLL_PTV_75_150_0J',
        403 : 'QQ2HLL_PTV_150_250_0J',
        404 : 'QQ2HLL_PTV_250_400_0J',
        405 : 'QQ2HLL_PTV_GT400_0J',
        406 : 'QQ2HLL_PTV_0_75_1J',
        407 : 'QQ2HLL_PTV_75_150_1J',
        408 : 'QQ2HLL_PTV_150_250_1J',
        409 : 'QQ2HLL_PTV_250_400_1J',
        410 : 'QQ2HLL_PTV_GT400_1J',
        411 : 'QQ2HLL_PTV_0_75_GE2J',
        412 : 'QQ2HLL_PTV_75_150_GE2J',
        413 : 'QQ2HLL_PTV_150_250_GE2J',
        414 : 'QQ2HLL_PTV_250_400_GE2J',
        415 : 'QQ2HLL_PTV_GT400_GE2J',
    },
    'ggzh' : {
        500 : 'GG2HLL_FWDH',
        501 : 'GG2HLL_PTV_0_75_0J',
        502 : 'GG2HLL_PTV_75_150_0J',
        503 : 'GG2HLL_PTV_150_250_0J',
        504 : 'GG2HLL_PTV_250_400_0J',
        505 : 'GG2HLL_PTV_GT400_0J',
        506 : 'GG2HLL_PTV_0_75_1J',
        507 : 'GG2HLL_PTV_75_150_1J',
        508 : 'GG2HLL_PTV_150_250_1J',
        509 : 'GG2HLL_PTV_250_400_1J',
        510 : 'GG2HLL_PTV_GT400_1J',
        511 : 'GG2HLL_PTV_0_75_GE2J',
        512 : 'GG2HLL_PTV_75_150_GE2J',
        513 : 'GG2HLL_PTV_150_250_GE2J',
        514 : 'GG2HLL_PTV_250_400_GE2J',
        515 : 'GG2HLL_PTV_GT400_GE2J',
    },
    'tth'  : {
        600 : 'TTH_FWDH', 
        601 : 'TTH_PTH_0_60',
        602 : 'TTH_PTH_60_120',
        603 : 'TTH_PTH_120_200',
        604 : 'TTH_PTH_200_300',
        605 : 'TTH_PTH_300_450',
        606 : 'TTH_PTH_GT450',
    },
    'bbh'  : {
        700 : 'BBH_FWDH', 
        701 : 'BBH',
    },
    'th'   : {
        800 : 'TH_FWDH', 
        801 : 'TH'
    },
}