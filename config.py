### CONFIG

cert_file_path = "/afs/cern.ch/user/p/pjurgiel/.globus/copy/usercert.pem"
key_file_path = "/afs/cern.ch/user/p/pjurgiel/.globus/copy/userkey_nopass.pem"

urlBase = "https://cmsweb.cern.ch/dqm/online/data/browse/Original/"
fileBase = "DQM_V0001_PixelPhase1_R"

fillStart = 6271
customQueryPiece = " and ".join(["r.lhcfill >= " + str(fillStart),
                                 "r.lhcfill != 6336"])
                                 
isSelectLongestRunInFill = False

histWidth, histHeight = 1280, 720
outputDir = "OUT/"
fileType = "png"

conversionOptions = "-delay 40 -loop 1"

### !CONFIG