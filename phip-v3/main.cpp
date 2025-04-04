#include <math.h>
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <portaudio.h>
#include <thread>
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"
#include <cstdlib>
#include <string>
using namespace std;

#define SAMPLE_RATE 16000
#define FRAME_LENGTH EI_CLASSIFIER_RAW_SAMPLE_COUNT

static float audio_buffer[FRAME_LENGTH];
static int audio_index = 0;
static bool detected_flag = false;
static float threshold = 0.5;

// PortAudio callback function
static int audio_callback(const void *inputBuffer, void *outputBuffer,
                          unsigned long framesPerBuffer,
                          const PaStreamCallbackTimeInfo* timeInfo,
                          PaStreamCallbackFlags statusFlags,
                          void *userData) {
    float *in = (float*) inputBuffer;
    if (in == NULL) return paContinue;

    for (unsigned int i = 0; i < framesPerBuffer; i++) {
        audio_buffer[audio_index++] = in[i];
        if (audio_index >= FRAME_LENGTH) {
            audio_index = 0;
            signal_t signal;
            ei_impulse_result_t result;
            signal.total_length = FRAME_LENGTH;
            signal.get_data = [](size_t offset, size_t length, float *out_ptr) -> int {
                for (size_t i = 0; i < length; i++) {
                    out_ptr[i] = audio_buffer[offset + i];
                }
                return EIDSP_OK;
            };

            EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);
            // printf("Inference result: %d\n", res);
            // for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
                if (result.classification[1].value >= threshold) {
                    printf("  %s: %.5f\n", ei_classifier_inferencing_categories[1], result.classification[1].value);
                    detected_flag = true;
                }
            // }
        }
    }
    return paContinue;
}

int main() {
        PaStream *stream;
        Pa_Initialize();
        Pa_OpenDefaultStream(&stream, 1, 0, paFloat32, SAMPLE_RATE, FRAME_LENGTH, audio_callback, NULL);
        Pa_StartStream(stream);
        
        while (1) {
            if (detected_flag) {
                system("python3 command/main.py");
            }
            detected_flag = false;
            Pa_Sleep(100);
        }

        Pa_StopStream(stream);
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
}
