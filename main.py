from ROOT import *
from copy import deepcopy
from rhapi import DEFAULT_URL, RhApi
import subprocess
import os

from config import *

gROOT.SetBatch() # don't pop up canvases
gStyle.SetOptStat()
gStyle.SetPalette(1) #palette change

gEnv.SetValue("Davix.GSI.UserCert", cert_file_path)
gEnv.SetValue("Davix.GSI.UserKey", key_file_path)

histogramNames = ["adc_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_" + str(i) for i in range(1, 5)]
histogramNames.extend(["adc_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_" + str(i) for i in range(1, 3)])

histogramDictionaryDic = { name : {} for name in histogramNames}

print(histogramNames)
### DEFINITIONS

def SelectOnlyLongestRunInTheFill(data):

  currFill = -1
  longestRunInTheFillDic = {}
  for d in data:
    fill = d[1]
    if currFill != fill:
      longestRunInTheFillDic.update({fill : [d[0], d[2]]})
      currFill = fill
    else:
      currentlyLongest = longestRunInTheFillDic[fill][1]
      if d[2] > currentlyLongest:
        longestRunInTheFillDic[fill] = [d[0], d[2]]
        
  print(longestRunInTheFillDic)
  
  runList = [[longestRunInTheFillDic[k][0], k] for k in longestRunInTheFillDic]
  runList.sort(key=lambda x: x[0])
    
  return runList
  
########################################
  
def SelectAllRuns(data):
  return [d[0:2] for d in data]

########################################
  
def GetRunNumbers():
  api = RhApi(DEFAULT_URL, debug = False)
        
  queryPiecesRunreg = [ customQueryPiece,
                  "r.pixel_present = 1",
                  "r.tracker_present = 1",
                  "r.bpix_ready = 1",
                  "r.fpix_ready = 1",
                  "r.beam1_stable = 1", 
                  "r.beam2_stable = 1",
                  "r.run_test = 0",
                  # "r.runlivelumi >= 50", #no value in this column...
                  ]
  qRunreg = "select r.runnumber, r.lhcfill, r.duration from runreg_tracker.runs r where " + " and ".join(queryPiecesRunreg) + " order by r.lhcfill asc"
  print(qRunreg)
  
  # queryPiecesWBM = ["f.lhcfill >= 6271",
                    # "f.lhcfill != 6336",
                    # "f.recorded > 50",
                    
                    # "r.lhcfill = f.lhcfill"]
  
  # qWBM = "select r.runnumber from wbm.runs r, wbm.fills f where " + " and ".join(queryPiecesWBM) + " order by r.runnumber asc"
  # print(qWBM)
  
  p = {}
  # qid = api.qid(qRunreg)
  # print api.count(qid, p)
  dataRunreg = api.json_all(qRunreg, p)
  print(dataRunreg)
  
  # dataWBM = [d[0] for d in api.json_all(qWBM, p)]
  
  # #FILTER OUT RUNS NOT IN DATAWBM
  # print("Before: " + str(len(dataRunreg)))
  # dataRunreg = [d for d in dataRunreg if d[0] in dataWBM]
  # print("After: " + str(len(dataRunreg)))
  # input("WAIT")
  return SelectAllRuns(dataRunreg) if not isSelectLongestRunInFill else SelectOnlyLongestRunInTheFill(dataRunreg)
  
########################################

def LinkGenerator(runNum):
  runNumStr = str(runNum)
  
  highStr = "000" + runNumStr[0:2] + "x"*4
  medStr = "000" + runNumStr[0:4] + "x"*2
  fileStr = fileBase + "000" + runNumStr + ".root"
  
  return urlBase + highStr + "/" + medStr + "/" + fileStr
  
########################################
  
def Grid2gif(image_str, output_gif):
  str1 = "convert " + conversionOptions + " " + image_str  + ' ' + output_gif #should create film like (unlooped)

  subprocess.call(str1, shell=True)  
  
########################################
    
def SaveInFolder(histogramDictionaryDic):
  if not os.path.exists(outputDir):
    os.system("mkdir " + outputDir)

  for name in histogramDictionaryDic:
    if not os.path.exists(outputDir + name):
      os.system("mkdir " + outputDir + name)
      
    for run in histogramDictionaryDic[name]:
      o = histogramDictionaryDic[name][run][0]
      
      c = TCanvas(name, name, histWidth, histHeight)
      o.SetTitle(o.GetTitle() + " -> " + str(histogramDictionaryDic[name][run][1]) + " (" + str(run) + ")")
      o.SetStats(0)
      o.GetYaxis().SetRange(0, 255)
      o.Draw("COLZ")
      
      c.Print(outputDir + name + "/" + str(run) + "." + fileType)
      
    Grid2gif(outputDir + name + "/*." + fileType, outputDir + name + "/out.gif")
      
### !DEFINITIONS  
  
runNumbers = GetRunNumbers()
print(len(runNumbers), runNumbers)

for run in runNumbers: 
  theUrl = LinkGenerator(run[0])
  print(theUrl)
  try:
    file = TFile.Open(theUrl)
    # file = TFile.Open("DQM_V0001_PixelPhase1_R000304366.root")
    
    if file.IsOpen():
      print("Success: %d" % (run[0]))
     
      baseRootDirs = ["DQMData/Run " + str(run[0]) + "/PixelPhase1/Run summary/Phase1_MechanicalView/PXBarrel",
                      "DQMData/Run " + str(run[0]) + "/PixelPhase1/Run summary/Phase1_MechanicalView/PXForward",
                      ]
                      
      for baseDir in baseRootDirs:
        for o in file.Get(baseDir).GetListOfKeys():
          if o.GetName() in histogramNames:
            histogramDictionaryDic[o.GetName()].update({run[0] : [deepcopy(o.ReadObj()), run[1]]}) 
           
      file.Close()
  except:
    print("Couldn't find: %d" % (run[0]))
    
SaveInFolder(histogramDictionaryDic)
