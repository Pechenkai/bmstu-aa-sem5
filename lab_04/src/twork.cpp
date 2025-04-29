#include "twork.h"

std::set<std::string> visitedUrls;
std::unordered_set<std::string> urlSet;
std::mutex urlMutex;

std::string getCurrentTime()
{
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    std::ostringstream ss;
    ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %X");
    return ss.str();
}

void logAction(std::vector<std::vector<std::string>>& logThreads, int threadIndex, const std::string& action,
               const std::string& url)
{
    std::ostringstream logEntry;
    logEntry << "[" << getCurrentTime() << "] " << "Thread " << threadIndex << ": " << action << " - " << url;
    logThreads[threadIndex].push_back(logEntry.str());
}

std::chrono::duration<double> crawlSequential(const std::string& startUrl, size_t maxPagesToDownload, bool muteMode)
{
    urlSet.insert(startUrl);

    // std::cout <<urlSet.front() << std::endl;

    std::string currentUrl;
    size_t pagesDownloaded = 0;

    auto start = std::chrono::high_resolution_clock::now();

    while (!urlSet.empty() && pagesDownloaded < maxPagesToDownload)
    {
        auto it = urlSet.begin();
        currentUrl = *it;
        urlSet.erase(it);

        if (visitedUrls.find(currentUrl) != visitedUrls.end())
        {
            continue;
        }

        visitedUrls.insert(currentUrl);

        std::string content = downloadPage(currentUrl);

        // std::cout << content << std::endl;

        if (containsRecipe(content))
        {
            savePage(content, 0);

            if (!muteMode)
                std::cout << "Page saved in sequential mode: " << currentUrl << std::endl;
        }

        ++pagesDownloaded;
        if (pagesDownloaded >= maxPagesToDownload)
        {
            break;
        }

        auto newLinks = findLinks(content);
        for (const auto& link : newLinks)
        {
            if (visitedUrls.find(link) == visitedUrls.end())
            {
                urlSet.insert(link);
                // std::cout << link << std::endl;
            }
        }


        // std::cout << urlSet.size() << std::endl;
        // std::cout << *(urlSet.begin()) << std::endl;
    }

    auto end = std::chrono::high_resolution_clock::now();

    return std::chrono::duration_cast<std::chrono::duration<double>>(end - start);

}

std::chrono::duration<double> crawlParallel(const std::string& startUrl, int threadCount, size_t maxPagesToDownload, bool muteMode)
{
    urlSet.insert(startUrl);
    std::vector<std::vector<std::string>> logThreads;
    logThreads.resize(threadCount);

    size_t pagesDownloaded = 0;
    std::mutex counterMutex;
    bool done = false;

    std::vector<std::vector<std::string>> threadLog;


    auto worker = [&](int threadIndex)
    {
        while (true)
        {
            std::string currentUrl;

            {
                std::lock_guard<std::mutex> lock(urlMutex);

                if (done || (urlSet.empty() && pagesDownloaded >= maxPagesToDownload))
                {
                    done = true;
                    break;
                }

                if (!urlSet.empty())
                {
                    auto it = urlSet.begin();
                    currentUrl = *it;
                    urlSet.erase(it);
                }
                else
                {
                    continue;
                }

                if (visitedUrls.find(currentUrl) != visitedUrls.end())
                    continue;
                visitedUrls.insert(currentUrl);
            }

            std::string content = downloadPage(currentUrl);
            if (!muteMode)
                logAction(logThreads, threadIndex, "Загрузка", currentUrl);

            if (containsRecipe(content))
            {
                savePage(content, threadIndex);
                if (!muteMode)
                    logAction(logThreads, threadIndex, "Сохранение", currentUrl);
                // std::cout << "Page saved by thread: " << std::to_string(threadIndex) << ": " << currentUrl << std::endl;
            }

            {
                std::lock_guard<std::mutex> counterLock(counterMutex);
                ++pagesDownloaded;
                if (pagesDownloaded >= maxPagesToDownload)
                {
                    done = true;
                    break;
                }
            }

            auto newLinks = findLinks(content);

            {
                std::lock_guard<std::mutex> lock(urlMutex);
                for (const auto& link : newLinks)
                {
                    if (visitedUrls.find(link) == visitedUrls.end())
                    {
                        urlSet.insert(link);
                    }
                }
            }
        }
    };


    auto start = std::chrono::high_resolution_clock::now();

    std::vector<std::thread> threads;
    for (int i = 0; i < threadCount; ++i)
        threads.emplace_back(worker, i);

    for (auto& t : threads)
        t.join();

    auto end = std::chrono::high_resolution_clock::now();

    if (!muteMode)
    {
        std::cout << "Лог действий:" << std::endl;
        for (int i = 0; i < logThreads.size(); ++i)
        {
            std::cout << "Thread " << i << " log:" << std::endl;
            for (const auto& entry : logThreads[i])
            {
                std::cout << entry << std::endl;
            }
            std::cout << "--------------------------------" << std::endl;
        }
    }

    return std::chrono::duration_cast<std::chrono::duration<double>>(end - start);
}
