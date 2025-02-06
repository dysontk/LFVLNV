//TO COMPILE: g++ `root-config --cflags --libs` -o read_root_file read_root_file.cpp
//TO RUN: ./read_root_file path/to/your/root/file.root


#include <iostream>
#include <TFile.h>
#include <TKey.h>
#include <TTree.h>
#include <TBranch.h>
#include <TLeaf.h>

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <path_to_root_file>" << std::endl;
        return 1;
    }

    const char* file_path = argv[1];
    TFile* file = TFile::Open(file_path);

    if (!file || file->IsZombie()) {
        std::cerr << "Error opening ROOT file: " << file_path << std::endl;
        return 1;
    }

    TKey* key;
    TIter next(file->GetListOfKeys());

    while ((key = (TKey*)next())) {
        TObject* obj = key->ReadObj();
        if (obj->IsA()->InheritsFrom(TTree::Class())) {
            TTree* tree = (TTree*)obj;
            std::cout << "Tree name: " << tree->GetName() << std::endl;
            std::cout << "Number of entries: " << tree->GetEntries() << std::endl;

            TObjArray* branches = tree->GetListOfBranches();
            for (int i = 0; i < branches->GetEntries(); ++i) {
                TBranch* branch = (TBranch*)branches->At(i);
                // std::cout << "  Branch name: " << branch->GetName() << std::endl;

                TObjArray* leaves = branch->GetListOfLeaves();
                for (int j = 0; j < leaves->GetEntries(); ++j) {
                    TLeaf* leaf = (TLeaf*)leaves->At(j);
                    // std::cout << "    Leaf name: " << leaf->GetName() << std::endl;
                }
            }
        }
        else{
            std::cout << "Something is wrong" << endl;
        }
    }

    file->Close();
    delete file;

    return 0;
}