import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import math
from collections import Counter
from wordcloud import WordCloud
from matplotlib.ticker import MultipleLocator

#help funcs
def FormatNumbers(value):
    if value >= 1_000_000:
        formatter = '{:1.1f}M'.format(value * 0.000_001)
    elif value >= 1_000:
        formatter = '{:1.0f}K'.format(value * 0.001)
    else:
        formatter = '{:1.0f}'.format(value)
    return formatter
def RoundMaxMinRange(number, round_up):
    if number == 0: return 0
    order_of_magnitude = 10 ** math.floor(math.log10(number))
    
    if round_up:
        return order_of_magnitude * math.ceil(number / order_of_magnitude)
    else:
        return order_of_magnitude * math.floor(number / order_of_magnitude)

#descriptive analysis
def OverviewOfData(file_path, channel_names, channel_count):
    df = pd.read_csv(file_path)
    channels_video_count = dict()
    if channel_count > 1:
        channels_video_count['combined'] = df.shape[0]
    
    for channel in channel_names:
        channel_rows = df[df['Channel'].str.lower() == channel.lower()]
        channels_video_count[channel] = channel_rows.shape[0]
    
    return channels_video_count
def SummaryStatistics(file_path, channel_names, channel_count):
    #calculates the mean, median, standard deviation, min, max, and quartiles for views, likes, comments, and duration. For each channel seperate and combined.
    df = pd.read_csv(file_path)
    summary_statistics = dict()
    #get the stats for every channel combined if there is more than 1 channel
    if channel_count > 1:
        summary_statistics['combined_mean'] = [df.loc[:, 'Views'].mean(), df.loc[:, 'Likes'].mean(), df.loc[:, 'Comments'].mean(), df.loc[:, 'Duration'].mean()]
        summary_statistics['combined_median'] = [df.loc[:, 'Views'].median(), df.loc[:, 'Likes'].median(), df.loc[:, 'Comments'].median(), df.loc[:, 'Duration'].median()]
        summary_statistics['combined_std'] = [df.loc[:, 'Views'].std(), df.loc[:, 'Likes'].std(), df.loc[:, 'Comments'].std(), df.loc[:, 'Duration'].std()]
        summary_statistics['combined_min'] = [df.loc[:, 'Views'].min(), df.loc[:, 'Likes'].min(), df.loc[:, 'Comments'].min(), df.loc[:, 'Duration'].min()]
        summary_statistics['combined_max'] = [df.loc[:, 'Views'].max(), df.loc[:, 'Likes'].max(), df.loc[:, 'Comments'].max(), df.loc[:, 'Duration'].max()]
        summary_statistics['combined_quartiles'] = [df.loc[:, 'Views'].quantile([0.25, 0.5, 0.75]), df.loc[:, 'Likes'].quantile([0.25, 0.5, 0.75]), 
                                                    df.loc[:, 'Comments'].quantile([0.25, 0.5, 0.75]), df.loc[:, 'Duration'].quantile([0.25, 0.5, 0.75])]
    #get the mean for each channel on it's own
    for channel in channel_names:
        summary_statistics[channel+'_mean'] = [df.loc[df['Channel']==channel, 'Views'].mean(),
                                               df.loc[df['Channel']==channel, 'Likes'].mean(),
                                                df.loc[df['Channel']==channel, 'Comments'].mean(),
                                                df.loc[df['Channel']==channel, 'Duration'].mean()]
        
        summary_statistics[channel+'_median'] = [df.loc[df['Channel']==channel, 'Views'].median(),
                                                 df.loc[df['Channel']==channel, 'Likes'].median(),
                                                  df.loc[df['Channel']==channel, 'Comments'].median(),
                                                  df.loc[df['Channel']==channel, 'Duration'].median()]
        
        summary_statistics[channel+'_std'] = [df.loc[df['Channel']==channel, 'Views'].std(),
                                              df.loc[df['Channel']==channel, 'Likes'].std(),
                                               df.loc[df['Channel']==channel, 'Comments'].std(),
                                               df.loc[df['Channel']==channel, 'Duration'].std()]
        
        summary_statistics[channel+'_min'] = [df.loc[df['Channel']==channel, 'Views'].min(),
                                              df.loc[df['Channel']==channel, 'Likes'].min(),
                                               df.loc[df['Channel']==channel, 'Comments'].min(),
                                               df.loc[df['Channel']==channel, 'Duration'].min()]
        summary_statistics[channel+'_max'] = [df.loc[df['Channel']==channel, 'Views'].max(),
                                              df.loc[df['Channel']==channel, 'Likes'].max(),
                                                df.loc[df['Channel']==channel, 'Comments'].max(),
                                                df.loc[df['Channel']==channel, 'Duration'].max()]
        
        summary_statistics[channel+'_quartiles'] = [df.loc[df['Channel']==channel, 'Views'].quantile([0.25, 0.5, 0.75]), 
                                                    df.loc[df['Channel']==channel, 'Likes'].quantile([0.25, 0.5, 0.75]), 
                                                    df.loc[df['Channel']==channel, 'Comments'].quantile([0.25, 0.5, 0.75]), 
                                                    df.loc[df['Channel']==channel, 'Duration'].quantile([0.25, 0.5, 0.75])]
    
    return summary_statistics
