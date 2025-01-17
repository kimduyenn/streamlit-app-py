import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

# Read the data from Excel
data = pd.read_excel('D:\Athlete_events.xlsx')

# Set the page configuration
st.set_page_config(page_title="PYTHON 2 - BUSINESS IT 2", page_icon="🥰", layout="wide")

# HEADER SECTION
with st.container():
    st.subheader("Hi everyone :😉: we're from group 7 class afternoon Business IT2")
    st.title("What is there more to know about Olympic Athletes?")
    st.write("Apart from their achievements, join us today on this app to get to know the athletes' Birth Countries and Average Age of Participation!") 

# OUR DATASET
url = "https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results"
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column: st.header("Our dataset :sparkles:")
    st.markdown(f"[Click here to see the original dataset]({url})")
    st.write("##")
    st.write(
        """ Our refined data frame contains several main variables as follows:
        \n - *Name*: Name of the athlete
        \n - *Sport*: Sport they competed in
        \n - *Event*: Specific event they participated in
        \n - *Medal*: Type of medal they won (if any)
        \n - *NOC*: National Olympic Committee (country) they represented
        \n - *Age*: Age of the athlete at the time of the event """)

st.divider()
st.header("Top Birth Countries, Age Distribution, and Geographic Distribution Chart")
st.write("Discover these three graphs below with us")

# Add Sidebar
st.sidebar.write('**:bulb: Reporting to Dr. Tan Duc Do**')
st.sidebar.write('**:bulb: Group 7 Business IT 2 Members:**')

# Add content to the main area
with st.sidebar:
    st.write('Tran Thi Thuy Trang')
    st.write('Tran Ngoc My Thao')
    st.write('Luong Nu Mai Nhung')
    st.write('Kim Duyen')


# Initial 3 tabs for each interactive graph
tab1, tab2, tab3 = st.tabs(["Bar Chart", "Boxplot Chart", "Geographic Distribution"])

### TAB 1: BAR CHART

# Calculate the value counts of NOC (National Olympic Committees)
df = data['NOC'].value_counts()

# Set the initial value for the slider
value = 5

# Get the top N countries with the most participating athletes
df1 = df.nlargest(n=value, keep='all')

# Define color palette for the bars
color1 = ["#19376D", "#576CBC", "#A5D7E8", "#66347F", "#9E4784", "#D27685", "#D4ADFC", "#F2F7A1", "#FB2576", "#E94560"]

# Add the slider
value = tab1.slider("Number of Countries", min_value=1, max_value=10, step=1, value=value)

# Update the top N countries based on the slider value
df1 = df.nlargest(n=value, keep='all')
color1 = color1[:len(df1)]

# Update the title of the plot
tab1.subheader("Top {} Countries That Had The Most Olympic Athletes".format(value))

# Create the bar chart using Altair
bar_data = pd.DataFrame({"Country": df1.index, "Number of Athletes": df1.values, "Color": color1})
bars = alt.Chart(bar_data).mark_bar().encode(
    x=alt.X('Country', sort=None),
    y=alt.Y('Number of Athletes'),
    color=alt.Color('Color', scale=None),
    tooltip=['Country', 'Number of Athletes']
).properties(width=1400)

# Rotate x-axis labels for better readability
bars = bars.configure_axisX(labelAngle=0)

# Display the chart using Streamlit
tab1.altair_chart(bars, use_container_width=True)

### TAB 2: BOXPLOT CHART

# Filter data to remove rows with missing 'Age'
data = data.dropna(subset=['Age'])

# Sort the data by Age in ascending order
data_sorted = data.sort_values(by='Age', ascending=True)

# Create a subset of data for Summer and Winter Olympics
summer = data_sorted[data_sorted['Season'] == 'Summer']
winter = data_sorted[data_sorted['Season'] == 'Winter']

# Create a palette color for seasons
season_colors = {
    'Summer': '#FFD700',
    'Winter': '#00BFFF'
}

