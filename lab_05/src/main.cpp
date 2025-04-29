#include <thread>
#include <iostream>
#include "TaskQueue.hpp"
#include "tasklogic.h"

int main()
{
    TaskQueue<Task> queueAfterGeneration;
    TaskQueue<Task> queueAfterReading;
    TaskQueue<Task> queueAfterParsing;
    TaskQueue<Task> queueAfterWriting;

    std::string folderPath = "../data";
    std::string logPath = "../log.tex";

    int taskCount = generateTasks(queueAfterGeneration, folderPath);

    std::cout << taskCount << std::endl;

    std::thread reader(readFile, std::ref(queueAfterGeneration), std::ref(queueAfterReading), taskCount);

    std::thread parser(parseContent, std::ref(queueAfterReading), std::ref(queueAfterParsing), taskCount);

    std::thread writer(writeToDatabase, std::ref(queueAfterParsing), std::ref(queueAfterWriting), taskCount);

    std::thread logger(logProcessor, std::ref(queueAfterWriting), taskCount, logPath);

    reader.join();
    parser.join();
    writer.join();
    logger.join();

    return 0;
}
