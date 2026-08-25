import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

import math

# ---------------------------------------------------------------------------
# T5ttcc  |  mGluino = 975 GeV  |  mLSP 5점: 775 ~ 865
# 생성: work/fragments/make_gluino_fragments.py
#   SLHA        <- Run2 승인본 frag_T5ttcc.py
#   generator   <- Run3 승인본 NPS-RunIII2024Summer24FSGenPremix-00007  (CP5 tune, comEnergy 13600)
#   matchParams <- Run2 승인본 (gluino 표)
# ---------------------------------------------------------------------------

baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     %MSTOP%   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     %MGLU%           # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     1.00000000E+05   # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     1.00000000E+05   # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   2000006     0.00000000E+00   # stop2 decays

DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     1.00000000E+00   # gluino decays
    0.00000000E+00    3    1000022     -1    1 # dummy allowed decay, in order to turn on off-shell decays
    0.5000000    2      1000006        -6
    0.5000000    2      -1000006        6

DECAY   1000006     1.00000000E+00   # stop1 decays
#          BR         NDA      ID1       ID2
         1.0000000    2     1000022        4
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     0.00000000E+00   # neutralino2 decays
DECAY   1000024     0.00000000E+00   # chargino1+ decays
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),
    RandomizedParameters = cms.VPSet(),
)

model = "T5ttcc"

# MLM matching scale. 승인본 표 그대로 (값을 풀어 적지 않는다 — 심사자가 승인본과 diff 대조 가능).
# ⚠ 이 표는 Run2 gluino gridpack 에서 잰 값이다. Run3 gridpack 은 다른 빌드라 계승 근거가
#    stop 만큼 정확히는 안 선다 -> 노드 6 (2) private GEN 에서 재서 갈아끼운다.
def matchParams(mass):
    if   mass<799: return 118., 0.235
    elif mass<999: return 128., 0.235
    elif mass<1199: return 140., 0.235
    elif mass<1399: return 143., 0.245
    elif mass<1499: return 147., 0.255
    elif mass<1799: return 150., 0.267
    elif mass<2099: return 156., 0.290
    elif mass<2301: return 160., 0.315
    elif mass<2601: return 162., 0.340
    elif mass<2851: return 168, 0.364
    else: return 160., 0.315

# 이 request 가 담는 점 — 설계 축은 (mGluino, mLSP) 이고 mGluino 는 이 파일에 고정이다.
# 점을 **나열**한다: 규칙으로 적으면 설계 축 mLSP 가 규칙 안에 숨는다.
# (stop 에서는 정반대였다 — 거기선 리터럴이 설계 축 DeltaM 을 숨겨서 규칙으로 적었다.)
MGLUINO = 975
MLSP_POINTS = [775, 800, 825, 850, 865]

# 점당 이벤트 수 [k]. mGluino 만의 함수라 이 request 안 모든 점이 같은 값을 받는다
# (= ConfigWeight 가 전부 같다 = 균등 분배). 정하는 것은 Sum(wgt) = McM 에 적는 총량뿐이다.
NEV = 232

mpoints = [(MGLUINO, mlsp, NEV) for mlsp in MLSP_POINTS]

qcut, tru_eff = matchParams(975)

# 이 request 는 mGluino 하나이고 표는 mGluino 로만 색인되므로, 안의 점들이 전부 같은
# tru_eff 를 받는다 -> 전체 효율도 그 값 -> 비율이 1 이 되는 것이 구조상 정상이다.
mcm_eff = tru_eff

for mglu, mlsp, nev in mpoints:
    wgt = nev * (mcm_eff / tru_eff)
    if mlsp == 0:
        mlsp = 1

    slhatable = baseSLHATable.replace('%MGLU%', '%e' % mglu)
    slhatable = slhatable.replace('%MLSP%', '%e' % mlsp)
    slhatable = slhatable.replace('%MSTOP%', '%e' % (mlsp + 20.))

    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '6:m0 = 172.5',
            'Check:abortIfVeto = on',
            'TauDecays:externalMode=2',
            '24:mMin = 0.1',                 # W 샘플링 하한. 기본 10 이면 chargino(mLSP+5) 붕괴가 꺼진다
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
    )
    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(wgt),
            GridpackPath =  cms.string('/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUSY_SMS/SMS-GlGl/SMS-GlGl_mGl-975_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'),
            ConfigDescription = cms.string('%s_%i_%i' % (model, mglu, mlsp)),
            SLHATableForPythia8 = cms.string('%s' % slhatable),
            PythiaParameters = basePythiaParameters,
        ),
    )

ProductionFilterSequence = cms.Sequence(generator)
