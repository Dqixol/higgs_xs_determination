#pragma once

#include <TLorentzVector.h>
#include <TruthWeightTools/IHiggsWeightTool.h>
#include <TruthWeightTools/HiggsWeightTool.h>
#include <TruthWeightTools/HiggsWeights.h>

// namespace TruthWeightTools {
//     class HiggsWeights;
//     class IHiggsWeightTool;
//     class HiggsWeightTool;
// }

TLorentzVector getTruthHiggsP4(const xAOD::TruthParticleContainer& particles){
    for (auto particle : particles){
        if (std::abs(particle->pdgId()) == 25 and particle->status() == 62){ // see https://pythia.org/latest-manual/ParticleProperties.html
            return particle->p4();
        }
    }
    return TLorentzVector();
}

std::vector<TLorentzVector> getTruthPhotonsP4(const xAOD::TruthParticleContainer& particles){
    std::vector<TLorentzVector> photons;
    for (auto particle : particles){
        if (std::abs(particle->pdgId()) == 22){ // see https://pythia.org/latest-manual/ParticleProperties.html
            photons.push_back(particle->p4());
        }
    }
    if (photons.size() != 2){
        std::cout << "ERROR: expected 2 photons, but found " << photons.size() << std::endl;
        assert (photons.size() == 2);
    }
    return photons;
}

int printTruthParticles(const xAOD::TruthParticleContainer& particles){
    std::cout << "particles: " << particles.size() << std::endl;
    int count = 0;
    for (auto particle : particles){
        std::cout << "    pdgId: " << particle->pdgId() << ", status: " << particle->status() << ", pt: " << particle->p4().Pt() / 1000. << std::endl;
        count++;
    }
    auto photons = getTruthPhotonsP4(particles);
    std::cout << "    pT_yy: " << (photons[0] + photons[1]).Pt() / 1000. << std::endl;
    return count;
}

TruthWeightTools::HiggsWeights getHiggsWeights(const xAOD::EventInfo& eventInfo, TruthWeightTools::HiggsWeightTool* tool){
    int HTXS_Njets30        = eventInfo.auxdata<int>("HTXS_Njets_pTjet30");
    int HTXS_Stage1         = eventInfo.auxdata<int>("HTXS_Stage1_Category_pTjet30");
    double HTXS_pTH         = eventInfo.auxdata<float>("HTXS_Higgs_pt"); // Needs to be in MeV
    int HTXS_Stage1p2       = eventInfo.auxdata<int>("HTXS_Stage1_2_Category_pTjet30");
    int HTXS_Stage1p2Fine   = eventInfo.auxdata<int>("HTXS_Stage1_2_Fine_Category_pTjet30");

    // Access all Higgs weights
    TruthWeightTools::HiggsWeights hw = tool->getHiggsWeights(
        HTXS_Njets30, 
        HTXS_pTH, 
        HTXS_Stage1, 
        HTXS_Stage1p2, 
        HTXS_Stage1p2Fine, 
        &eventInfo
    );
    return hw;
}