#include <iostream>
#include <chrono>
#include <vector>
#include <fstream>
#include <string>
#include <filesystem> // Required for directory creation

constexpr size_t EXPERIMENT_ITERATIONS{1'000'000};
const std::string output_file_extension{".bin"};
const std::string output_file_directory{"output"};

class TimeDeltaRecorder
{
public:
    using clock_t = std::chrono::high_resolution_clock;
    using duration_t = clock_t::duration;

    void start() { _start = clock_t::now(); }
    void stop() { _deltas.emplace_back(clock_t::now() - _start); }

    void write_to_file(const std::string& filename)
    {
        std::ofstream out_file(filename, std::ios::binary);
        if (!out_file)
        {
            std::cerr << "Error: Could not open file " << filename << std::endl;
            return;
        }

        std::vector<int64_t> durations_in_ns;
        for (const auto& delta : _deltas)
        {
            durations_in_ns.push_back(std::chrono::duration_cast<std::chrono::nanoseconds>(delta).count());
        }

        out_file.write(reinterpret_cast<const char*>(durations_in_ns.data()), durations_in_ns.size() * sizeof(int64_t));
        out_file.close();
    }

private:
    std::vector<duration_t> _deltas{};
    clock_t::time_point _start{};
};

void ensure_output_directory()
{
    std::filesystem::create_directories(output_file_directory);
}

std::string filename_from_epoch_number(size_t epoch_number)
{
    return output_file_directory + "/epoch_" + std::to_string(epoch_number) + output_file_extension;
}

void operation()
{
    volatile int total = 0;
    for (size_t i = 0; i < 100; i++)
    {
        for (size_t j = 0; j < 100; j++)
        {
            total++;
        }
    }
}

void experiment(size_t epoch_number)
{
    std::cout << "Epoch " << epoch_number << " started experiment with " << EXPERIMENT_ITERATIONS << " iterations...\n";
    
    auto start_time = TimeDeltaRecorder::clock_t::now();
    TimeDeltaRecorder recorder{};

    for (size_t i = 0; i < EXPERIMENT_ITERATIONS; i++)
    {
        recorder.start();
        operation();
        recorder.stop();
    }

    // Ensure output directory exists before writing
    ensure_output_directory();
    recorder.write_to_file(filename_from_epoch_number(epoch_number));

    double elapsed_time = std::chrono::duration<double>(TimeDeltaRecorder::clock_t::now() - start_time).count();
    std::cout << "Epoch " << epoch_number << " completed in " << elapsed_time << " seconds" << std::endl;
}

void run_experiments(size_t number_of_epochs)
{
    for (size_t i = 0; i < number_of_epochs; i++)
    {
        experiment(i);
    }
}

int main()
{
    ensure_output_directory();
    run_experiments(10);
}
