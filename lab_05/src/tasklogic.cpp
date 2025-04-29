#include "tasklogic.h"

int generateTasks(TaskQueue<Task>& taskQueue, const std::string& folderPath)
{
    static int taskId = 1;
    int task_count = 0;

    try
    {
        for (const auto& entry : std::filesystem::directory_iterator(folderPath))
        {
            if (entry.is_regular_file())
            {
                std::string filename = entry.path().string();

                Task task(taskId++, filename);

                task.creation_time = std::chrono::high_resolution_clock::now();

                task_count++;

                taskQueue.push(task);
            }
        }
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error reading files from directory: " << e.what() << std::endl;
    }

    return task_count;
}

void readFile(TaskQueue<Task>& inputQueue, TaskQueue<Task>& outputQueue, int taskCount)
{
    int task_count = 0;

    while (task_count < taskCount)
    {
        Task task = inputQueue.pop();

        task.start_first_step = std::chrono::high_resolution_clock::now();

        std::ifstream file(task.filename);
        if (!file.is_open())
        {
            std::cerr << ": Failed to open file " << task.filename << std::endl;
            continue;
        }

        std::ostringstream contentStream;
        contentStream << file.rdbuf();
        task.content = contentStream.str();

        file.close();

        task.end_first_step = std::chrono::high_resolution_clock::now();

        outputQueue.push(task);

        task_count++;
    }
}


std::string cleanString(const std::string& input)
{
    std::string result = std::regex_replace(input, std::regex("<[^>]*>"), ""); // Удаление HTML-тегов
    result = std::regex_replace(result, std::regex("&nbsp;"), " "); // Замена спецсимволов
    result = std::regex_replace(result, std::regex("\\s+"), " "); // Удаление лишних пробелов
    result = std::regex_replace(result, std::regex("^\\s+|\\s+$"), ""); // Удаление пробелов в начале/конце строки
    return result;
}

void parseContent(TaskQueue<Task>& inputQueue, TaskQueue<Task>& outputQueue, int taskCount)
{
    int task_count = 0;

    while (task_count < taskCount)
    {
        Task task = inputQueue.pop();

        task.start_second_step = std::chrono::high_resolution_clock::now();

        std::istringstream contentStream(task.content);
        std::string line;

        std::string url, title;
        std::vector<std::map<std::string, std::string>> ingredients;
        std::vector<std::string> steps;

        bool findUrl = false;
        bool findTitle = false;
        bool findIngredients = false;

        while (std::getline(contentStream, line))
        {
            if (line.find("url=") == 0)
            {
                url = line.substr(4);
                findUrl = true;
            }

            else if (line.find("<title>") != std::string::npos && findUrl == true)
            {
                std::regex titleRegex("<title>(.*?)</title>");
                std::smatch match;
                if (std::regex_search(line, match, titleRegex))
                {
                    title = cleanString(match[1]);
                }

                findTitle = true;
            }

            else if (line.find("<h3>Потребуются:</h3>") != std::string::npos && findTitle == true)
            {
                while (std::getline(contentStream, line) && line.find("</ul>") == std::string::npos)
                {
                    if (line.find("<li>") != std::string::npos)
                    {
                        std::regex ingredientRegex("<li>(.*?)</li>");
                        std::smatch match;
                        if (std::regex_search(line, match, ingredientRegex))
                        {
                            std::string rawIngredient = cleanString(match[1]);

                            rawIngredient = std::regex_replace(rawIngredient, std::regex("&frac12;"), "1/2");
                            rawIngredient = std::regex_replace(rawIngredient, std::regex("&frac14;"), "1/4");

                            std::regex quantityRegex(
                                R"((\d+/\d+|\d+,\d+|\d+\.\d+|\d+)\s*(гр\.|гр|мл|шт\.|л|кг|г|мг|ст\. л\.|ч\.л\.|чайной ложки|столовые ложки|чайная ложка|столовая ложка)(\s|$))");
                            std::smatch quantityMatch;

                            std::string name = rawIngredient;
                            std::string unit, quantity;

                            if (std::regex_search(rawIngredient, quantityMatch, quantityRegex))
                            {
                                quantity = cleanString(quantityMatch[1]);
                                unit = cleanString(quantityMatch[2]);

                                size_t matchEnd = quantityMatch.position() + quantityMatch.length();
                                if (matchEnd < rawIngredient.size())
                                {
                                    name = rawIngredient.substr(matchEnd);
                                    name = cleanString(name);
                                }
                                else
                                {
                                    name = rawIngredient.substr(0, quantityMatch.position());
                                    name = cleanString(name);
                                }
                            }
                            else
                            {
                                std::regex fallbackRegex(R"(^(\d+)\s+(.+)$)");
                                std::smatch fallbackMatch;
                                if (std::regex_search(rawIngredient, fallbackMatch, fallbackRegex))
                                {
                                    quantity = fallbackMatch[1];
                                    name = cleanString(fallbackMatch[2]);
                                    unit = "шт.";
                                }
                            }

                            ingredients.push_back({{"name", name}, {"unit", unit}, {"quantity", quantity}});
                        }
                    }
                }

                findIngredients = true;
            }

            else if (findIngredients == true && line.find("<p>") == 0)
            {
                std::getline(contentStream, line);
                while (std::getline(contentStream, line) && line.find("</p>") != std::string::npos)
                {
                    std::string step = cleanString(line);
                    if (!step.empty())
                    {
                        steps.push_back(step);
                    }
                    std::getline(contentStream, line);
                }
                break;
            }
        }

        task.url = url;
        task.title = title;
        task.ingredients = ingredients;
        task.steps = steps;

        task.end_second_step = std::chrono::high_resolution_clock::now();
        outputQueue.push(task);

        task_count++;
    }
}

