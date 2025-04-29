#include <iostream>
#include <string>
#include "twork.h"

int main()
{
    std::string start_url;
    int max_pages;
    int choice;
    int num_threads = 1;

    std::cout << "=== Программа для загрузки страниц с https://sytyikrolik.ru ===" << std::endl;

    start_url = "https://sytyikrolik.ru";

    std::cout << "Введите максимальное количество страниц для загрузки: ";
    while (!(std::cin >> max_pages) || max_pages <= 0)
    {
        std::cout << "Введено некорректное число страниц!" << std::endl;
        std::cout << "Введите положительное число: ";
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    std::cout << "Выберите режим обработки:\n";
    std::cout << "1 - Последовательный\n";
    std::cout << "2 - Параллельный\n";
    std::cout << "3 - Исследование по числу потоков\n";
    std::cout << "4 - Исследование по числу страниц\n";
    std::cout << "Ваш выбор: ";
    while (!(std::cin >> choice) || choice <= 0 || choice > 4)
    {
        std::cout << "Введена некорректная опция!" << std::endl;
        std::cout << "Введите положительное число (1-2): ";
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    if (choice == 2)
    {
        std::cout << "Введите количество потоков для параллельной обработки: ";
        while (!(std::cin >> num_threads) || num_threads <= 0)
        {
            std::cout << "Введено некорректное число потоков!" << std::endl;
            std::cout << "Введите положительное число: ";
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }

        std::cout << "\nЗапуск параллельной обработки с " << num_threads << " потоками...\n";
        crawlParallel(start_url, num_threads, max_pages);
    }
    else if (choice == 1)
    {
        std::cout << "\nЗапуск последовательной обработки...\n";
        crawlSequential(start_url, max_pages);
    }
    else if (choice == 3)
    {
        int start_thread = 1;
        int end_thread = 4;
        int pages_count = 100;

        std::chrono::duration<double> time = crawlSequential(start_url, pages_count, true);
        std::ofstream outFile("../data/res_threads.txt");

        if (!outFile.is_open())
        {
            std::cerr << "Error: Could not open file for writing." << std::endl;
            return 1;
        }

        outFile << "0 " << time.count() << std::endl;

        for (int i = start_thread; i <= end_thread; i++)
        {
            time = crawlParallel(start_url, i * 4, pages_count, true);
            outFile << std::to_string(i * 4) << " " << time.count() << std::endl;
        }

        outFile.close();
    }
    else
    {
        int start_pages = 10;
        int end_pages = 100;
        int step = 10;

        int threads_count = 12;

        std::chrono::duration<double> time{};
        std::ofstream outFile("../data/res_pages.txt");


        for (int i = start_pages; i <= end_pages; i+=step)
        {
            outFile << i << " ";
            time = crawlSequential(start_url, i, true);
            outFile << time.count() << " ";
            time = crawlParallel(start_url, threads_count, i, true);
            outFile << time.count() << std::endl;
        }

        outFile.close();
    }


    std::cout << "Обработка завершена." << std::endl;
    return 0;
}
