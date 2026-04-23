rm -rf logs/*
nohup python ntupler.py --channel mc23_ggf_hyy > logs/mc23_ggf_hyy.log 2>&1 &
nohup python ntupler.py --channel mc23_vbf_hyy > logs/mc23_vbf_hyy.log 2>&1 &
nohup python ntupler.py --channel mc23_qqzh_hyy > logs/mc23_qqzh_hyy.log 2>&1 &
nohup python ntupler.py --channel mc23_ggzh_hyy > logs/mc23_ggzh_hyy.log 2>&1 &
nohup python ntupler.py --channel mc23_wmh_hyy > logs/mc23_wmh_hyy.log 2>&1 &
nohup python ntupler.py --channel mc23_wph_hyy > logs/mc23_wph_hyy.log 2>&1 &
nohup python ntupler.py --channel mc23_tth_hyy > logs/mc23_tth_hyy.log 2>&1 &

nohup python ntupler.py --channel mc20_ggf_hyy > logs/mc20_ggf_hyy.log 2>&1 &
nohup python ntupler.py --channel mc20_vbf_hyy > logs/mc20_vbf_hyy.log 2>&1 &
nohup python ntupler.py --channel mc20_qqzh_hyy > logs/mc20_qqzh_hyy.log 2>&1 &
nohup python ntupler.py --channel mc20_ggzh_hyy > logs/mc20_ggzh_hyy.log 2>&1 &
nohup python ntupler.py --channel mc20_wmh_hyy > logs/mc20_wmh_hyy.log 2>&1 &
nohup python ntupler.py --channel mc20_wph_hyy > logs/mc20_wph_hyy.log 2>&1 &
nohup python ntupler.py --channel mc20_tth_hyy > logs/mc20_tth_hyy.log 2>&1 &