std::string toJSON(const std::vector<std::map<std::string, std::string>>& ingredients)
{
    std::ostringstream json;
    json << "[";
    for (size_t i = 0; i < ingredients.size(); ++i)
    {
        json << "{";
        json << "\"name\":\"" << ingredients[i].at("name") << "\",";
        json << "\"unit\":\"" << ingredients[i].at("unit") << "\",";
        json << "\"quantity\":\"" << ingredients[i].at("quantity") << "\"";
        json << "}";
        if (i < ingredients.size() - 1)
        {
            json << ",";
        }
    }
    json << "]";
    return json.str();
}

void writeToDatabase(TaskQueue<Task>& inputQueue, TaskQueue<Task>& outputQueue, int taskCount)
{
    int task_count = 0;

    try
    {
        const char* connectionString = std::getenv("RECIPES_DB_CONNECTION");
        if (connectionString == nullptr)
        {
            throw std::runtime_error("RECIPES_DB_CONNECTION is not set.");
        }

        pqxx::connection connection(connectionString);

        if (!connection.is_open())
        {
            throw std::runtime_error("Failed to connect to database.");
        }


        while (task_count < taskCount)
        {
            Task task = inputQueue.pop();

            task.start_third_step = std::chrono::high_resolution_clock::now();

            std::ostringstream ingredientsJSON;
            ingredientsJSON << "[";
            for (size_t i = 0; i < task.ingredients.size(); ++i)
            {
                const auto& ingredient = task.ingredients[i];
                ingredientsJSON << "{";
                for (auto it = ingredient.begin(); it != ingredient.end(); ++it)
                {
                    if (it != ingredient.begin())
                    {
                        ingredientsJSON << ",";
                    }
                    ingredientsJSON << "\"" << it->first << "\":\"" << it->second << "\"";
                }
                ingredientsJSON << "}";
                if (i < task.ingredients.size() - 1)
                {
                    ingredientsJSON << ",";
                }
            }
            ingredientsJSON << "]";

            std::ostringstream stepsJSON;
            stepsJSON << "[";
            for (size_t i = 0; i < task.steps.size(); ++i)
            {
                stepsJSON << "\"" << task.steps[i] << "\"";
                if (i < task.steps.size() - 1)
                {
                    stepsJSON << ",";
                }
            }
            stepsJSON << "]";

            std::string query = "INSERT INTO recipes (id, issue_id, url, title, ingredients, steps) VALUES (" +
                std::to_string(task.id) + ", " +
                "9169, " +
                connection.quote(task.url) + ", " +
                connection.quote(task.title) + ", " +
                connection.quote(ingredientsJSON.str()) + ", " +
                connection.quote(stepsJSON.str()) + ");";

            pqxx::work transaction(connection);
            transaction.exec(query);
            transaction.commit();


            task.end_third_step = std::chrono::high_resolution_clock::now();
            outputQueue.push(task);

            task_count++;
        }
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error in thread: " << e.what() << std::endl;
    }
}

