#ifndef TWORK_H
#define TWORK_H

#include <thread>
#include <ctime>
#include <unordered_set>
#include <chrono>
#include <sstream>
#include <iomanip>
#include "processing.h"

std::chrono::duration<double> crawlSequential(const std::string& startUrl, size_t maxPagesToDownload, bool muteMode = false);
std::chrono::duration<double> crawlParallel(const std::string& startUrl, int threadCount, size_t maxPagesToDownload, bool muteMode = false);

#endif //TWORK_H
