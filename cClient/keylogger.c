#include <linux/input.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include "keylogger.h"

#define BUFFER_SIZE 100
#define NUM_KEYCODES 71

int nslog(void);


int loop = 1;

void sigint_handler(int sig){
    loop = 0;
}

/**
 * Ensures that the string pointed to by str is written to the file with file
 * descriptor file_desc.
 *
 * \returns 1 if writing completes succesfully, else 0
 */
int write_all(int file_desc, const char *str){
    int bytesWritten = 0;
    int bytesToWrite = strlen(str) + 1;

    do {
        bytesWritten = write(file_desc, str, bytesToWrite);

        if(bytesWritten == -1){
            return 0;
        }
        bytesToWrite -= bytesWritten;
        str += bytesWritten;
    } while(bytesToWrite > 0);

    return 1;
}


/**
 * Wrapper around write_all which exits safely if the write fails, without
 * the SIGPIPE terminating the program abruptly.
 */
void monitorKeyStroke (struct timespec time)
{
    static int begin = 0;
    static struct timespec lastCall;
    struct timespec timeDiff;
    
    if (begin == 0 ){
        lastCall = time;
        //appelle API
        if (nslog() == 0)
            begin++;            
    }else{
        printf("******************************************\n");
        timeDiff.tv_sec = time.tv_sec - lastCall.tv_sec;
        if ((unsigned long)timeDiff.tv_sec > 300){
            printf("time: %ld \n", time.tv_sec);
            printf("last call time: %ld \n", lastCall.tv_sec);
            printf("diff time: %ld \n", timeDiff.tv_sec);            
            printf("new last call time: %ld \n", lastCall.tv_sec);
            if (nslog() == 0)
                lastCall = time;
        }else{
            write(1,"too soon\n",9);
        }
    }
    
}
void keylogger(int keyboard, int writeout){
    int eventSize = sizeof(struct input_event);
    int bytesRead = 0;
    struct input_event events[NUM_EVENTS];
    int i;
    struct timespec t;

    //signal(SIGINT, sigint_handler);

    nslog();            
    while(loop){
        bytesRead = read(keyboard, events, eventSize * NUM_EVENTS);

        for(i = 0; i < (bytesRead / eventSize); ++i){
            if(events[i].type == EV_KEY){
                if(events[i].value == 1){
                    timespec_get(&t, TIME_UTC);//t = clock();
                    monitorKeyStroke (t);
                }
            }
        }
        //sleep(60);
    }
}
