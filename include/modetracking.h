//==============================================================================
//
//     __  ___          __      __   ______            __   __ __ _ __
//    /  |/  /___  ____/ /___ _/ /  /_  __/___  ____  / /  / //_/(_) /_
//   / /|_/ / __ \/ __  / __ `/ /    / / / __ \/ __ \/ /  / ,<  / / __/
//  / /  / / /_/ / /_/ / /_/ / /    / / / /_/ / /_/ / /  / /| |/ / /
// /_/  /_/\____/\__,_/\__,_/_/    /_/  \____/\____/_/  /_/ |_/_/\__/
//
//
// University of Michigan
// Active Aeroelasticity and Structures Research Lab
//
// Author: Christopher A. Lupp
//
// Mode Tracking
//
//==============================================================================
#ifndef MTK_MODETRACKING_H

#define MTK_MODETRACKING_H

// system headers
#include <vector>

// Eigen headers
#include <Eigen/Eigen>

// MTK headers
#include "mtk_datatypes.h"
#include "modaltools.h"


using namespace std;
using namespace Eigen;


// Mode Tracking
//------------------------------------------------------------------------------
vector<ModeSet> TrackModes(vector<ModeSet> data)
{
    // results array (of ModeSets)
    vector<ModeSet> result;

    // temporary modeset for results
    ModeSet set_temp;

    // sorting of seed mode set
    for (int i = 0; i < data[0].Size(); ++i)
     {
        // remove all eigenpairs with negative imaginary part
        if (data[0][i].evalue.imag() >= 0.0)
        {
            set_temp.AddPair(data[0][i].evalue, data[0][i].evector);
            result.push_back(set_temp);
        }
     }
        

    for (int i = 0; i < data.size() - 1; ++i)
    {
        vector<int> exclude;
		double mac_temp;

        for (int j = 0; j < result[i-1].Size(); ++j)
        {
            // best MAC for mode j
            int best_index = 0;
            double mac_best = 0.0;

            complex<double> best_val = data[i+1][0].evalue;
            VectorXcd best_vec = data[i+1][0].evector;


            // previous mode
            VectorXcd prev_mode = result[i][j].evector;

            for (int k = 0; k < data[i+1].Size(); ++k)
            {
                if (find(exclude.begin(), exclude.end(), k) != exclude.end())
                {
                    continue;
                }
                else
                {
                    VectorXcd current_mode = data[i+1][k].evector;
                    mac_temp = ComputeMAC(prev_mode, current_mode);
                }

                if (mac_temp > mac_best)
                {
                    // set new best MAC
                    mac_best = mac_temp;

                    // save previous mode
                    best_index = k;
                    best_val = data[i+1][k].evalue;
                    best_vec = data[i+1][k].evector;
                }
            }

            // save the best mode and blacklist mode index
            set_temp.AddPair(best_val, best_vec);
            exclude.push_back(best_index);
        }
        
        result.push_back(set_temp);

        // reset blacklist
        exclude.clear();
    }

    return result;
}


#endif