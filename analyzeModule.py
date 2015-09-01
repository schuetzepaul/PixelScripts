#!/usr/bin/env python
from ROOT import *
import glob, os
from array import array

gROOT.SetBatch(kTRUE) 
outdir = "Overview"
postfix = ".png"

def _makelabel(text):
    pt = TPaveText(0.3507014,0.9013333,0.6012024,0.9573333,"br")
    pt.SetFillColor(0)
    pt.SetFillStyle(0)
    pt.SetLineColor(0)
    pt.SetShadowColor(0)
    pt.SetTextColor(1)
    pt.AddText(text);
    return pt


def _modmap(rocs, colors, logy=False):
    if len(colors) > 1:
        color = array('i', colors)
        gStyle.SetPalette( 4, color);
    else:
        gStyle.SetPalette(1)

    c = TCanvas("modmap","modmap",2200,800)

    c.cd()
    gPad.SetMargin(0.3,0.3,0.2,0.3)
    c.Divide(8,2,0,0)    

    #modmap.Divide(8,2)

    gStyle.SetOptStat(0)
    for i,roc in enumerate(rocs):
        roc.SetTitle("ROC "+ str(i))
        c.cd(i+1)
        if logy:
            gPad.SetLogy()
        
        roc.Draw("col")

        roc.GetXaxis().SetTickSize(0.00001)
        roc.GetYaxis().SetTickSize(0.00001)
        roc.GetZaxis().SetTickSize(0.00001)
        roc.GetXaxis().SetLabelSize(0.09)
        roc.GetYaxis().SetLabelSize(0.05)

    return c
    
def PixelAlive(tfile, testName, modName):
    rocs = []
    colors=[0, 1, 2, 3, 4, 5, 6]
    for i in range (0,16):
        hist = tfile.Get("PixelAlive/PixelAlive_C"+ str(i) + "_V0")
        rocs.append(hist)
    
    c = _modmap( rocs , colors)
    pt = _makelabel(testName +" "+ modName +" Pixel Alive map")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_Alive" + postfix)
    return c

def BB2(tfile, testName, modName):
    thrwidth_rocs = []
    bb2_rocs = []
    colors=[0, 1, 3, 2]
    for i in range (0,16):
        hist = tfile.Get("BB2/BBtestMap_C"+ str(i) + "_V0")
        bb2_rocs.append(hist)
        hist = tfile.Get("BB2/CalsVthrPlateauWidth_C"+ str(i) + "_V0")
        thrwidth_rocs.append(hist)


    c = _modmap( bb2_rocs , colors)
    pt = _makelabel(testName +" "+ modName +" BB2 Map")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" +modName+ "/" + testName+ "_BB2" + postfix)

    c = _modmap( thrwidth_rocs , colors, true)
    pt = _makelabel(testName +" "+ modName + " BB2 ThrWidth Distribution")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" +modName+ "/" + testName+ "_BB2_ThrWidth" + postfix)

    return 0

def Trim(tfile, testName, modName):
    thrfinal = []
    thrfinal = []
    distthrfinal = []
    thrinitial = []    
    
    colors=[0]
    for i in range (0,16):
        hist = tfile.Get("Trim/thr_TrimThrFinal_vcal_C"+ str(i) + "_V0")
        hist.SetMinimum(0)
        hist.SetMaximum(45)
        thrfinal.append(hist)
        
        hist = tfile.Get("Trim/dist_thr_TrimThrFinal_vcal_C"+ str(i) + "_V0")
        distthrfinal.append(hist)

        hist = tfile.Get("Trim/thr_TrimThr0_vthrcomp_C"+ str(i) + "_V0")
        hist.SetMinimum(0)
        hist.SetMaximum(150)
        thrinitial.append(hist)

    c = _modmap( thrinitial , colors)
    pt = _makelabel(testName +" "+ modName +" Threshold Map before Trimming Range 0 - 150")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_ThrMapInitial" + postfix)    
    c = _modmap( thrfinal , colors)
    pt = _makelabel(testName +" "+ modName +" Threshold Map after Trimming Range 0 - 45")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_ThrMapFinal" + postfix)

    c = _modmap( distthrfinal , colors, True)
    pt = _makelabel(testName +" "+ modName +" Threshold Dist after Trimming")
    c.cd()
    pt.Draw()
    c.SaveAs(outdir + "/" + modName+ "/" + testName+ "_ThrDistFinal" + postfix)



    return c

def HtmlMod(modName, plots):
    f = open(outdir + "/"+modName + ".html",'w')
    f.write("<html> \n")
    f.write("<head> \n")
    f.write("<title>Quick Module Qualification</title> \n")
    f.write("</head> \n")
    f.write("<body> \n")

    pretest =  [  x for x in plots if "000" in x ]
    fulltest1 =  [  x for x in plots if "001" in x ]
    fulltest2 =  [  x for x in plots if "003" in x ]
    f.write("<h1> 000_Pretest_p17</h1> <br>")
    for plot in pretest:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="200" width="600"> </a> \n' )

    f.write("<h1> 001_Fulltest_m20</h1> <br>")
    for plot in fulltest1:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="200" width="600"> </a> \n' )

    f.write("<h1> 003_Fulltest_m20</h1> <br>")
    for plot in fulltest2:
        f.write('<a href="'+ plot +'">')
        f.write('<img src="'+ plot +'" height="200" width="600"> </a> \n' )

    f.write("</body> \n")
    f.write("</html> \n")


def HtmlIndex(modules):
    f = open(outdir + "/index.html",'w')
    f.write("<html> \n")
    f.write("<head> \n")
    f.write("<title>Quick Module Qualification</title> \n")
    f.write("</head> \n")
    f.write("<body> \n")
    
    for mod in modules:
        f.write('<a href="' + mod +'.html">Module ' + mod +' </a> <br> \n' )

    f.write("</body> \n")
    f.write("</html> \n")

if __name__ == "__main__":
    
    try:
        os.stat(outdir)
    except:
        os.mkdir(outdir)
    modules = []
    for fileName in glob.glob('./*/*/pxar.root'):
        
        tfile = TFile(fileName,"READ")
        modName = fileName[fileName.find("M"):fileName.find("M") + 5 ]
        modules.append(modName)
        testName = fileName[ fileName.find("/0") +1 : fileName.find("/pxa")]
        try:
            os.stat(outdir + "/"+modName)
        except:
            os.mkdir(outdir + "/"+modName)

        if not "IV" in fileName:
            PixelAlive(tfile, testName, modName)
            BB2(tfile, testName, modName)
            if "Fulltest" in fileName:
                Trim(tfile, testName, modName)

    modules = set(modules)
    plots = []
    for mod in modules:
        plots = glob.glob(outdir + "/" + mod +"/*" + postfix)
        plots = [ x.replace(outdir + "/", "") for x in plots ]
        
        HtmlMod(mod, plots)

    HtmlIndex(modules)

