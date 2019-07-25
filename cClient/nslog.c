#include <sys/socket.h>
#include <sys/ioctl.h>
/*#include <linux/if.h>*/
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <stdio.h>
#include <curl/curl.h>
#include <stdlib.h>
#include <string.h>
#define CURL_STATICLIB


int nslog(void)
{
  CURL *curl;
  CURLcode res;
  char *header;
  const char header_prefix[] = "Authorization: Token ";
  const char* token = getenv("TOKEN");
  //int cpt=0;
  int status = 0;


  printf("TOKEN :%s\n",(token!=NULL)? token : "getenv returned NULL");

  header = malloc(strlen(header_prefix) + strlen(token) + 1);
  if (!header) {
    fprintf(stderr, "malloc() failed: insufficient memory!\n");
    return EXIT_FAILURE;
  }
  strcpy(header, header_prefix);
  strcat(header, token);

  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);
 
  /* get a curl handle */ 
  curl = curl_easy_init();
  if(curl) {
      /* First set the URL that is about to receive our POST. This URL can
       just as well be a https:// URL if that is what should receive the
       data. */ 
      struct curl_slist *chunk = NULL;

      /*chunk = curl_slist_append(chunk, "Authorization: Token a944a33599369265bd255987010203a413e71a5c");*/
      printf("%s\n",header);
      chunk = curl_slist_append(chunk, header);

      curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
      curl_easy_setopt(curl, CURLOPT_URL, "https://netsoul.owaale.com/logs");
      curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);      
      /*curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0);*/
      /*Now specify the POST data */
      
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "client=nsloger");     
      
      /* Perform the request, res will get the return code */ 

      res = curl_easy_perform(curl);

      /* Check for errors */     
      if(res != CURLE_OK)
      {
          write(1,"Something bad happen\n",21);
          fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
          status = 1;
      }
      curl_easy_cleanup(curl);
  }
  curl_global_cleanup();
  free(header);
  printf("\n");
  return status;
}