def CreateDistributionAnalysisGraph(_max, _min, data, channels, data_type, output_folder):
    #set up the y-axis ticks & labels
    step_size = (_max - _min) / 10
    yticks_range = np.arange(_min, _max, step_size)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]

    # create the graph
    fig, ax = plt.subplots(figsize=(10, 6))
    hex_colors = ['#6C567B', '#C06C84','#F67280','#F8B195']
    plt.bar(channels, data, color =hex_colors, width = 1)
    plt.xlabel("Channels",fontsize=12)
    plt.ylabel("No. of "+ data_type,fontsize=12)
    plt.title("Total Channel "+data_type,fontsize=18)

    #apply the ticks & labels
    ax.set_yticks(yticks_range)
    ax.set_yticklabels(yticks_labels)

    #save the graph
    output_path = os.path.join(output_folder, "DistributionAnalysisBar" + data_type)
    plt.savefig(output_path)
    plt.close()
def CreateDistributionAnalysisMath(df, channels, data_type):
    _min = 0
    _max = 0
    if len(channels) > 1:
        data = list()
        for channel in channels:
            data.append(df.loc[df['Channel']==channel, data_type].sum())
        _min = RoundMaxMinRange(min(data), False)
        _max = RoundMaxMinRange(max(data), True)
    else:
        _min = RoundMaxMinRange(df.loc[df['Channel']==channels[0], data_type].min(), False)
        data = df.loc[df['Channel']==channels[0], data_type].max()
        _max = RoundMaxMinRange(data, True)
    return _min, _max, data
def DistributionAnalysis(channels, csv_file_path, output_folder):
    #bar graphs to visualize the view, like, and comment count.

    #read the data file
    df = pd.read_csv(csv_file_path)
    # do the math
    min_views, max_views, views = CreateDistributionAnalysisMath(df, channels, 'Views')
    min_likes, max_likes, likes = CreateDistributionAnalysisMath(df, channels, 'Likes')
    min_comments, max_comments, comments = CreateDistributionAnalysisMath(df, channels, 'Comments')
    # make graphs from the math
    CreateDistributionAnalysisGraph(max_views, min_views, views, channels, 'Views', output_folder)
    CreateDistributionAnalysisGraph(max_likes, min_likes, likes, channels, 'Likes', output_folder)
    CreateDistributionAnalysisGraph(max_comments, min_comments, comments, channels, 'Comments', output_folder)
def GetTemporalPattersMonths(df, channel_name):
    channel_data = df[df['Channel'] == channel_name]
    upload_dates = pd.to_datetime(channel_data['Upload Date'])
    months = upload_dates.dt.month
    return Counter(months)
def CreateTemporalPattersGraph(channel_name, month_counter, output_folder):
    month_names = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December']
    counts = [month_counter[i] for i in range(1, 13)]
    # create the graph
    fig, ax = plt.subplots(figsize=(12, 6))
    hex_colors = ['#6C567B', '#C06C84','#F67280','#F8B195']
    plt.bar(month_names, counts, color =hex_colors, width = 0.5)
    plt.xlabel("Month",fontsize=12)
    plt.ylabel("No. of Uploads",fontsize=12)
    plt.title("Total Uploads Per Month For "+channel_name,fontsize=18)

    #save the graph
    output_path = os.path.join(output_folder, "TemporalPatterns" + channel_name)
    plt.savefig(output_path)
    plt.close()