# Add the title of the plot
tab2.subheader("Age Distribution of Olympic Athletes")

# Store the initial value of widgets in session state
if "disabled" not in st.session_state:
    st.session_state.disabled = False

col1, col2, col3 = tab2.columns([2,2,3])
with col1:
    overview = st.checkbox("Overview of all seasons", key="disabled")
    age_type = st.radio("Choose a value you want to look for 👇",
                        ["Oldest age", "Median age", "Youngest age"],
                        key="visibility",
                        # label_visibility= "visible",
                        disabled= st.session_state.disabled)
with col2:
    rank = st.selectbox("Rank", ("Maximum", "Minimum"), key="rank",
                        # label_visibility= "visible",
                        disabled= st.session_state.disabled)
with col3:
    if overview:
        st.write("Below is all seasons.")
    else:
        st.write("Below are all seasons with")
        st.write("the {} value of the {} in each group.".format(rank.lower(), age_type.lower()))
        st.write(":green[**Note: Outlier values are accepted.**]")

# Create a container for displaying the boxplots
with tab2.container():
    
    # define a function to find the season as requested
    def find_season(data, age_type, rank):
        if age_type == "Oldest age":
            if rank == "Maximum":
                season = data.groupby('Season')['Age'].max().idxmax()
            else:
                season = data.groupby('Season')['Age'].max().idxmin()
        elif age_type == "Median age":
            if rank == "Maximum":
                season = data.groupby('Season')['Age'].median().idxmax()
            else:
                season = data.groupby('Season')['Age'].median().idxmin()
        elif age_type == "Youngest age":
            if rank == "Maximum":
                season = data.groupby('Season')['Age'].min().idxmax()
            else:
                season = data.groupby('Season')['Age'].min().idxmin()
        return season
    
    # Create two columns for displaying the boxplots
    box1, box2 = tab2.columns(2)
    with box1:
        # Add label above the first boxplot
        st.subheader("Summer Olympics")
        
        # Display the first boxplot
        if overview:
            fig1 = px.box(summer, y="Age", x="Season", color="Season", color_discrete_map=season_colors)
            fig1.update_layout(showlegend=False)  # Remove legend from the first plot
        else:
            summer_season = find_season(summer, age_type, rank)
            summer_display_season = summer[summer['Season'].isin([summer_season])]
            fig1 = px.box(summer_display_season, y="Age", x="Season", color="Season", color_discrete_map=season_colors)
            fig1.update_layout(showlegend=False)  # Remove legend from the first plot

        st.plotly_chart(fig1, use_container_width=True)


    with box2:
        # Add label above the second boxplot
        st.subheader("Winter Olympics")

        # Display the second boxplot
        if overview:
            fig2 = px.box(winter, y="Age", x="Season", color="Season", color_discrete_map=season_colors)
            fig2.update_layout(showlegend=False)  # Remove legend from the second plot
        else:
            winter_season = find_season(winter, age_type, rank)
            winter_display_season = winter[winter['Season'].isin([winter_season])]
            fig2 = px.box(winter_display_season, y="Age", x="Season", color="Season", color_discrete_map=season_colors)
            fig2.update_layout(showlegend=False)  # Remove legend from the second plot

        st.plotly_chart(fig2, use_container_width=True)

### TAB 3: GEOGRAPHIC DISTRIBUTION

# Calculate the count of athletes by birth country
athlete_counts = data['NOC'].value_counts().reset_index()
athlete_counts.columns = ['NOC', 'Count']

# Add the title of the plot
tab3.subheader("Geographic Distribution of Olympic Athletes' Birth Countries")

# Create the map visualization
fig_map = px.scatter_geo(
    athlete_counts,
    locations="NOC",
    color="Count",
    hover_name="NOC",
    size="Count",
    projection="natural earth",
    title="Olympic Athletes' Birth Countries",
)

# Display the map
tab3.plotly_chart(fig_map, use_container_width=True)
