import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

import math

# ---------------------------------------------------------------------------
# T2cc  |  mStop = 850 GeV  |  DeltaM = 10 15 20 25 30 40 50 60 70 80
# 생성: work/fragments/make_fragments.py  (기준선 = McM 승인본 NPS-RunIII2024Summer24FSGenPremix-00007)
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
   1000006     %MSTOP%          # ~t_1
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
   1000021     1.00000000E+05    # ~g
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
DECAY   1000006     1.00000000E+00   # stop1 decays
    1.00000000E+00    2    1000022      4     # stop -> LSP + charm
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
DECAY   1000021     0.00000000E+00   # gluino decays
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

model = "T2cc"

# MLM matching scale. 승인본 표 그대로 (2026-08-14 결정: 상수가 아니라 mStop의 함수).
# 표가 topology와 무관한 이유: matching은 gridpack(hard process)과 shower 사이의 일이고 붕괴는 그 뒤라,
# T2cc/T2ttC/T2bWC가 같은 gridpack(SMS-StopStop, xqcut 30)을 쓰는 한 나눌 대상이 같다.
def matchParams(mass):
  if mass < 649: return 62., 0.274
  elif mass < 699: return 64., 0.269
  elif mass < 749: return 64., 0.269
  elif mass < 799: return 66., 0.259
  elif mass < 849: return 66., 0.261
  elif mass < 899: return 68., 0.257
  elif mass < 949: return 68., 0.252
  elif mass < 999: return 70., 0.250
  elif mass < 1049: return 70., 0.248
  elif mass < 1099: return 70., 0.248
  elif mass < 1149: return 70., 0.249
  elif mass < 1199: return 70., 0.242
  elif mass < 1249: return 70., 0.239
  elif mass < 1299: return 70., 0.242
  elif mass < 1349: return 70., 0.241
  elif mass < 1399: return 70., 0.237
  elif mass < 1449: return 70., 0.239
  elif mass < 1499: return 70., 0.241
  elif mass < 1549: return 70., 0.235
  elif mass < 1599: return 70., 0.239
  elif mass < 1649: return 70., 0.239
  elif mass < 1699: return 70., 0.237
  elif mass < 1749: return 70., 0.241
  elif mass < 1799: return 70., 0.237
  elif mass < 1849: return 70., 0.237
  elif mass < 1899: return 70., 0.240
  elif mass < 1949: return 70., 0.241
  elif mass < 1999: return 70., 0.244
  elif mass < 2049: return 70., 0.246
  elif mass < 2099: return 70., 0.249
  elif mass < 2149: return 70., 0.246
  elif mass < 2199: return 70., 0.246
  elif mass < 2249: return 70., 0.251
  elif mass < 2299: return 70., 0.249
  elif mass < 2349: return 70., 0.257
  elif mass < 2399: return 70., 0.257
  elif mass < 2449: return 70., 0.261
  elif mass < 2499: return 70., 0.264
  elif mass < 2549: return 70., 0.266
  ### Just for testing
  else: return 70., 0.243

# 이 request 가 담는 점 — 설계 축은 (mStop, DeltaM) 이고 mStop 은 이 파일에 고정이다.
# 점을 나열하지 않고 DeltaM 눈금으로 적는다: mLSP 만 나열하면 우리 설계 축인 DeltaM 이 안 보인다.
#
# DeltaM 눈금은 균등하지 않다 (<=30 은 step 5, 그 위는 step 10). 근거는 Run2 압축 stop 격자
# 실측이다 — T2bW_X05 / T2tt 4-body 의 Run2 생산 격자가 정확히 이 10 개 눈금을 썼다.
# 「어디를 촘촘히 볼지」는 eff(DeltaM) 곡선이 정하는데 그 곡선이 이 요청의 산출물이라
# 계산으로는 못 정한다 -> 자기순환을 깨는 것은 계산이 아니라 「그 격자로 실제 해 봤다」는 실증이다.
MSTOP = 850
DM_POINTS = [10, 15, 20, 25, 30, 40, 50, 60, 70, 80]

# 점당 이벤트 수 [k]. mStop 만의 함수라 이 request 안 모든 점이 같은 값을 받는다
# (= ConfigWeight 가 전부 같다 = 균등 분배). 그래서 이 값이 이 파일 안에서 가르는 것은 없고,
# 정하는 것은 Sum(wgt) = McM 에 적는 총량뿐이다.
# 값의 근거(goalLumi 400 · xsec · cap 1000k / floor 100k)는 이 파일 밖에 있다 — 요청 CSV 의
# events 칸과 발표의 grid justification 이 그 자리다.
NEV = 100

mpoints = [(MSTOP, MSTOP - dm, NEV) for dm in DM_POINTS]

qcut, tru_eff = matchParams(850)

# 미결 (2) 결정 (2026-08-15): tru_eff 는 리터럴로 박지 않고 위 표에서 받는다((b) 규칙).
#
#   mcm_eff = McM 입력칸에 신고하는 효율. 정의는 "이 request 전체의 최종/생성" 이고,
#   그래야 Sum(wgt) 가 우리가 원한 최종 이벤트 총합과 같아진다.
#   이 request 는 mStop 하나이고 표는 mStop 으로만 색인되므로, 안의 점들이 전부 같은
#   tru_eff 를 받는다 -> 전체 효율도 그 값 -> 비율이 1 이 되는 것이 구조상 정상이다.
#   (승인본 -00007 도 mStop 1050 하나뿐이라 mcm_eff = tru_eff = 0.248 로 비율이 1이다.
#    나눗셈 자체는 한 request 가 여러 mStop 을 담던 옛 구조의 잔재다.)
mcm_eff = tru_eff

# 이 표의 값은 승인본 저자들이 T2tt 를 돌려서 잰 것이다. 우리 topology(T2cc/T2ttC/T2bWC)와
# 압축 격자(DeltaM 10~80)에서도 같은지는 아직 모른다 -> private GEN 에서 직접 세어 갈아끼운다.
# 지금 이 값이 영향을 주는 곳은 McM 신고 효율(=생성량)뿐이고, ConfigWeight 와 격자 모양은
# 비율이 1 이라 이 값과 무관하다.

for mstop, mlsp, nev in mpoints:
    wgt = nev * (mcm_eff / tru_eff)
    if mlsp == 0:
        mlsp = 1

    slhatable = baseSLHATable.replace('%MSTOP%', '%e' % mstop)
    slhatable = slhatable.replace('%MLSP%',  '%e' % mlsp)

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
            'SLHA:allowOnlyOffShell = on',   # 압축 영역엔 on-shell 경로가 0개
            '24:mMin = 0.1',                 # W 샘플링 하한. 기본 10 이면 DeltaM 10 에서 붕괴가 꺼진다
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
            GridpackPath =  cms.string('/cvmfs/cms-griddata.cern.ch/phys_generator/gridpacks_tarball/pp/13p6TeV/madgraph/SMS-StopStop/SMS-StopStop_mStop-850_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'),
            ConfigDescription = cms.string('%s_%i_%i' % (model, mstop, mlsp)),
            SLHATableForPythia8 = cms.string('%s' % slhatable),
            PythiaParameters = basePythiaParameters,
        ),
    )

ProductionFilterSequence = cms.Sequence(generator)