def TemporalPatterns(channels, csv_file_path, output_folder):
    # using a bar chart, check monthly upload frequencies, to identify periods of increased or decreased activitiy.
    #read the data file
    df = pd.read_csv(csv_file_path)

    for channel in channels:
        months = GetTemporalPattersMonths(df, channel)
        CreateTemporalPattersGraph(channel, months, output_folder)
def CreateLikeEngagementOverTimeGraph(df, channel, output_folder, data_type):
    df['Upload Date'] = pd.to_datetime(df['Upload Date'])
    
    # Filter data for the specified channel
    filtered_df = df[df['Channel'] == channel]

    min_likes = filtered_df['Likes'].min()
    max_likes = filtered_df['Likes'].max()

    step_size = (max_likes - min_likes) / 10
    yticks_range = np.arange(min_likes, max_likes, step_size)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]
    
    # Create the line plot
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(filtered_df['Upload Date'], filtered_df[data_type], label= channel + '\'s ' + data_type)
    
    plt.xlabel('Upload Date', fontsize = 12)
    plt.ylabel(data_type, fontsize = 12)
    plt.title(data_type + ' Engagement Over Time for ' + channel)
    plt.legend()
    plt.grid(True)

    ax.set_yticks(yticks_range)
    ax.set_yticklabels(yticks_labels)

    # Save the graph
    output_path = os.path.join(output_folder, "EngagementOverTime" + channel)
    plt.savefig(output_path)
    plt.close()
def LikeEngagementOverTime(channels, csv_file_path, output_folder):
    # Plot line graphs to visualize how like count change over time
    df = pd.read_csv(csv_file_path)

    for channel in channels:
        CreateLikeEngagementOverTimeGraph(df, channel, output_folder, 'Likes')
def CategoryDistribution(channels, csv_file_path, output_folder):
    # pie chart to show which categories are most prevalent on each channel
    df = pd.read_csv(csv_file_path)

    filtered_df = df[df['Channel'].isin(channels)]
    category_counts = filtered_df.groupby('Category ID').size().reset_index(name='Count')
    category_counts['Percentage'] = (category_counts['Count'] / category_counts['Count'].sum()) * 100
    category_counts = category_counts.sort_values(by='Percentage', ascending=False)

    # create pie chart
    hex_colors = ['#6C567B', '#C06C84','#F67280','#F8B195','#F5E8C7','#ECCCB2','#DEB6AB','#AC7088']
    plt.figure(figsize=(7, 7))
    wedges, _ = plt.pie(category_counts['Count'], startangle=140, colors = hex_colors)

    # create legend
    legend_labels = ['{} - {:.1f}%'.format(cat_id, percentage) for cat_id, percentage in zip(category_counts['Category ID'], category_counts['Percentage'])]
    plt.legend(wedges, legend_labels, title="Category ID", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title('Combined Video Category Distribution', fontsize = 20)
    output_path = os.path.join(output_folder, 'CategoryDistributionPieChart')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
def TagInsights(csv_file_path, output_folder):
    # display the most frequently used tags in a word cloud
    df = pd.read_csv(csv_file_path)
    
    df.dropna(subset=['Tags'], inplace=True)
    all_tags = ' '.join(df['Tags'].astype(str))

    # create word cloud
    wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(all_tags)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Turn off axis labels and ticks

    output_path = os.path.join(output_folder, 'TagInsights')
    plt.savefig(output_path)
    plt.close()
def DurationAnalysis(csv_file_path, output_folder):
    # box plot to visualize whether most videos are of similar lengths or if there's significant variation
    df = pd.read_csv(csv_file_path)
    
    df['Duration'] = df['Duration'].astype(int)
    df_below_60 = df[df['Duration'] <= 60]
    df_above_60 = df[df['Duration'] > 60]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
    # durations below 60
    y_ticks_1 = np.arange(0, 61, 2)
    ax1.boxplot(df_below_60['Duration'])
    ax1.set_title('Video Duration Distribution (0-60 minutes)')
    ax1.set_ylabel('Duration (minutes)')
    ax1.set_xticks([1])
    ax1.set_xticklabels(['Video Duration'])
    ax1.set_yticks(y_ticks_1)
    # durations above 60
    y_ticks_2 = np.arange(0, df_above_60['Duration'].max() + 1, 60)
    ax2.boxplot(df_above_60['Duration'])
    ax2.set_title('Video Duration Distribution (Above 60 minutes)')
    ax2.set_ylabel('Duration (minutes)')
    ax2.set_xticks([1])
    ax2.set_xticklabels(['Video Duration'])
    ax2.set_yticks(y_ticks_2)

    plt.tight_layout()
    output_path = os.path.join(output_folder, 'DurationAnalysis')
    plt.savefig(output_path)
    plt.close()

#temporal analysis
def UploadTimePatterns(csv_file_path, output_folder):
    # line graph for upload time patterns
    df = pd.read_csv(csv_file_path)

    df['Upload Time'] = pd.to_datetime(df['Upload Time'], format='%H:%M')
    df['Hour'] = df['Upload Time'].dt.hour
    upload_counts = df.groupby(['Channel', 'Hour']).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    for channel in upload_counts.index:
        plt.plot(upload_counts.columns, upload_counts.loc[channel], label=channel)
    plt.xlabel('Hour of the Day', fontsize = 14)
    plt.ylabel('Number of Uploads', fontsize = 14)
    plt.title('Upload Time Patterns', fontsize = 18)
    plt.xticks(range(0, 24))
    plt.legend()
    plt.grid(True)

    output_path = os.path.join(output_folder, 'UploadTimePatterns')
    plt.savefig(output_path)
    plt.close()
def CreateUploadTimeInfluenceGraph(df, output_folder, data_type):
    df['Upload Time'] = pd.to_datetime(df['Upload Time'], format='%H:%M')
    df['Hour'] = df['Upload Time'].dt.hour
    hour_grouped = df.groupby('Hour')[[data_type]].mean()
    
    max_ = max(hour_grouped[data_type])
    yticks_range = np.arange(0, RoundMaxMinRange(max_, round_up=True) + 1, RoundMaxMinRange(max_, round_up=True) / 10)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]

    plt.figure(figsize=(10, 6))
    plt.plot(hour_grouped.index, hour_grouped[data_type], label=data_type)
    plt.xlabel('Hour of the Day', fontsize = 14)
    plt.ylabel('Average Likes', fontsize = 14)
    plt.title('Upload Time Influence - ' + data_type, fontsize = 18)
    plt.xticks(range(24))
    plt.legend()
    plt.grid(True)
    plt.yticks(yticks_range, yticks_labels)
    output_path = os.path.join(output_folder, 'UploadTimeInfluence_'+data_type)
    plt.savefig(output_path)
    plt.close()
