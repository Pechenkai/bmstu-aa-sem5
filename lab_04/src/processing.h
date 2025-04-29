#ifndef PROCESSING_H
#define PROCESSING_H

#include <string>
#include <fstream>
#include <set>
#include <queue>
#include <regex>
#include <iostream>
#include <curl/curl.h>
#include <mutex>

std::string makeAbsoluteUrl(const std::string& relativeUrl);

bool containsRecipe(const std::string& content);

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* data);

std::string downloadPage(const std::string& url);

void savePage(const std::string& content, int threadIndex);

std::set<std::string> findLinks(const std::string& content);

#endif //PROCESSING_H
