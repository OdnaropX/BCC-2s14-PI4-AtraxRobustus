#include <stdio.h>
#include <CkSpider.h>

int main()
    {
    //  The Chilkat Spider component/library is free.
    CkSpider spider;

    //  The spider object crawls a single web site at a time.  As you'll see
    //  in later examples, you can collect outbound links and use them to
    //  crawl the web.  For now, we'll simply spider 10 pages of chilkatsoft.com
    spider.Initialize("vndb.org");

    //  Add the 1st URL:
    spider.AddUnspidered("http://vndb.org/");/*
    spider.AddUnspidered("http://www.chilkatsoft.com/");
    spider.AddUnspidered("http://www.chilkatsoft.com/");
    spider.AddUnspidered("http://www.chilkatsoft.com/");
    spider.AddUnspidered("http://www.chilkatsoft.com/");
    spider.AddUnspidered("http://www.chilkatsoft.com/");*/

    //  Begin crawling the site by calling CrawlNext repeatedly.
    long i;
    for (i = 0; i <= 9; i++) {
        bool success;
        success = spider.CrawlNext();
        if (success == true) {
            //  Show the URL of the page just spidered.
            printf("%s\n",spider.lastUrl());
            //  The HTML is available in the LastHtml property
        }
        else {
            //  Did we get an error or are there no more URLs to crawl?
            if (spider.get_NumUnspidered() == 0) {
                printf("No more URLs to spider\n");
            }
            else {
                printf("%s\n",spider.lastErrorText());
            }

        }

        //  Sleep 1 second before spidering the next URL.
        //spider.SleepMs(1000);
    }
	
	while(1);
    }