def UploadTimeInfluence(csv_file_path, output_folder):
    # line graphs for relationship between upload time engagement metrics
    df = pd.read_csv(csv_file_path)

    CreateUploadTimeInfluenceGraph(df, output_folder, 'Likes')
    CreateUploadTimeInfluenceGraph(df, output_folder, 'Views')
    CreateUploadTimeInfluenceGraph(df, output_folder, 'Comments')
def UploadDayPatterns(csv_file_path, output_folder):
    # A bar graph illustrates the volume of video uploads for each weekday. 
    # Each bar corresponds to a specific weekday, depicting the number of videos released on that day.
    df = pd.read_csv(csv_file_path)

    # Convert the 'Upload Date' column to datetime format
    df['Upload Date'] = pd.to_datetime(df['Upload Date'])
    
    # Extract the weekday from the 'Upload Date' column and order the days
    weekdays_ordered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['Weekday'] = df['Upload Date'].dt.day_name()
    df['Weekday'] = pd.Categorical(df['Weekday'], categories=weekdays_ordered, ordered=True)
    
    # Group the data by weekday and count the number of videos for each weekday
    weekday_counts = df['Weekday'].value_counts().sort_index()
    
    # Define the hex colors
    hex_colors = ['#6C567B', '#C06C84', '#F67280', '#F8B195', '#F5E8C7', '#ECCCB2', '#DEB6AB', '#AC7088']
    
    # Create the bar graph using the specified colors
    plt.figure(figsize=(9, 10))
    plt.bar(weekday_counts.index, weekday_counts.values, color=hex_colors)
    plt.xlabel('Weekday', fontsize = 14)
    plt.ylabel('Number of Videos', fontsize = 14)
    plt.title('Volume of Video Uploads for Each Weekday', fontsize=18)
    plt.xticks(rotation=45)

    plt.yticks(range(0, max(weekday_counts.values) + 60, 20))

    output_path = os.path.join(output_folder, 'UploadDayPatters')
    plt.savefig(output_path)
    plt.tight_layout()
    plt.close()
