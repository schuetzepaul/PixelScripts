#include "TROOT.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TKey.h"
#include "TObject.h"
#include <algorithm>
#include "TStyle.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TMacro.h"
#include "TList.h"
#include "TString.h"
#include "TObject.h"
#include "TH1D.h"
#include "TProfile2D.h"
#include "TLine.h"
//#inclide "string.h"
#include <iostream> // cout
#include <iomanip> //  setw
#include <fstream> // ofstream
#include <sstream> // combine string with integer

//
// A.Vargas Jul.2015
// Copy all histograms -except BB2- from Fulltest root file into the new root file: rootOutputName
// Copy BB2 subdirectory from rootPreTest into rootOutputName
// run it as:
// root -b -q 'combinePreFullTests.C("Testing_2015-07-13/M4027_FullQualification_2015-07-13_16h29m_1436797756/004_Fulltest_p17/pxar.root","Testing_2015-07-13/M4027_FullQualification_2015-07-13_16h29m_1436797756/000_Pretest_p17/pxar.root","pxarNew.root")' 


void combinePreFullTests( string rootFullName, string rootPreTest, string rootOutputName)
{

  // open output file 
  TFile *_fileSave = TFile::Open( rootOutputName.c_str(), "new" );
  // open existing files
  TFile * fileFullTest = TFile::Open( rootFullName.c_str(),"read" );  
  TFile * filePreTest = TFile::Open( rootPreTest.c_str(),"read" );

  fileFullTest->cd();
  if( ! fileFullTest ) continue;
  
  TIter nextkey( gDirectory->GetListOfKeys() );
  TKey * key;

  cout << "Copy Subdirectory/histograms from " << fileFullTest->GetName() << endl;
  cout << "into the file: " << _fileSave->GetName() << endl;

  while( ( key = (TKey*)nextkey() ) ) {
    
    TObject * obj = key->ReadObj();
    if (obj->IsA()->InheritsFrom( "TDirectory" )){
      cout << "----- Subdir " << obj->GetName() <<  "  " << obj->GetUniqueID() << endl;
      // create same structure
      _fileSave->mkdir(obj->GetName());
      
      // loop over all histograms in subdirectory
      fileFullTest->cd(obj->GetName());
      TIter nextkey2( gDirectory->GetListOfKeys() );
      TKey * key2;
       
      string objName = obj->GetName(); 
      if (objName.substr(0,3) == "BB2"){
	cout << "for Subdirectory BB2 in file " << fileFullTest->GetName() << " do nothing"  << endl;
      }
      else{
	while( ( key2 = (TKey*)nextkey2() ) ) {
	  _fileSave->cd();	
	  TObject * obj2 = key2->ReadObj();
	  
	  if( obj2->IsA()->InheritsFrom( "TH2D" )) {
	    //cout << "2d histograms " << obj2->GetName() << endl;
	    TH2D * h2 = (TH2D*)obj2;	  
	    _fileSave->cd(obj->GetName());
	    h2->Write();	  
	  }
	  else if ( obj2->IsA()->InheritsFrom( "TH1D" )) {	  
	    //cout << "1d histograms " << obj2->GetName() << endl;
	    TH1D * h1 = (TH1D*)obj2;
	    _fileSave->cd(obj->GetName());
	    h1->Write();	  
	  }	
	}
      } // do not save BB2 from Fulltest but from next file
      // here please save BB2 to final file

    }
    else{
      // store Histograms which are not in a subdirectory HA and HD
      _fileSave->cd();
      if ( obj->IsA()->InheritsFrom( "TH1D" )) {	  
	//cout << "1d histograms " << obj->GetName() << endl;
	TH1D * h1 = (TH1D*)obj;
	_fileSave->cd();
	h1->Write();	  
      }	
      //cout << obj->GetName() <<  " this is a histogram " << endl;
    }

  }

  // Now use BB2 from Pretest and store it in the outputfile _fileSave

  if( ! filePreTest ) continue;

  filePreTest->cd();
  filePreTest->cd("BB2");
  cout << "copy BB2 histograms from file " << filePreTest->GetName() << " into " << _fileSave->GetName() << endl;
 
  TIter nextkey3( gDirectory->GetListOfKeys() );
  TKey * key3;
  while( ( key3 = (TKey*)nextkey3() ) ) {    
    TObject * obj3 = key3->ReadObj();
    if( obj3->IsA()->InheritsFrom( "TH2D" )) {
      //cout << "2d histograms " << obj3->GetName() << endl;
      TH2D * h2 = (TH2D*)obj3;	  
      _fileSave->cd("BB2");
      h2->Write();	  
    }
    else if ( obj3->IsA()->InheritsFrom( "TH1D" )) {	  
      //cout << "1d histograms " << obj3->GetName() << endl;
      TH1D * h1 = (TH1D*)obj3;
      _fileSave->cd("BB2");
      h1->Write();	  
    }
    //cout << "----- " << obj3->GetName() << endl;
  }


  fileFullTest->Close();
  filePreTest->Close();
  _fileSave->Close();

}

