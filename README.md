# Run3 NPS Stop SMS sample requests

Fragments and gridpacks for the NPS stop-search signal (SMS) sample production
request (Run 3, 13.6 TeV) — 6 topologies:
**T2cc, T2ttC, T2bWC** (stop, compressed region) and **T1tttt, T1ttbb, T5ttcc**
(gluino).

## Contents
- `fragments/stop/` — 57 fragments (mStop 300–1200, step 50 × 3 topologies)
- `fragments/gluino/` — 158 fragments (mGluino scan × 3 topologies)
- `gridpacks/` — newly built gridpacks for **mStop 350/450/550** (the gaps in the
  existing cvmfs SMS-StopStop set): the tarball plus the cards used to create it,
  named after the existing cvmfs gridpacks. All other mass points use gridpacks
  already on cvmfs (paths in the request CSV).

Total: 3,371 mass points · ~543 M events per campaign (see request CSV).

Request CSV (draft): [`csv/nps_stop_sms_requests_draft.csv`](csv/nps_stop_sms_requests_draft.csv) — 215 rows, one per dataset. Column order to be aligned with the official template
(`csv_for_requests/template_sus_requests.csv`) before submission.

Contact: Jiheon Kim (KNU) — jiheon.kim@cern.ch — Aug 2026