def CreateUploadDayInfluenceGraph(df, output_folder, data_type):
    df['Upload Date'] = pd.to_datetime(df['Upload Date'])
    df['Weekday'] = df['Upload Date'].dt.weekday
    day_grouped = df.groupby('Weekday')[[data_type]].mean()
    
    max_ = max(day_grouped[data_type])
    yticks_range = np.arange(0, RoundMaxMinRange(max_, round_up=True) + 1, RoundMaxMinRange(max_, round_up=True) / 10)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    plt.figure(figsize=(10, 6))
    plt.plot(day_grouped.index, day_grouped[data_type], label=data_type)
    plt.xlabel('Weekday', fontsize=14)
    plt.ylabel('Average ' + data_type, fontsize=14)
    plt.title('Upload Day Influence - ' + data_type, fontsize=18)
    plt.xticks(range(7), weekdays)
    plt.legend()
    plt.grid(True)
    plt.yticks(yticks_range, yticks_labels)
    output_path = os.path.join(output_folder, 'UploadDayInfluence_' + data_type)
    plt.savefig(output_path)
    plt.close()
def UploadDayInfluence(csv_file_path, output_folder):
    # line graphs for relationship between upload day engagement metrics
    df = pd.read_csv(csv_file_path)

    CreateUploadDayInfluenceGraph(df, output_folder, 'Likes')
    CreateUploadDayInfluenceGraph(df, output_folder, 'Views')
    CreateUploadDayInfluenceGraph(df, output_folder, 'Comments')

#engagement patterns
def CreateEngagementMetricCorrelationGraph(df, output_folder, x_data, y_data):
    engagement_df = df[[x_data, y_data]]
    plt.figure(figsize=(10, 6))
    plt.scatter(engagement_df[x_data], engagement_df[y_data], c='blue', alpha=0.7)
    plt.xlabel(x_data, fontsize = 14)
    plt.ylabel(y_data, fontsize = 14)
    plt.title(x_data+' to ' +y_data+ ' Engagement Correlation', fontsize = 18)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: FormatNumbers(x)))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: FormatNumbers(y)))
    
    output_path = os.path.join(output_folder, 'EngagementMetricCorrelation_'+ x_data + y_data)
    plt.savefig(output_path)
    plt.close()
def EngagementMetricCorrelation(csv_file_path, output_folder):
    # scatter plot to depict the correlation between engagement metrics
    df = pd.read_csv(csv_file_path)
    CreateEngagementMetricCorrelationGraph(df, output_folder, "Views", "Likes")
    CreateEngagementMetricCorrelationGraph(df, output_folder, "Views", "Comments")
    CreateEngagementMetricCorrelationGraph(df, output_folder, "Likes", "Comments")
def CreateEngagementOverTimeGraph(df, output_folder, data_type):
    df['Upload DateTime'] = pd.to_datetime(df['Upload Date'] + ' ' + df['Upload Time'])
    df = df.sort_values(by='Upload DateTime')
    time_period = 'Y'
    grouped = df.groupby(pd.Grouper(key='Upload DateTime', freq=time_period)).sum()
    
    min_likes = grouped[data_type].min()
    max_likes = grouped[data_type].max()
    max_likes = max_likes + (max_likes * .1)

    step_size = (max_likes - min_likes) / 10
    yticks_range = np.arange(min_likes, max_likes, step_size)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]
    
    plt.figure(figsize=(10, 6))
    plt.plot(grouped.index, grouped[data_type])
    plt.xlabel('Years', fontsize=14)
    plt.ylabel(data_type, fontsize=14)
    plt.title('Total ' +data_type + ' Each Year', fontsize=18)
    plt.grid(True)
    ax = plt.gca()
    ax.set_yticks(yticks_range)
    ax.set_yticklabels(yticks_labels)
    
    output_path = os.path.join(output_folder, 'EngagementOverTime_'+data_type)
    plt.savefig(output_path)
    plt.close()
def EngagementOverTime(csv_file_path, output_folder):
    #line graphs for engagement metrics over time
    df = pd.read_csv(csv_file_path)
    CreateEngagementOverTimeGraph(df, output_folder, 'Views')
    CreateEngagementOverTimeGraph(df, output_folder, 'Likes')
    CreateEngagementOverTimeGraph(df, output_folder, 'Comments')

