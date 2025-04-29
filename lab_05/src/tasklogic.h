#ifndef TASKLOGIC_H
#define TASKLOGIC_H

#include <string>
#include <vector>
#include <regex>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <filesystem>
#include <pqxx/pqxx>
#include <iostream>
#include "TaskQueue.hpp"

struct Ingredient {
    std::string name;
    std::string unit;
    double quantity;
};

class Task {
public:
    int id;
    std::string filename;
    std::string url;
    std::string title;
    std::string content;
    std::vector<std::map<std::string, std::string>> ingredients;
    std::vector<std::string> steps;

    std::chrono::time_point<std::chrono::high_resolution_clock> creation_time;
    std::chrono::time_point<std::chrono::high_resolution_clock> start_first_step;
    std::chrono::time_point<std::chrono::high_resolution_clock> end_first_step;
    std::chrono::time_point<std::chrono::high_resolution_clock> start_second_step;
    std::chrono::time_point<std::chrono::high_resolution_clock> end_second_step;
    std::chrono::time_point<std::chrono::high_resolution_clock> start_third_step;
    std::chrono::time_point<std::chrono::high_resolution_clock> end_third_step;

    Task(int taskId, const std::string& file)
        : id(taskId), filename(file), creation_time(std::chrono::high_resolution_clock::now()) {}
};

int generateTasks(TaskQueue<Task>& taskQueue, const std::string& folderPath);
void readFile(TaskQueue<Task>& inputQueue, TaskQueue<Task>& outputQueue, int taskCount);
void parseContent(TaskQueue<Task>& inputQueue, TaskQueue<Task>& outputQueue, int taskCount);
void writeToDatabase(TaskQueue<Task>& inputQueue, TaskQueue<Task>& outputQueue, int taskCount);
void logProcessor(TaskQueue<Task>& finalQueue, int taskCount, const std::string& logFilename);

#endif //TASKLOGIC_H
