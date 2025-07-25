
def OverviewOfDataFormat(header, dict_key, video_counts):
    print(header)
    print("Video Count:", video_counts[dict_key])
    print("------------------------")

def PrintOverviewOfData(video_counts, channels, channel_count):
    print("--- Overview of Data ---")
    if channel_count > 1:
        OverviewOfDataFormat("All Channels:", "combined", video_counts)
    for channel in channels:
        OverviewOfDataFormat(channel+ ":", channel, video_counts)

def SummaryStatisticsFormat(header, dict_key,summary_statistics):
    print(header)
    print("Mean:                    | Views({:.0f}) | Likes ({:.0f}) | Comments({:.0f}) | Duration({:.2f}) |".format(
        summary_statistics[dict_key+'_mean'][0],
        summary_statistics[dict_key+'_mean'][1],
        summary_statistics[dict_key+'_mean'][2],
        summary_statistics[dict_key+'_mean'][3]))
    print("Median:                  | Views({:.0f}) | Likes ({:.0f}) | Comments({:.0f}) | Duration({:.2f}) |".format(
        summary_statistics[dict_key+'_median'][0],
        summary_statistics[dict_key+'_median'][1],
        summary_statistics[dict_key+'_median'][2],
        summary_statistics[dict_key+'_median'][3]))
    print("STD:                     | Views({:.0f}) | Likes ({:.0f}) | Comments({:.0f}) | Duration({:.2f}) |".format(
        summary_statistics[dict_key+'_std'][0],
        summary_statistics[dict_key+'_std'][1],
        summary_statistics[dict_key+'_std'][2],
        summary_statistics[dict_key+'_std'][3]))
    print("Minimum:                 | Views({:.0f}) | Likes ({:.0f}) | Comments({:.0f}) | Duration({:.2f}) |".format(
        summary_statistics[dict_key+'_min'][0],
        summary_statistics[dict_key+'_min'][1],
        summary_statistics[dict_key+'_min'][2],
        summary_statistics[dict_key+'_min'][3]))
    print("Maximum:                 | Views({:.0f}) | Likes ({:.0f}) | Comments({:.0f}) | Duration({:.2f}) |".format(
        summary_statistics[dict_key+'_max'][0],
        summary_statistics[dict_key+'_max'][1],
        summary_statistics[dict_key+'_max'][2],
        summary_statistics[dict_key+'_max'][3]))

    print("Quartiles(25%, 50%, 75%):| Views({:.0f},{:.0f},{:.0f}) | Likes({:.0f},{:.0f},{:.0f}) | Comments({:.0f},{:.0f},{:.0f}) | Duration({:.2f},{:.2f},{:.2f}) |".format(
        summary_statistics[dict_key+'_quartiles'][0].loc[0.25],
        summary_statistics[dict_key+'_quartiles'][0].loc[0.5],
        summary_statistics[dict_key+'_quartiles'][0].loc[0.75],
        summary_statistics[dict_key+'_quartiles'][1].loc[0.25],
        summary_statistics[dict_key+'_quartiles'][1].loc[0.5],
        summary_statistics[dict_key+'_quartiles'][1].loc[0.75],
        summary_statistics[dict_key+'_quartiles'][2].loc[0.25],
        summary_statistics[dict_key+'_quartiles'][2].loc[0.5],
        summary_statistics[dict_key+'_quartiles'][2].loc[0.75],
        summary_statistics[dict_key+'_quartiles'][3].loc[0.25],
        summary_statistics[dict_key+'_quartiles'][3].loc[0.5],
        summary_statistics[dict_key+'_quartiles'][3].loc[0.75]))
    print("--------------------------")

def PrintSummaryStatistics(summary_statistics, channels, channel_count):
    print("--- Summary Statistics ---")
    if channel_count > 1:
        SummaryStatisticsFormat("All Channels:", "combined", summary_statistics)
    for channel in channels:
        SummaryStatisticsFormat(channel+ ":", channel, summary_statistics)