#duration exploration
def VideoDurationDistribution(csv_file_path, output_folder):
    # histogram to display video durations across each channel
    df = pd.read_csv(csv_file_path)
    
    channel_durations = {}
    for index, row in df.iterrows():
        channel = row['Channel']
        duration = row['Duration']
        
        if channel not in channel_durations:
            channel_durations[channel] = {'below_60': [], 'above_60': []}

        if duration <= 60:
            channel_durations[channel]['below_60'].append(duration)
        else:
            channel_durations[channel]['above_60'].append(duration)
    
    for channel, durations_dict in channel_durations.items():
        plt.figure(figsize=(10, 6))
        if durations_dict['below_60']:
            if durations_dict['above_60']:
                plt.subplot(1, 2, 1)
            plt.hist(durations_dict['below_60'], bins=20, alpha=0.7)
            plt.xlabel('Duration in Minutes', fontsize = 14)
            plt.ylabel('Number of Videos', fontsize = 14)
            plt.title('Video Duration < 60 for ' + channel, fontsize = 18)
            plt.grid(True)

        if durations_dict['above_60']:
            plt.subplot(1, 2, 2)
            plt.hist(durations_dict['above_60'], bins=20, alpha=0.7)
            plt.xlabel('Duration in Minutes', fontsize = 14)
            plt.ylabel('Number of Videos', fontsize = 14)
            plt.title('Video Duration > 60 for ' + channel, fontsize = 18)
            plt.grid(True)

        plt.tight_layout()
        channel_plot_path = os.path.join(output_folder, 'VideoDurationDistribution_'+channel)
        plt.savefig(channel_plot_path)
        plt.close()
def CreateEngagementVideoDurationGraph(df, output_folder, data_type):
    df_under_60 = df[df['Duration'] < 60]
    _max = df_under_60[data_type].min()
    _min = df_under_60[data_type].max()
    step_size = (_max - _min) / 10
    yticks_range = np.arange(_min, _max, step_size)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]
    
    plt.figure(figsize=(9, 6))
    plt.scatter(df_under_60['Duration'], df_under_60[data_type], color='blue', alpha=0.5)
    plt.xlabel('Video Duration (minutes)', fontsize = 14)
    plt.ylabel('Number of ' + data_type, fontsize = 14)
    plt.title('Engagement ' + data_type + ' vs. Video Duration (Under 60 Minutes)', fontsize = 18)
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(base=2))
    ax.set_yticks(yticks_range)
    ax.set_yticklabels(yticks_labels)
    
    output_path_under_60 = os.path.join(output_folder, 'EngagementVideoDuration_'+ data_type)
    plt.savefig(output_path_under_60)
    plt.close()
def EngagementVideoDuration(csv_file_path, output_folder):
    #scatter plots for engagement to video duration
    df = pd.read_csv(csv_file_path)
    CreateEngagementVideoDurationGraph(df, output_folder, 'Views')
    CreateEngagementVideoDurationGraph(df, output_folder, 'Likes')
    CreateEngagementVideoDurationGraph(df, output_folder, 'Comments')
def CreateDurationTrendGraph(df, output_folder, data_type):
    df['Duration'] = df['Duration'].astype(int)
    df[data_type] = df[data_type].astype(int)
    df_filtered = df[df['Duration'] < 60]
    duration_views = df_filtered.groupby('Duration')[data_type].sum()

    max_ = max(duration_views.values)
    yticks_range = np.arange(0, RoundMaxMinRange(max_, round_up=True) + 1, RoundMaxMinRange(max_, round_up=True) / 10)
    yticks_labels = [FormatNumbers(value) for value in yticks_range]
    
    plt.figure(figsize=(10, 6))
    plt.plot(duration_views.index, duration_views.values, marker='o')
    plt.xlabel('Video Duration (minutes)', fontsize = 14)
    plt.ylabel('Sum of ' + data_type, fontsize = 14)
    plt.title('Trends in '+data_type+' over Video Duration < 60 minutes', fontsize=18)
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(base=2))
    ax.set_yticks(yticks_range)
    ax.set_yticklabels(yticks_labels)

    output_path = os.path.join(output_folder, 'DurationTrend_'+data_type)
    plt.savefig(output_path)
    plt.close()
def DurationTrend(csv_file_path, output_folder):
    #line graphs for trends in engagement over video duration
    df = pd.read_csv(csv_file_path)
    CreateDurationTrendGraph(df, output_folder, 'Views')
    CreateDurationTrendGraph(df, output_folder, 'Likes')
    CreateDurationTrendGraph(df, output_folder, 'Comments')

    
    