void logProcessor(TaskQueue<Task>& finalQueue, int taskCount, const std::string& logFilename)
{
    struct LogEntry
    {
        std::chrono::time_point<std::chrono::high_resolution_clock> timestamp;
        std::string event;
        int taskId;
    };

    std::vector<LogEntry> logEntries;
    int task_count = 0;

    std::vector<long long> taskLifetimes;
    std::vector<long long> queueWaitTimes[3];
    std::vector<long long> stageDurations[3];

    while (task_count < taskCount)
    {
        Task task = finalQueue.pop();

        logEntries.push_back({task.creation_time, "creation", task.id});
        logEntries.push_back({task.start_first_step, "start_step_1", task.id});
        logEntries.push_back({task.end_first_step, "end_step_1", task.id});
        logEntries.push_back({task.start_second_step, "start_step_2", task.id});
        logEntries.push_back({task.end_second_step, "end_step_2", task.id});
        logEntries.push_back({task.start_third_step, "start_step_3", task.id});
        logEntries.push_back({task.end_third_step, "end_step_3", task.id});

        auto destruction_time = std::chrono::high_resolution_clock::now();
        logEntries.push_back({destruction_time, "destruction", task.id});

        task_count++;

        auto lifetime = std::chrono::duration_cast<std::chrono::microseconds>(destruction_time - task.creation_time).
            count();
        taskLifetimes.push_back(lifetime);

        auto wait1 = std::chrono::duration_cast<std::chrono::microseconds>(task.start_second_step - task.end_first_step)
            .
            count();
        auto duration1 = std::chrono::duration_cast<std::chrono::microseconds>(
            task.end_first_step - task.start_first_step).count();
        queueWaitTimes[0].push_back(wait1);
        stageDurations[0].push_back(duration1);

        auto wait2 = std::chrono::duration_cast<std::chrono::microseconds>(task.start_third_step - task.end_second_step)
            .count();
        auto duration2 = std::chrono::duration_cast<std::chrono::microseconds>(
            task.end_second_step - task.start_second_step).count();
        queueWaitTimes[1].push_back(wait2);
        stageDurations[1].push_back(duration2);

        auto wait3 = std::chrono::duration_cast<std::chrono::microseconds>(destruction_time - task.end_third_step)
            .count();
        auto duration3 = std::chrono::duration_cast<std::chrono::microseconds>(
            task.end_third_step - task.start_third_step).count();
        queueWaitTimes[2].push_back(wait3);
        stageDurations[2].push_back(duration3);
    }

    std::sort(logEntries.begin(), logEntries.end(), [](const LogEntry& a, const LogEntry& b)
    {
        return a.timestamp < b.timestamp;
    });

    std::ofstream logFile(logFilename);
    logFile << "\\begin{longtable}{|l|l|l|}\n\\hline\n";
    logFile << "Timestamp & Event & Task ID \\\\\\hline\n";

    for (const auto& entry : logEntries)
    {
        long long timestamp = std::chrono::duration_cast<std::chrono::microseconds>(
            entry.timestamp.time_since_epoch()).count();
        logFile << timestamp << " & " << entry.event << " & " << entry.taskId << " \\\\\\hline\n";
    }

    logFile << "\\end{longtable}\n";
    logFile.close();

    auto calculateAverage = [](const std::vector<long long>& times)
    {
        if (times.empty()) return 0LL;
        long long sum = 0;
        for (auto time : times)
        {
            sum += time;
        }
        return sum / static_cast<long long>(times.size());
    };

    long long avgLifetime = calculateAverage(taskLifetimes);
    long long avgQueueWait[3] = {
        calculateAverage(queueWaitTimes[0]),
        calculateAverage(queueWaitTimes[1]),
        calculateAverage(queueWaitTimes[2]),
    };
    long long avgStageDuration[3] = {
        calculateAverage(stageDurations[0]),
        calculateAverage(stageDurations[1]),
        calculateAverage(stageDurations[2]),
    };

    std::cout << "Average Task Lifetime: " << avgLifetime << " us\n";
    for (int i = 0; i < 3; ++i)
    {
        std::cout << "Average Queue Wait Time for Step " << (i + 1) << ": " << avgQueueWait[i] << " us\n";
        std::cout << "Average Stage Duration for Step " << (i + 1) << ": " << avgStageDuration[i] << " us\n";
    }
}
