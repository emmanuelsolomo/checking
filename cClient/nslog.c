#include <unistd.h>
#include <stdio.h>
#include <curl/curl.h>
#include <stdlib.h>
#include <string.h>


 
int main(void)
{
  CURL *curl;
  CURLcode res;
  const char header_prefix[] = "Authorization: Token ";
  const char str2[] = "Second"; 
  const char* token = getenv("TOKEN");
  const char* url = getenv("URL");

  printf("TOKEN :%s\n",(token!=NULL)? token : "getenv returned NULL");
  printf("URL :%s\n",(url!=NULL)? url : "getenv returned NULL");


  char *header;

  header = malloc(strlen(header_prefix) + strlen(token) + 1);
  if (!header) {
    fprintf(stderr, "malloc() failed: insufficient memory!\n");
    return EXIT_FAILURE;
  }

  strcpy(header, header_prefix);
  strcat(header, token);

  printf("Result: '%s'\n", header);
  free(header);


  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);
 
  /* get a curl handle */ 
  curl = curl_easy_init();
  if(curl) {
    /* First set the URL that is about to receive our POST. This URL can
       just as well be a https:// URL if that is what should receive the
       data. */ 
    struct curl_slist *chunk = NULL;

    chunk = curl_slist_append(chunk, "Authorization: Token a944a33599369265bd255987010203a413e71a5c");

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
    curl_easy_setopt(curl, CURLOPT_URL, url);

    /*Now specify the POST data */

    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "client=nsloger");     
 
    /* Perform the request, res will get the return code */ 
    while(1){

      res = curl_easy_perform(curl);
      /* Check for errors */     
      if(res != CURLE_OK)
	fprintf(stderr, "curl_easy_perform() failed: %s\n",
		curl_easy_strerror(res));
      /* always cleanup */ 
      sleep(60);
      printf("\n");
    }
    curl_easy_cleanup(curl);
  }
  curl_global_cleanup();
  return 0;
}