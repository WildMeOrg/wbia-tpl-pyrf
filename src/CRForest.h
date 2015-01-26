/*
// Author: Juergen Gall, BIWI, ETH Zurich
// Email: gall@vision.ee.ethz.ch
*/

#pragma once

#include "CRTree.h"

#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

class CRForest {
public:
	// Constructors
	CRForest(int trees = 0) {
		vTrees.resize(trees);
	}
	~CRForest() {
		for(std::vector<CRTree*>::iterator it = vTrees.begin(); it != vTrees.end(); ++it) delete *it;
		vTrees.clear();
	}

	// Set/Get functions
	void SetTrees(int n) {vTrees.resize(n);}
	int GetSize() const {return vTrees.size();}
	unsigned int GetDepth() const {return vTrees[0]->GetDepth();}
	unsigned int GetNumCenter() const {return vTrees[0]->GetNumCenter();}

	// Regression
	void regression(std::vector<const LeafNode*>& result, uchar** ptFCh, int stepImg) const;

	// Training
	void trainForest(int min_s, int max_d, CvRNG* pRNG, const CRPatch& TrData, int samples, int default_split, const char* filename, unsigned int offset = 0);

	// IO functions
	void saveForest(const char* filename, unsigned int offset = 0);
	void loadForest(const char* filename, int type = 0);
	void show(int w, int h) const {vTrees[0]->showLeaves(w,h);}

	// Trees
	std::vector<CRTree*> vTrees;
};

inline void CRForest::regression(std::vector<const LeafNode*>& result, uchar** ptFCh, int stepImg) const {
	result.resize( vTrees.size() );

	#pragma omp parallel for
	for(int i=0; i<(int)vTrees.size(); ++i) {
		result[i] = vTrees[i]->regression(ptFCh, stepImg);
	}
}

//Training
inline void CRForest::trainForest(int min_s, int max_d, CvRNG* pRNG, const CRPatch& TrData, int samples, int default_split, const char* filename, unsigned int offset) {
	char buffer[200];

	std::cout << "AIM FOR A SPLIT OF 24k - 32k POSITIVE & NEGATIVE PATCHES EACH FOR GOOD REGULARIZATION AT DEPTH 16" << std::endl;
	std::cout << "\n**************************\n" << std::endl;
	for(int i=0; i < (int)vTrees.size(); ++i) {
		vTrees[i] = new CRTree(min_s, max_d, TrData.vLPatches[1][0].center.size(), pRNG);
		vTrees[i]->growTree(TrData, samples, default_split);

		// Save as trees are grown
		std::cout << std::endl;
		sprintf_s(buffer,"%s%03d.txt",filename,i+offset);
		vTrees[i]->saveTree(buffer);
		std::cout << "\n**************************\n" << std::endl;
	}
}

// IO Functions
inline void CRForest::saveForest(const char* filename, unsigned int offset) {
	char buffer[200];

	for(unsigned int i=0; i<vTrees.size(); ++i) {
		sprintf_s(buffer,"%s%03d.txt",filename,i+offset);
		vTrees[i]->saveTree(buffer);
	}
}

inline void CRForest::loadForest(const char* filename, int type) {
	char buffer[200];
	int offset = 1;
	for(unsigned int i=0; i<vTrees.size(); ++i) {
		sprintf_s(buffer,"%s%03d.txt",filename,i+offset);
		vTrees[i] = new CRTree(buffer);
	}
}
