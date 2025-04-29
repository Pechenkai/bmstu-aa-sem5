#ifndef TASKQUEUE_HPP
#define TASKQUEUE_HPP

#include <queue>
#include <mutex>
#include <condition_variable>

template <typename T>
class TaskQueue {
public:
    TaskQueue() = default;
    ~TaskQueue() = default;

    void push(const T& value) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            queue.push(value);
        }
        cv.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this] { return !queue.empty(); });
        T value = queue.front();
        queue.pop();
        return value;
    }

    bool empty() const {
        std::lock_guard<std::mutex> lock(mtx);
        return queue.empty();
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mtx);
        return queue.size();
    }

private:
    std::queue<T> queue;
    mutable std::mutex mtx;
    std::condition_variable cv;
};

#endif
