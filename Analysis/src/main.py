import os
import time
import youtube_scrape as scrape
import data_analysis as da
import print_data as DataPrint

enable_scrape = False
enable_anlysis_all = True
# what analysis wanting to be ran
enable_anlysis_descriptive = True
enable_anlysis_temporal = True
enable_anlysis_engagment_pattern = True
enable_anlysis_duration_exploration = True

if __name__ == '__main__':
    program_start_time = time.time() # track how long program takes
    file_name = "data.csv"
    data_folder = './data/'
    descriptive_analysis_output = './output/descriptive_analysis/'
    temporal_analysis_output = './output/temporal_analysis/'
    engagement_patterns_output = './output/engagement_patterns/'
    duration_exploration_output = './output/duration_exploration/'
    data_path = os.path.join(data_folder, file_name)

    #Channel names we want to scrape
    channels_names = ["@MrBeast", "@MrBeastGaming", "@BeastReacts", "@BeastPhilanthropy"]
    channel_count = len(channels_names)

    #start scrape
    if enable_scrape:
        start_time = time.time() #track how long the scrape takes
        total_scraped = 0
        for channel in channels_names:
            #Scrap the video links on each channel
            urls = scrape.ScrapeChannelVideoLinks(channel)
            #Scrap each video detail and save it to a csv file
            scrape.SaveChannelDetails(data_path, scrape.ScrapeEveryVideo(channel, urls), channel)
            total_scraped += len(urls)
    
        #how much time it took to scrape
        end_time = time.time()
        elapsed_time = end_time - start_time 
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        #print details to finish it off
        print("Scrapes Complete.")
        print("Total videos scraped:", total_scraped)
        print("Total time taken:", minutes, "minutes and", seconds, "seconds!")

    #start analysis
    if enable_anlysis_all:
        start_time = time.time() #track how long the scrape takes

        #descriptive analysis
        if enable_anlysis_descriptive:
            video_counts = da.OverviewOfData(data_path, channels_names, channel_count)
            DataPrint.PrintOverviewOfData(video_counts, channels_names, channel_count)
            summary_statistics = da.SummaryStatistics(data_path, channels_names, channel_count)
            DataPrint.PrintSummaryStatistics(summary_statistics, channels_names, channel_count)
            da.DistributionAnalysis(channels_names, data_path, descriptive_analysis_output)
            da.TemporalPatterns(channels_names, data_path, descriptive_analysis_output)
            da.LikeEngagementOverTime(channels_names, data_path, descriptive_analysis_output)
            da.CategoryDistribution(channels_names, data_path, descriptive_analysis_output)
            da.TagInsights(data_path, descriptive_analysis_output)
            da.DurationAnalysis(data_path, descriptive_analysis_output)
    
        #temporal analysis
        if enable_anlysis_temporal:
            da.UploadTimePatterns(data_path, temporal_analysis_output)
            da.UploadTimeInfluence(data_path, temporal_analysis_output)
            da.UploadDayPatterns(data_path, temporal_analysis_output)
            da.UploadDayInfluence(data_path, temporal_analysis_output)

        #engagement patterns
        if enable_anlysis_engagment_pattern:
            da.EngagementMetricCorrelation(data_path, engagement_patterns_output)
            da.EngagementOverTime(data_path, engagement_patterns_output)
            pass

        #duration exploration
        if enable_anlysis_duration_exploration:
            da.VideoDurationDistribution(data_path, duration_exploration_output)
            da.EngagementVideoDuration(data_path, duration_exploration_output)
            da.DurationTrend(data_path, duration_exploration_output)
            pass

        #how much time it the analysis took
        end_time = time.time()
        elapsed_time = end_time - start_time 
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print("Analysis Complete.")
        print("Total time taken:", minutes, "minutes and", seconds, "seconds!")
    
    end_time = time.time()
    elapsed_time = end_time - program_start_time 
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print("-------------------------")
    print("Program Complete.")
    print("Total time taken:", minutes, "minutes and", seconds, "seconds!")

