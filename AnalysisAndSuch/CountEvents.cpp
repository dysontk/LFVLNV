//TO COMPILE:  g++ `root-config --cflags --libs` -o CountEvents CountEvents.cpp `root-config --libs` `root-config --cflags`
//TO RUN: ./CountEvents 
// For ease of running, this all of the file paths are hard coded into here since I'll be 
// using this mainly for counting across multiple files. Use read_root_file.cpp if only one


#include <iostream>
#include <TFile.h>
#include <TKey.h>
#include <TTree.h>
#include <TBranch.h>
#include <TLeaf.h>
#include <string>

using namespace std;

const int numDirs = 4;

string startPath = "/work/pi_mjrm_umass_edu/LNV_collider/Generated/";


string files[numDirs][2] = {{"ttbar", "3"}, {"W3j", "2"}, {"WZ2j", "3"}, {"ZZ2j", "1"}};

//  {"ZZ2j", "run_01"}};
// Copy paths

bool adHoc = false;

int main()
{
    vector <string> filePaths;
    int nEvents = 0;

    for (int i=0; i<numDirs; i++)
    {
        for (int r=1; r<=stoi(files[i][1]); r++)
        {
            string run = "run_0"+to_string(r);
            cout<< files[i][0] << " " <<run << endl;
            string thisPath = startPath + files[i][0] + "/Events/" + run + "/tag_1_delphes_events.root";
            cout << "Trying : " << startPath<< endl;
            const int thisLength = thisPath.length();
            char* file_path = new char[thisLength+1];
            strcpy(file_path, thisPath.c_str());

            TFile* file = TFile::Open(file_path);

            int attempts = 0;
            while ((!file || file->IsZombie()) and attempts < 4 )
            {
                cerr << "Error opening ROOT file:" << file_path << endl;
                // return 1;
                thisPath = startPath + files[i][0] + "/Events/" + run + "/tag_" + to_string(attempts+2)+"_delphes_events.root";
                // file_path = new char[thisLength+1];
                strcpy(file_path, thisPath.c_str());
                cout << "Am trying new tag"<< endl << thisPath << endl;
                file = TFile::Open(file_path);
                attempts++;
            }

            TKey* key;
            TIter next(file->GetListOfKeys());

            while ((key=(TKey*)next()))
            {
                TObject* obj = key->ReadObj();
                if (obj->IsA()->InheritsFrom(TTree::Class()))
                {
                    TTree* tree = (TTree*) obj;
                    nEvents += tree->GetEntries();
                }
            }
            file->Close();
            delete file;
            cout << "Finished " << thisPath<< endl;
        }
    }

    // int nEvents = 0;

    // for (int f = 0; f<numFiles; f++)
    // {
    //     string thisPath = filePaths[f];
    //     const int thisLength = thisPath.length();
    //     char* file_path = new char[thisLength+1];
    //     strcpy(file_path, thisPath.c_str());

    //     // const string* file_path = filePaths[f];
    //     TFile* file = TFile::Open(file_path);

    //     if (!file || file->IsZombie())
    //     {
    //         cerr << "Error opening ROOT file:" << file_path << endl;
    //         return 1;
    //     }
    //     TKey* key;
    //     TIter next(file->GetListOfKeys());

    //     while ((key=(TKey*)next()))
    //     {
    //         TObject* obj = key->ReadObj();
    //         if (obj->IsA()->InheritsFrom(TTree::Class()))
    //         {
    //             TTree* tree = (TTree*) obj;
    //             nEvents += tree->GetEntries();
    //         }
    //     }
    //     file->Close();
    //     delete file;
    //     cout << "Finished " << thisPath<< endl;
    // }
    cout << "Total number of events is "<< nEvents<< endl;
    return 0;    
}