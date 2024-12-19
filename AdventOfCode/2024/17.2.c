#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Define constants
#define PROGRAM_LENGTH 16
#define MAX_OUTPUT_SIZE PROGRAM_LENGTH
#define MAX_I 10000000000ULL  // 10,000,000,000

// Function to perform the "run" logic
void run(uint64_t register_a, uint64_t register_b, uint64_t register_c, int program[], int program_length, int *out, int *out_length) {
    uint64_t instr_ptr = 0;
    *out_length = 0;

    while (instr_ptr < (uint64_t)(program_length - 1)) {
        int instruct = program[instr_ptr];
        int org_value = program[instr_ptr + 1];
        instr_ptr += 2;

        int value;
        if (org_value >= 0 && org_value <= 3) {
            value = org_value;
        } else if (org_value == 4) {
            value = (int)register_a;
        } else if (org_value == 5) {
            value = (int)register_b;
        } else if (org_value == 6) {
            value = (int)register_c;
        } else {
            fprintf(stderr, "Invalid org_value: %d\n", org_value);
            exit(EXIT_FAILURE);
        }

        switch (instruct) {
            case 0:
                if (value >= 64) {
                    fprintf(stderr, "Shift value too large for instruction 0: %d\n", value);
                    exit(EXIT_FAILURE);
                }
                register_a /= (1ULL << value);
                break;
            case 1:
                register_b ^= (uint64_t)org_value;
                break;
            case 2:
                register_b = value % 8;
                break;
            case 3:
                if (register_a != 0) {
                    if (org_value >= program_length) {
                        fprintf(stderr, "Jump to invalid instruction pointer: %d\n", org_value);
                        exit(EXIT_FAILURE);
                    }
                    instr_ptr = org_value;
                }
                break;
            case 4:
                register_b ^= register_c;
                break;
            case 5:
                if (*out_length >= PROGRAM_LENGTH) {
                    return;
                }
                out[*out_length] = value % 8;
                (*out_length)++;
                break;
            case 6:
                if (value >= 64) {
                    fprintf(stderr, "Shift value too large for instruction 6: %d\n", value);
                    exit(EXIT_FAILURE);
                }
                register_b = register_a / (1ULL << value);
                break;
            case 7:
                if (value >= 64) {
                    fprintf(stderr, "Shift value too large for instruction 7: %d\n", value);
                    exit(EXIT_FAILURE);
                }
                register_c = register_a / (1ULL << value);
                break;
            default:
                fprintf(stderr, "Invalid instruction: %d\n", instruct);
                exit(EXIT_FAILURE);
        }
    }
}

int main(const int argc, const char *argv[]) {
    // Initialize registers based on the provided input
    uint64_t initial_register_a = 51064159;
    uint64_t initial_register_b = 0;
    uint64_t initial_register_c = 0;

    // Define the program
    int program[PROGRAM_LENGTH] = {2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0};

    // Prepare output buffer
    int out[MAX_OUTPUT_SIZE];
    int out_length = 0;

    // read in i min and i max from sys args
    uint64_t i_min = 0;
    uint64_t i_max = 0;

    if (argc == 3) {
        i_min = strtoull(argv[1], NULL, 10);
        i_max = strtoull(argv[2], NULL, 10);
    } else {
        fprintf(stderr, "Usage: %s <i_min> <i_max>\n", argv[0]);
        return 1;
    }

    // Iterate over possible values of 'i'
    for (uint64_t i = i_min; i < i_max; i++) {
        // Optional: Print progress every 1 million iterations
        if (i % 1000000 == 0 && i != 0) {
            // printf("Checked up to i = %llu\n", i);
        }
        // Run the program with current 'i' as Register A
        run(i, initial_register_b, initial_register_c, program, PROGRAM_LENGTH, out, &out_length);

        // Compare the output with the program
        // First, check if lengths match
        if (out_length != PROGRAM_LENGTH) {
            out_length = 0;  // Reset for next iteration
            continue;
        }

        // Then, check each element
        int match = 1;
        for (int j = 0; j < PROGRAM_LENGTH; j++) {
            if (out[j] != program[j]) {
                match = 0;
                break;
            }
        }

        if (match) {
            printf("Found matching i: %llu\n", i);
            return 0;
        }

        // Reset output length for next iteration
        out_length = 0;
    }

    printf("No matching 'i' found up to %llu\n", MAX_I);
    return 0;
}
