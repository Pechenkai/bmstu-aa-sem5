#include "processing.h"


bool isSameDomain(const std::string& url)
{
    std::string baseDomain = "sytyikrolik.ru";
    return (url.find("http://" + baseDomain) == 0 || url.find("https://" + baseDomain) == 0);
}

std::string makeAbsoluteUrl(const std::string& relativeUrl)
{
    const std::string baseUrl = "https://sytyikrolik.ru";
    if (relativeUrl.find("http://") == 0 || relativeUrl.find("https://") == 0)
    {
        return relativeUrl;
    }
    if (relativeUrl[0] == '/')
    {
        return baseUrl + relativeUrl;
    }
    return baseUrl + "/" + relativeUrl;
}

bool containsRecipe(const std::string& content)
{
    return content.find("Потребуются:") != std::string::npos;
}

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* data)
{
    size_t totalSize = size * nmemb;
    data->append((char*)contents, totalSize);
    return totalSize;
}

std::string downloadPage(const std::string& url)
{
    CURL* curl;
    CURLcode res;
    std::string buffer;

    curl = curl_easy_init();
    if (curl)
    {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK)
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;

        curl_easy_cleanup(curl);
    }

    return buffer;
}

void savePage(const std::string& content, int threadIndex)
{
    std::string filename = "../data/page_" + std::to_string(threadIndex) + ".html";
    std::ofstream outFile(filename);

    if (!outFile.is_open())
    {
        std::cerr << "Error: Could not open file " << filename << " for writing." << std::endl;
        return;
    }

    outFile << content;
    outFile.close();
}

std::set<std::string> findLinks(const std::string& content)
{
    std::set<std::string> newLinks;
    std::regex linkRegex(R"(<a\s+(?:[^>]*?\s+)?href=["']([^"']+)["'])");
    auto linksBegin = std::sregex_iterator(content.begin(), content.end(), linkRegex);
    auto linksEnd = std::sregex_iterator();

    for (std::sregex_iterator i = linksBegin; i != linksEnd; ++i)
    {
        std::smatch match = *i;
        std::string url = match[1].str();
        std::string absoluteUrl = makeAbsoluteUrl(url);

        if (url[0] == '/' || isSameDomain(absoluteUrl))
        {
            newLinks.insert(absoluteUrl);
        }
    }

    return newLinks;
}
