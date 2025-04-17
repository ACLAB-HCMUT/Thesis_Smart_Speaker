#include <iostream>
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
static float threshold = 0.49;
// static float arr[10] = {0};
// int i = 0;

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
            printf("  %s: %.5f\n", ei_classifier_inferencing_categories[1], result.classification[1].value);
            // arr[i] = (float)result.classification[1].value;
            // if (i <= 9) i += 1;
            // else i = 0;
            // float sum = 0.0;
            // for (int i = 0; i < 10; i++) {
            //     sum += arr[i];
            // }
            // threshold = sum/10;
            // printf("AVG = %.5f\n", threshold);

                if (result.classification[1].value >= threshold) {
                    printf("  %s: %.5f\n", ei_classifier_inferencing_categories[1], result.classification[1].value);
                    detected_flag = true;
                }
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

// #include <Python.h>
// #include <iostream>
// #include <stdio.h>
// #include <alsa/asoundlib.h>
// #include "edge-impulse-sdk/classifier/ei_run_classifier.h"

// // Audio capture settings
// #define PCM_DEVICE "default"
// unsigned int AUDIO_SAMPLE_RATE = 16000;
// #define AUDIO_FRAME_SIZE EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE

// // Audio buffer for inference
// static float audio_buffer[AUDIO_FRAME_SIZE];

// // Function declarations
// static int get_signal_data(size_t offset, size_t length, float *out_ptr);
// int capture_audio_and_infer();

// int main(int argc, char **argv) {
//     while (true) {
//         int res = capture_audio_and_infer();

//         if (res == 1) {
//             FILE *file;
//             Py_Initialize();

//             file = fopen("command/main.py", "r");
//             if (file != NULL) {
//                 PyRun_SimpleFile(file, "command/main.py");
//                 fclose(file);
//             }

//             Py_Finalize();
//             break;
//         }
//     }

//     return 0;
// }

// // Function to capture audio and run inference
// int capture_audio_and_infer() {
//     snd_pcm_t *pcm_handle;
//     snd_pcm_hw_params_t *params;
//     snd_pcm_uframes_t frames = AUDIO_FRAME_SIZE;
//     short *buffer;
//     int pcm, pcm_rc;

//     // Allocate input buffer
//     buffer = (short *)malloc(AUDIO_FRAME_SIZE * sizeof(short));
//     if (!buffer) {
//         printf("Failed to allocate audio buffer\n");
//         return -1;
//     }

//     // Open PCM device
//     if ((pcm = snd_pcm_open(&pcm_handle, PCM_DEVICE, SND_PCM_STREAM_CAPTURE, 0)) < 0) {
//         printf("ERROR: Can't open PCM device. %s\n", snd_strerror(pcm));
//         free(buffer);
//         return -1;
//     }

//     // Configure hardware parameters
//     snd_pcm_hw_params_alloca(&params);
//     snd_pcm_hw_params_any(pcm_handle, params);
//     snd_pcm_hw_params_set_access(pcm_handle, params, SND_PCM_ACCESS_RW_INTERLEAVED);
//     snd_pcm_hw_params_set_format(pcm_handle, params, SND_PCM_FORMAT_S16_LE);
//     snd_pcm_hw_params_set_channels(pcm_handle, params, 1);
//     snd_pcm_hw_params_set_rate_near(pcm_handle, params, &AUDIO_SAMPLE_RATE, 0);
//     snd_pcm_hw_params_set_period_size_near(pcm_handle, params, &frames, 0);

//     if ((pcm = snd_pcm_hw_params(pcm_handle, params)) < 0) {
//         printf("ERROR: Can't set hardware parameters. %s\n", snd_strerror(pcm));
//         free(buffer);
//         snd_pcm_close(pcm_handle);
//         return -1;
//     }

//     // Read audio from mic
//     pcm_rc = snd_pcm_readi(pcm_handle, buffer, AUDIO_FRAME_SIZE);
//     if (pcm_rc == -EPIPE) {
//         printf("XRUN (overrun).\n");
//         snd_pcm_prepare(pcm_handle);
//     } else if (pcm_rc < 0) {
//         printf("ERROR: Can't read PCM. %s\n", snd_strerror(pcm_rc));
//     } else if (pcm_rc != (int)AUDIO_FRAME_SIZE) {
//         printf("Short read: read %d frames\n", pcm_rc);
//     }

//     // Normalize audio to float [-1.0, 1.0]
//     for (size_t i = 0; i < AUDIO_FRAME_SIZE; i++) {
//         audio_buffer[i] = (float)buffer[i] / 32768.0f;
//     }

//     free(buffer);
//     snd_pcm_close(pcm_handle);

//     // Run classifier
//     signal_t signal;
//     ei_impulse_result_t result;
//     EI_IMPULSE_ERROR res;

//     signal.total_length = AUDIO_FRAME_SIZE;
//     signal.get_data = &get_signal_data;

//     res = run_classifier(&signal, &result, false);

//     if (res != EI_IMPULSE_OK) {
//         printf("Classifier failed (%d)\n", res);
//         return -1;
//     }

//     // printf("Inference result:\n");
//     // printf("Timing: DSP %d ms, inference %d ms, anomaly %d ms\n", 
//     //     result.timing.dsp, result.timing.classification, result.timing.anomaly);

//     for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
//         printf("%s: %.5f\n", ei_classifier_inferencing_categories[1], result.classification[1].value);
//     }
    
//     if (result.classification[1].value > 0.52f) {
//         // printf("%s: %.5f\n", ei_classifier_inferencing_categories[1], result.classification[1].value);
//         return 1;
//     }

//     return 0;
// }

// // Callback for classifier to get signal data
// static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
//     for (size_t i = 0; i < length; i++) {
//         out_ptr[i] = audio_buffer[offset + i];
//     }
//     return EIDSP_OK;
// }
